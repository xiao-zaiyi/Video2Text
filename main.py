"""
Video2Text - 超简化版
直接运行即可，所有配置在代码顶部修改
"""
import os
from pathlib import Path
from audio_extractor import extract_audio
from transcriber import transcribe, save_markdown

# ==================== 配置区域 ====================
# 修改这里的配置，然后直接运行

# 视频文件路径（单个文件）
VIDEO_PATH = r"video.mp4"  # 修改为你的视频路径

# 或者批量处理整个目录（留空则处理单个文件）
VIDEO_DIR = ""  # 例如: r"D:\videos"

# Whisper模型大小: tiny, base, small, medium, large
MODEL_SIZE = "base"

# 语言: zh(中文), en(英文)
LANGUAGE = "zh"

# 处理后是否保留视频文件
KEEP_VIDEO = True

# ==================================================


def main():
    print("=" * 60)
    print("Video2Text - 视频转文本工具")
    print("=" * 60)

    # 批量处理目录
    if VIDEO_DIR:
        video_files = []
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}

        for file in Path(VIDEO_DIR).iterdir():
            if file.is_file() and file.suffix.lower() in video_extensions:
                video_files.append(str(file))

        if not video_files:
            print(f"错误：在 {VIDEO_DIR} 中未找到视频文件")
            return

        print(f"\n找到 {len(video_files)} 个视频文件")
        success = 0

        for i, video_path in enumerate(video_files, 1):
            print(f"\n{'=' * 60}")
            print(f"[{i}/{len(video_files)}] {Path(video_path).name}")
            print(f"{'=' * 60}")

            if process_one(video_path):
                success += 1

        print(f"\n✅ 完成！成功处理 {success}/{len(video_files)} 个视频")
        print(f"📁 输出目录: output/texts/")

    # 处理单个文件
    else:
        if not os.path.isfile(VIDEO_PATH):
            print(f"错误：视频文件不存在 {VIDEO_PATH}")
            return

        process_one(VIDEO_PATH)


def process_one(video_path):
    """处理单个视频"""

    # 步骤1: 提取音频
    print(f"\n[1/2] 提取音频...")
    audio_path = extract_audio(video_path, keep_video=KEEP_VIDEO)
    if not audio_path:
        print("❌ 音频提取失败")
        return False

    # 步骤2: 转录
    print(f"\n[2/2] 语音转文字...")
    result = transcribe(audio_path, model_size=MODEL_SIZE, language=LANGUAGE)
    if not result:
        print("❌ 转录失败")
        return False

    # 保存Markdown
    video_name = Path(video_path).name
    md_path = save_markdown(result, video_title=video_name)

    # 输出结果
    print("\n" + "=" * 60)
    print("✅ 处理完成！")
    print("=" * 60)
    print(f"📄 文本: {result['text_path']}")
    print(f"📝 Markdown: {md_path}")
    print(f"🎵 音频: {audio_path}")

    # 显示预览
    print("\n内容预览:")
    print("-" * 60)
    preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
    print(preview)
    print("-" * 60)

    return True


if __name__ == "__main__":
    main()
