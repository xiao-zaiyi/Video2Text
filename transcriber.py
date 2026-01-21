"""语音转文字模块 - 使用OpenAI Whisper进行语音识别"""
import os
import sys
from pathlib import Path
from datetime import datetime


def transcribe(audio_path, model_size="base", language="zh", output_dir="output/texts"):
    """
    将音频转换为文字

    Args:
        audio_path: 音频文件路径
        model_size: Whisper模型大小 (tiny/base/small/medium/large)
        language: 语言代码 (zh=中文, en=英文)
        output_dir: 文本输出目录

    Returns:
        包含文本内容和元数据的字典，失败返回None
    """
    try:
        import whisper
    except ImportError:
        print("错误：未安装openai-whisper，请运行: pip install openai-whisper")
        return None

    if not os.path.exists(audio_path):
        print(f"错误：音频文件不存在 {audio_path}")
        return None

    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        print(f"正在加载Whisper模型: {model_size}")
        model = whisper.load_model(model_size)

        print(f"正在转录音频: {audio_path}")
        result = model.transcribe(audio_path, language=language, verbose=False)

        # 提取结果
        text = result["text"].strip()
        segments = result.get("segments", [])

        # 生成时间轴
        timeline = []
        for seg in segments:
            start_time = format_timestamp(seg["start"])
            end_time = format_timestamp(seg["end"])
            segment_text = seg["text"].strip()
            timeline.append(f"{start_time} - {end_time}: {segment_text}")

        # 生成输出文件名
        audio_name = Path(audio_path).stem
        text_path = os.path.join(output_dir, f"{audio_name}.txt")
        md_path = os.path.join(output_dir, f"{audio_name}.md")

        # 保存纯文本
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"文本已保存: {text_path}")

        # 返回结果
        return {
            "text": text,
            "timeline": timeline,
            "audio_path": audio_path,
            "text_path": text_path,
            "md_path": md_path,
            "language": result.get("language", language),
            "duration": segments[-1]["end"] if segments else 0
        }

    except Exception as e:
        print(f"转录失败: {str(e)}")
        return None


def format_timestamp(seconds):
    """将秒数转换为 HH:MM:SS 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def save_markdown(result, video_url="", video_title=""):
    """
    将转录结果保存为Markdown格式

    Args:
        result: transcribe()返回的结果字典
        video_url: 视频来源URL
        video_title: 视频标题

    Returns:
        Markdown文件路径
    """
    if not result:
        return None

    md_path = result["md_path"]
    text = result["text"]
    timeline = result["timeline"]
    duration = result["duration"]
    language = result["language"]

    # 生成Markdown内容
    md_content = f"""# {video_title if video_title else "视频转录"}

**来源**: {video_url if video_url else "本地文件"}
**时长**: {format_timestamp(duration)}
**语言**: {language}
**转录时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 内容

{text}

---

## 时间轴

"""

    # 添加时间轴
    for line in timeline:
        md_content += f"- {line}\n"

    # 保存Markdown文件
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Markdown已保存: {md_path}")
    return md_path


def transcribe_batch(audio_paths, model_size="base", language="zh", output_dir="output/texts"):
    """
    批量转录音频

    Args:
        audio_paths: 音频文件路径列表
        model_size: Whisper模型大小
        language: 语言代码
        output_dir: 文本输出目录

    Returns:
        转录结果列表
    """
    results = []

    for i, audio_path in enumerate(audio_paths, 1):
        print(f"\n[{i}/{len(audio_paths)}] 处理: {audio_path}")
        result = transcribe(audio_path, model_size, language, output_dir)
        if result:
            results.append(result)
            save_markdown(result)

    print(f"\n完成：成功转录 {len(results)}/{len(audio_paths)} 个音频")
    return results


if __name__ == "__main__":
    # 测试代码示例
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
        result = transcribe(audio_path, model_size)
        if result:
            save_markdown(result)
    else:
        print("用法: python transcriber.py <音频文件路径> [模型大小]")
        print("示例: python transcriber.py audio.wav base")
