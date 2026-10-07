import os
import xarray as xr
from ppgnss import gnss_utils
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset, random_split
import xarray as xr
import matplotlib.pyplot as plt


import numpy as np
import torch

class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, delta=0, path='checkpoint.pt', trace_func=print):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
            path (str): Path for the checkpoint to be saved to.
                            Default: 'checkpoint.pt'
            trace_func (function): trace print function.
                            Default: print            
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.inf
        self.delta = delta
        self.path = path
        self.trace_func = trace_func

    def __call__(self, val_loss, model):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            self.trace_func(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        '''Saves model when validation loss decrease.'''
        if self.verbose:
            self.trace_func(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss
        
        
# 自定义数据集类
class DualInputDataset(Dataset):
    def __init__(self, iri_data, cosmic_data, label_data):
        """
        iri_data: xarray DataArray (time, lat, lon)
        cosmic_data: xarray DataArray (time, lat, lon, channel)
        label_data: xarray DataArray (time, lat, lon)
        """
        # 转换为numpy数组并调整维度顺序
        self.iri = iri_data.values[:, np.newaxis, :, :]  # 增加通道维度 -> (815, 1, 40, 72)
        self.cosmic = np.transpose(cosmic_data.values, (0, 3, 1, 2))  # (815, 4, 40, 72)
        self.labels = label_data.values[:, np.newaxis, :, :]  # (815, 1, 40, 72)
        
        # 转换为float32类型
        self.iri = self.iri.astype(np.float32)
        self.cosmic = self.cosmic.astype(np.float32)
        self.labels = self.labels.astype(np.float32)
        
    def __len__(self):
        return len(self.iri)
    
    def __getitem__(self, idx):
        return (self.iri[idx], self.cosmic[idx]), self.labels[idx]

# 双分支CNN模型
class DualBranchCNN(nn.Module):
    def __init__(self, channels=4):
        super(DualBranchCNN, self).__init__()
        self.channels = channels
        # IRI分支 (单通道输入)
        self.iri_branch = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        )
        
        # COSMIC分支 (多通道输入)
        self.cosmic_branch = nn.Sequential(
            nn.Conv2d(self.channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        )
        
        # 合并分支
        self.merge_branch = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 1, kernel_size=1)  # 输出单通道
        )
        
        self.upsample = nn.Upsample(size=(41, 73), mode='bilinear', align_corners=True)

        
    def forward(self, inputs):
        iri, cosmic = inputs
        
        # 处理两个分支
        iri_out = self.iri_branch(iri)
        cosmic_out = self.cosmic_branch(cosmic)
        
        # 合并特征
        combined = torch.cat((iri_out, cosmic_out), dim=1)
        
        # 最终输出
        output = self.merge_branch(combined)
        output = self.upsample(output)
        return output

