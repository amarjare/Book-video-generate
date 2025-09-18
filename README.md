# 📚 Book Video Generator

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)

一个自动化书籍推广视频生成工具，可以根据书名自动生成带有配音和字幕的短视频。

## 🖼️ 效果预览

[示例视频](https://github.com/user-attachments/assets/385a804c-904a-4aae-a595-58f9240a66b9)


### 视频特性
生成的视频包含：
- 🎬 **动态封面展示效果** - 书籍封面滑动动画，4秒片头效果，书籍封面在`resource/covers/`中随机获取
- 🖼️ **背景图片自动切换** - 每10秒切换背景，营造氛围，背景图片随机从`resource/backgrounds/`中获取
- 📝 **同步字幕显示** - 根据音频时长精准同步，底部居中显示
- 🎵 **多音轨混合** - 配音 + 背景音乐 + 音效，音量自动平衡，背景音乐随机从`resource/bgm/`中获取

### 使用建议
1. **首次使用**: 建议先下载示例视频查看效果
2. **测试运行**: 使用简单的书籍名称进行测试
3. **参数调整**: 根据需要调整视频参数和语音选择

## 📋 系统要求

- **Python**: 3.7+
- **FFmpeg**: 必须安装并添加到系统PATH
- **操作系统**: Windows / macOS / Linux

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/SheenHalo/Book-video-generate.git
cd Book-video-generate
```

### 2. 创建虚拟环境

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 检查FFmpeg

项目依赖FFmpeg进行视频合成，请确保已正确安装：

```bash
python video_processor.py
```

如果显示"ffmpeg 可用"，则安装成功。如果显示"ffmpeg 不可用"，请按以下步骤安装：

#### Windows FFmpeg安装
1. 下载FFmpeg: https://ffmpeg.org/download.html
2. 解压到 `C:\ffmpeg`
3. 添加 `C:\ffmpeg\bin` 到系统PATH环境变量
4. 重启命令行并验证：`ffmpeg -version`

#### macOS FFmpeg安装
```bash
brew install ffmpeg
```

#### Linux FFmpeg安装
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL/Fedora
sudo yum install ffmpeg
```

### 5. 配置LLM API
提供了一个免费的LLM API接口。如果失效了，请自行配置。
编辑 `llm.py` 文件，配置你的LLM API信息：

```python
# 在LLMClient类中修改
self.api_url = "你的API地址"
self.api_key = "你的API密钥"
```

### 6. 准备资源文件

确保以下目录包含必要的文件：

```
resource/
├── backgrounds/    # 背景图片 (jpg/png)
├── bgm/           # 背景音乐 (mp3)
├── covers/        # 书籍封面存储位置
├── effects/       # 音效文件 (mp3)
└── fonts/         # 字体文件 (包含msyh.ttc)
```

### 7. 运行程序

```bash
python main.py
```

按照提示输入书名，程序将自动生成视频：

```
请输入书名: 巴别塔
正在获取书籍信息...
正在生成文案...
正在生成语音...
正在生成视频...
开始合成音视频...
最终视频已保存到: appdata/巴别塔/final_video.mp4
```

## 🛠️ 高级配置

### 修改语音类型

在 `main.py` 中修改语音选择：

```python
# 查看所有可用语音
print(voice_dict.keys())

# 选择特定语音
voice = voice_dict.get("晓秋-女")
```

### 自定义视频参数

在 `app.py` 的 `make_movie` 函数中可以调整：
- 屏幕尺寸
- 动画时长
- 音量大小
- 背景切换时间

### 支持的语音列表

项目支持43种中文语音变体：

| 语音名称 | 类型 | 特点 |
|---------|------|------|
| 晓晓（标准）-女 | 标准 | 温暖，全面，生动 |
| 晓辰（标准）-女 | 标准 | 友好，休闲，乐观 |
| 云峰-男 | 标准 | 自信，生动，情感 |
| 晓晓（多语言）-女 | 多语言 | 温暖，生动，明亮 |
| 晓通（吴语）-女 | 方言 | 温暖，友好，舒缓 |
| 晓敏（粤语）-女 | 方言 | 明亮，清晰，自信 |
| ...更多语音详见代码 | | |

## 📁 项目结构

```
Book-video-generate/
├── main.py              # 主入口文件
├── app.py               # 视频生成核心
├── spider.py            # 豆瓣爬虫
├── llm.py               # LLM客户端
├── tts_generator.py     # TTS生成器
├── video_processor.py   # 视频处理工具
├── requirements.txt     # 依赖列表
├── CLAUDE.md           # 开发文档
├── appdata/            # 生成的文件
└── resource/           # 资源文件
```

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

