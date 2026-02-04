# 音频卡顿分析工具 - 打包版本

## 项目简介

这是一个用于从数据包中提取音频并进行卡顿分析的工具，可以将网络数据包（pcap格式）中的音频流提取并转换为wav格式文件，同时提供音频卡顿分析功能。

## 打包内容

- 源代码（所有模块）
- 配置文件
- 打包脚本
- 依赖管理文件
- 图标文件

## 打包步骤

### 方法一：使用批处理脚本（推荐）

1. 双击运行 `build_project.bat` 文件
2. 等待自动安装依赖和打包完成
3. 可执行文件将位于 `dist/frame_to_wav_run/` 目录下

### 方法二：手动打包

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 执行打包：
   ```bash
   pyinstaller -D frame_to_wav_run.spec
   ```

## 生成的文件

- 主程序：`frame_to_wav_run.exe`
- 配置文件：`get_data/base/myconfig.yml`
- 所有必需的依赖库和资源文件

## 使用说明

1. 运行生成的 `frame_to_wav_run.exe` 文件
2. 在界面上配置相关参数（IP地址、端口等）
3. 选择需要分析的pcap文件
4. 开始提取音频并进行卡顿分析

## 环境要求

- Windows操作系统
- Python 3.7+（开发环境）
- 打包后的程序可在无Python环境的Windows系统上运行

## 项目结构

- `gui/` - 图形界面模块
- `services/` - 核心服务（音频转换、数据解码）
- `analysis/` - 通信数据分析
- `utils/` - 工具类集合
- `business/` - 业务逻辑初始化
- `packet/` - 报文处理工具