# 主函数
def main():
    channels = 5
    key = f"{channels}ch"
    # trainning = False
    trainning = True

    current_dir = os.path.dirname(os.path.abspath(__file__))  # 脚本目录
    root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))  # 项目根目录
    # codg_filename = os.path.join(root_dir, "data", "codg2022_034.obj")
    # iri_filename = os.path.join(root_dir, "data", "i202022_2023.obj")
    # cosmic_grids_file = os.path.join(root_dir, "data", f"cosmic_grid_{key}_2022_034.obj")

    # ----------- 使用2019-2024完整数据 ----------------
    # cosmic数据
    cosmic_grids_file = os.path.join(root_dir, "data", f"cosmic_grid_{key}_2019to2024.obj")
    xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

    print("xr_cosmic:\n",xr_cosmic)

    # 构造 IRI 数据路径列表
    iri_folder = '/mnt/geodata/GIM/IRI2020'
    iri_filenames = [
        os.path.join(iri_folder, fname)
        for fname in [
            "i202019_2020.obj",
            "i202020_2021.obj",
            "i202021_2022.obj",
            "i202022_2023.obj",
            "i202023_2024.obj",
            "i202024_2025.obj",
        ]
    ]
    # 读取并合并 IRI 数据
    xr_iri_list = [gnss_utils.loadobject(fname) for fname in iri_filenames]
    xr_iri = xr.concat(xr_iri_list, dim="time")  # 假设时间是共享维度
    # xr_iri = xr_iri.sortby("time")  # 排序，防止打乱

    print("xr_iri:\n",xr_iri)


    # 构造 CODE 文件路径列表
    codg_folder ='/mnt/geodata/GIM/CODG_1ch'
    codg_filenames = [
        os.path.join(codg_folder, fname)
        for fname in [
            "CODG2019.obj",
            "CODG2020.obj",
            "CODG2021.obj", 
            "CODG2022.obj",
            "CODG2023.obj",
            # "CODG2024.obj"           # 没有2024年的codg
        ]
    ]
    extra_file_2024 = '/home/yxlei/cosmic2gim/data/codg_gim/CODG_2024_2025.obj'
    # 加入2024额外文件
    codg_filenames.append(extra_file_2024)

    # 读取并合并 CODE 数据
    xr_codg_list = [gnss_utils.loadobject(fname) for fname in codg_filenames]
    xr_codg = xr.concat(xr_codg_list, dim="time")  # 使用实际的时间维度名
    # xr_codg = xr_codg.sortby("time")

    print("xr_codg:\n",xr_codg)
    
    # 可选：检查时间范围
    print(f"xr_codg 时段范围: {str(xr_codg.time[0].values)} 至 {str(xr_codg.time[-1].values)}")
    

    xr_cosmic, xr_iri, xr_codg = xr.align(xr_cosmic, xr_iri, xr_codg, join="inner")

    print("xr_cosmic:\n",xr_cosmic)
    print("xr_iri:\n",xr_iri)
    print("xr_codg:\n",xr_codg)


    # 创建数据集
    # 时间段设定
    time_from_train = "2019-10-01T00:00:00"
    time_to_train   = "2023-12-31T23:00:00"
    time_from_test  = "2024-01-01T00:00:00"
    time_to_test    = "2024-12-31T23:00:00"

    

    # 将数据按时间筛选为训练/测试部分
    xr_cosmic_train = xr_cosmic.sel(time=slice(time_from_train, time_to_train))
    xr_iri_train    = xr_iri.sel(time=slice(time_from_train, time_to_train))
    xr_codg_train   = xr_codg.sel(time=slice(time_from_train, time_to_train))

    xr_cosmic_test = xr_cosmic.sel(time=slice(time_from_test, time_to_test))
    xr_iri_test    = xr_iri.sel(time=slice(time_from_test, time_to_test))
    xr_codg_test   = xr_codg.sel(time=slice(time_from_test, time_to_test))


    def print_time_range(name, ds):
        print(f"{name} time range: {str(ds.time.values[0])} ~ {str(ds.time.values[-1])}, 共 {len(ds.time)} 条")

    print_time_range("xr_cosmic_train", xr_cosmic_train)
    print_time_range("xr_iri_train", xr_iri_train)
    print_time_range("xr_codg_train", xr_codg_train)

    print_time_range("xr_cosmic_test", xr_cosmic_test)
    print_time_range("xr_iri_test", xr_iri_test)
    print_time_range("xr_codg_test", xr_codg_test)


    # 获取所有训练样本的时间索引（确保时间是 sorted 的）
    time_train = xr_cosmic_train.time.values
    time_train_sorted = sorted(time_train)

    # 构造完整训练+验证数据集
    full_trainval_dataset = DualInputDataset(xr_iri_train, xr_cosmic_train, xr_codg_train)

    # 按 8:2 比例划分
    total_size = len(full_trainval_dataset)
    train_size = int(total_size * 0.8)
    val_size   = total_size - train_size

    train_dataset, val_dataset = random_split(full_trainval_dataset, [train_size, val_size])

    test_dataset  = DualInputDataset(xr_iri_test, xr_cosmic_test, xr_codg_test)

        
    # dataset = DualInputDataset(xr_iri, xr_cosmic, xr_codg)

    # # 查看数据集长度
    # print(dataset[0])
    # # 查看第一个样本的结构和数据形状
    # (iri, cosmic), label = dataset[0]
    # print("IRI shape:", iri.shape)
    # print("COSMIC shape:", cosmic.shape)
    # print("Label shape:", label.shape)


    
    # # 划分数据集 (70%训练, 15%验证, 15%测试)
    # total_size = len(dataset)
    # train_size = int(0.7 * total_size)
    # val_size = int(0.15 * total_size)
    # test_size = total_size - train_size - val_size
    
    # train_dataset, val_dataset, test_dataset = random_split(
    #     dataset, [train_size, val_size, test_size]
    # )

   







    
    # 创建数据加载器
    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)
    
    # 初始化模型、损失函数和优化器
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device('cpu')

    model = DualBranchCNN(channels).to(device)
    criterion = nn.MSELoss()  # 回归任务使用MSE损失
    
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5)
    
    # early_stopping = EarlyStopping(patience=10, verbose=True, path=f'{key}_checkpoint.pt')
    # 修改保存路径为 scripts/test_bylyx/   6.14
    save_dir = "scripts/test_bylyx/train_save"
    os.makedirs(save_dir, exist_ok=True)

    checkpoint_path = os.path.join(save_dir, f"{key}_checkpoint.pt")
    best_model_path = os.path.join(save_dir, f"{key}_best_model.pth")
    early_stopping = EarlyStopping(patience=10, verbose=True, path=checkpoint_path)
    # 6.14

    if trainning:
        # 训练循环
        num_epochs = 200
        best_val_loss = float('inf')
        
        for epoch in range(num_epochs):
            # 训练阶段
            model.train()
            train_loss = 0.0
            for (iri_inputs, cosmic_inputs), labels in train_loader:
                iri_inputs = iri_inputs.to(device)
                cosmic_inputs = cosmic_inputs.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad()
                outputs = model((iri_inputs, cosmic_inputs))
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item() * iri_inputs.size(0)
            
            # 验证阶段
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for (iri_inputs, cosmic_inputs), labels in val_loader:
                    iri_inputs = iri_inputs.to(device)
                    cosmic_inputs = cosmic_inputs.to(device)
                    labels = labels.to(device)
                    
                    outputs = model((iri_inputs, cosmic_inputs))
                    loss = criterion(outputs, labels)
                    val_loss += loss.item() * iri_inputs.size(0)
            
            # 计算平均损失
            train_loss /= len(train_loader.dataset)
            val_loss /= len(val_loader.dataset)
            
            # 学习率调整
            scheduler.step(val_loss)
            
            # 保存最佳模型
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(model.state_dict(), best_model_path)
                 # torch.save(model.state_dict(), f'{key}_best_model.pth')             


            print(f'Epoch {epoch+1}/{num_epochs}: '
                f'Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}')
            
            early_stopping(val_loss, model)
            if early_stopping.early_stop:
                print("Early stopping")
                break
            
    else:
        # 加载最佳模型进行测试  
        # model.load_state_dict(torch.load(f'{key}_best_model.pth'))
        model.load_state_dict(torch.load(best_model_path))

        model.eval()
        test_loss = 0.0
        predictions = []
        actuals = []
        ind = 0
        # 全球范围：180度（纬度）x 360度（经度）
        lat = np.linspace(-50, 50, 41)    # 41个点，范围-45至45°，2.5°间隔
        lon = np.linspace(-180, 180, 73)   # 73个点，范围-180至180°，5°间隔
        lon_grid, lat_grid = np.meshgrid(lon, lat)

        with torch.no_grad():
            for (iri_inputs, cosmic_inputs), labels in test_loader:
                iri_inputs = iri_inputs.to(device)
                cosmic_inputs = cosmic_inputs.to(device)
                labels = labels.to(device)
                
                outputs = model((iri_inputs, cosmic_inputs))
                loss = criterion(outputs, labels)
                test_loss += loss.item() * iri_inputs.size(0)
                
                # for ind_j in range(32):  #报错：index 27 is out of bounds for dimension 0 with size 27
                for ind_j in range(labels.size(0)):
                    delta = labels[ind_j, 0, :, :].cpu().numpy() - outputs[ind_j, 0, :, :].cpu().numpy()
                    iri_delta = labels[ind_j, 0, :, :].cpu().numpy() - iri_inputs[ind_j, 0, :, :].cpu().numpy()
                    rms = np.sqrt(np.mean(delta**2))
                    rms_iri = np.sqrt(np.mean(iri_delta**2))
                    fig = plt.figure(figsize=(10, 10))
                    ax = fig.add_subplot(4, 1, 1, projection=ccrs.PlateCarree())
                    ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())
                    ax.coastlines(resolution='10m', color='black', linewidth=0.5)
                    im = ax.pcolor(lon, lat, iri_inputs[ind_j, 0, :, :].cpu().numpy(), cmap="jet", vmin=0, vmax=100, transform=ccrs.PlateCarree())
                    plt.colorbar(im)
                    ax.set_title("IRI")
                    
                    ax = fig.add_subplot(4, 1, 2, projection=ccrs.PlateCarree())
                    ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())
                    ax.coastlines(resolution='10m', color='black', linewidth=0.5)
                    im = ax.pcolor(lon, lat, outputs[ind_j, 0, :, :].cpu().numpy(), cmap="jet", vmin=0, vmax=100, transform=ccrs.PlateCarree())
                    plt.colorbar(im)
                    ax.set_title("NEW")
                    
                    ax = fig.add_subplot(4, 1, 3, projection=ccrs.PlateCarree())
                    ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())
                    ax.coastlines(resolution='10m', color='black', linewidth=0.5)
                    im = ax.pcolor(lon, lat, labels[ind_j, 0, :, :].cpu().numpy(), cmap="jet", vmin=0, vmax=100, transform=ccrs.PlateCarree())
                    plt.colorbar(im)
                    ax.set_title("CODE")
                    
                    ax = fig.add_subplot(4, 1, 4, projection=ccrs.PlateCarree())
                    ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())
                    ax.coastlines(resolution='10m', color='black', linewidth=0.5)
                    im = ax.pcolor(lon, lat, delta, cmap="coolwarm", vmin=-20, vmax=20, transform=ccrs.PlateCarree())
                    plt.colorbar(im)
                    # fig_filename = os.path.join(current_dir, "..", "figures", f"{key}_{ind:02d}_{ind_j:02d}.png")
                    fig_filename = os.path.join(save_dir, "figures",f"{key}_{ind:02d}_{ind_j:02d}.png")

                    plt.title(f"NEW: {rms:.1f} TECU, IRI: {rms_iri:.1f} TECU")
                    plt.savefig(fig_filename)
                    plt.close()
                ind += 1
                # 保存结果用于后续分析
                predictions.append(outputs.cpu().numpy())
                actuals.append(labels.cpu().numpy())
        
        test_loss /= len(test_loader.dataset)
        print(f'Test Loss: {test_loss:.6f}')
        
        # 合并所有测试结果
        predictions = np.concatenate(predictions, axis=0)
        actuals = np.concatenate(actuals, axis=0)
    
    # 可选：保存预测结果
    # np.save('predictions.npy', predictions)
    # np.save('actuals.npy', actuals)

    np.save(os.path.join(save_dir, 'predictions.npy'), np.concatenate(predictions, axis=0))
    np.save(os.path.join(save_dir, 'actuals.npy'), np.concatenate(actuals, axis=0))

if __name__ == "__main__":
    main()