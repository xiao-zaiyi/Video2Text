<div align="center">

# 🎬 Video2Text

**简单高效的视频转文本工具**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenAI Whisper](https://img.shields.io/badge/Whisper-OpenAI-orange.svg)](https://github.com/openai/whisper)

[功能特点](#功能特点) • [快速开始](#快速开始) • [使用方法](#使用方法) • [常见问题](#常见问题)

</div>

---

## 📖 简介

Video2Text 是一个基于 OpenAI Whisper 的视频转文本工具，可以将视频中的语音内容自动转录为文字。

**核心特点**：
- 🚀 **简单易用** - 零配置，开箱即用
- 🎯 **高准确率** - 基于 OpenAI Whisper，中文识别准确率高
- 📝 **多格式输出** - 支持纯文本和 Markdown 格式，包含时间轴
- ⚡ **批量处理** - 支持批量处理多个视频文件
- 🔧 **灵活配置** - 支持多种模型大小和语言

## ✨ 功能特点

- ✅ 从视频中提取音频（基于 ffmpeg）
- ✅ 高准确率的语音识别（基于 OpenAI Whisper）
- ✅ 生成纯文本和 Markdown 格式
- ✅ 自动生成时间轴
- ✅ 支持批量处理
- ✅ 支持多种视频格式（mp4, avi, mov, mkv, flv, wmv, webm）
- ✅ 支持多种语言（中文、英文等 99 种语言）

## 🚀 快速开始

### 系统要求

- Python 3.8+
- ffmpeg

### 安装 ffmpeg

**Windows**:
```bash
# 使用 Chocolatey
choco install ffmpeg

# 或从官网下载: https://ffmpeg.org/download.html
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/你的用户名/Video2Text.git
cd Video2Text

# 安装 Python 依赖
pip install -r requirements.txt
```

**注意**：首次运行时，Whisper 会自动下载模型文件（base 模型约 140MB），需要联网。

## 📚 使用方法

### 方法一：使用 main.py（推荐新手）

1. 打开 `main.py`，修改配置：

```python
# 视频文件路径
VIDEO_PATH = r"video.mp4"  # 修改为你的视频路径

# Whisper 模型大小
MODEL_SIZE = "base"  # tiny, base, small, medium, large

# 语言
LANGUAGE = "zh"  # zh(中文), en(英文)
```

2. 运行：

```bash
python main.py
```

### 方法二：使用 video2text.py（命令行）

```bash
# 处理单个视频
python video2text.py video.mp4

# 批量处理目录
python video2text.py videos/

# 使用更大的模型
python video2text.py video.mp4 --model medium

# 处理英文视频
python video2text.py video.mp4 --language en

# 处理后删除视频文件（节省空间）
python video2text.py video.mp4 --no-keep-video
```

### 方法三：单独使用模块

```bash
# 只提取音频
python audio_extractor.py video.mp4

# 只转录音频
python transcriber.py audio.wav base
```

## 📊 Whisper 模型选择

| 模型 | 速度 | 准确率 | 内存占用 | 适用场景 |
|------|------|--------|----------|----------|
| tiny | 最快 | 较低 | ~1GB | 快速预览 |
| base | 快 | 中等 | ~1GB | **日常使用（推荐）** |
| small | 中等 | 较高 | ~2GB | 重要内容 |
| medium | 慢 | 高 | ~5GB | 专业转录 |
| large | 很慢 | 最高 | ~10GB | 最高质量要求 |

**建议**：
- CPU 用户：使用 `base` 或 `small` 模型
- GPU 用户：可以使用 `medium` 或 `large` 模型

## 📁 输出文件

处理完成后，文件会保存在 `output` 目录：

```
output/
├── videos/          # 下载的视频文件
├── audios/          # 提取的音频文件（WAV 格式）
└── texts/           # 转录结果
    ├── xxxxx.txt    # 纯文本
    └── xxxxx.md     # Markdown 格式（包含时间轴）
```

### Markdown 输出示例

```markdown
# 视频标题

**来源**: video.mp4
**时长**: 03:42
**语言**: zh
**转录时间**: 2026-01-20 10:30:00

---

## 内容

[完整的转录文本内容...]

---

## 时间轴

- 00:00 - 00:15: 开场白内容
- 00:15 - 00:45: 主题介绍
- 00:45 - 01:20: 详细讲解
...
```

## ⚡ 性能参考

以 3 分钟视频为例（使用 base 模型，CPU 处理）：

- 提取音频：5 秒
- 语音转录：30-60 秒
- **总计**：约 35-65 秒

**GPU 加速**：如果有 NVIDIA GPU，Whisper 会自动使用 CUDA 加速，转录速度可提升 5-10 倍。

## 🔧 项目结构

```
Video2Text/
├── main.py                  # 简化版主程序（配置式）
├── video2text.py           # 完整版主程序（命令行）
├── audio_extractor.py      # 音频提取模块
├── transcriber.py          # 语音转文字模块
├── downloader.py           # 视频下载模块（可选）
├── requirements.txt        # 依赖列表
├── .gitignore             # Git 忽略文件
└── output/                # 输出目录
    ├── videos/
    ├── audios/
    └── texts/
```

## ❓ 常见问题

### 1. ffmpeg 错误

**问题**：提示找不到 ffmpeg

**解决**：
- 确保已安装 ffmpeg
- 检查 ffmpeg 是否在系统 PATH 中：`ffmpeg -version`
- Windows 用户可能需要重启终端

### 2. 转录速度慢

**问题**：转录速度很慢

**解决**：
- 使用更小的模型（`--model tiny`）
- 如果有 GPU，确保安装了 CUDA 版本的 PyTorch
- 考虑使用云 API（需要修改代码）

### 3. 中文识别不准确

**问题**：中文识别准确率低

**解决**：
- 使用更大的模型（`--model medium`）
- 确保指定了语言：`--language zh`
- 检查音频质量（背景噪音、音量）

### 4. 首次运行很慢

**问题**：首次运行需要很长时间

**解决**：
- 首次运行会下载 Whisper 模型（base 模型约 140MB）
- 需要联网，请耐心等待
- 模型下载后会缓存，后续运行会很快

## 🛠️ 技术栈

- **ffmpeg** - 音视频处理
- **OpenAI Whisper** - 语音识别（支持 99 种语言）
- **Python 3.8+** - 开发语言

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐

## 📮 联系方式

如有问题或建议，请提交 [Issue](https://github.com/你的用户名/Video2Text/issues)

---

<div align="center">

**[⬆ 回到顶部](#-video2text)**

Made with ❤️ by [你的名字]

</div>
