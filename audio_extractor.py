"""音频提取模块 - 使用ffmpeg从视频中提取音频"""
import os
import sys
from pathlib import Path


def extract_audio(video_path, output_dir="output/audios", keep_video=True):
    """
    从视频文件提取音频

    Args:
        video_path: 视频文件路径
        output_dir: 音频输出目录
        keep_video: 是否保留原视频文件

    Returns:
        提取的音频文件路径，失败返回None
    """
    try:
        import ffmpeg
    except ImportError:
        print("错误：未安装ffmpeg-python，请运行: pip install ffmpeg-python")
        return None

    if not os.path.exists(video_path):
        print(f"错误：视频文件不存在 {video_path}")
        return None

    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 生成音频文件路径
    video_name = Path(video_path).stem
    audio_path = os.path.join(output_dir, f"{video_name}.wav")

    try:
        print(f"正在提取音频: {video_path}")

        # 使用ffmpeg提取音频，转换为16kHz WAV格式（Whisper要求）
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ac=1, ar='16k')
        ffmpeg.run(stream, overwrite_output=True, quiet=True)

        if os.path.exists(audio_path):
            print(f"音频提取成功: {audio_path}")

            # 删除原视频文件（如果不需要保留）
            if not keep_video:
                os.remove(video_path)
                print(f"已删除原视频: {video_path}")

            return audio_path
        else:
            print(f"错误：音频文件未生成 {audio_path}")
            return None

    except ffmpeg.Error as e:
        print(f"FFmpeg错误: {e.stderr.decode() if e.stderr else str(e)}")
        return None
    except Exception as e:
        print(f"提取失败: {str(e)}")
        return None


def extract_audios_batch(video_paths, output_dir="output/audios", keep_video=True):
    """
    批量提取音频

    Args:
        video_paths: 视频文件路径列表
        output_dir: 音频输出目录
        keep_video: 是否保留原视频文件

    Returns:
        成功提取的音频文件路径列表
    """
    audio_files = []

    for i, video_path in enumerate(video_paths, 1):
        print(f"\n[{i}/{len(video_paths)}] 处理: {video_path}")
        audio_path = extract_audio(video_path, output_dir, keep_video)
        if audio_path:
            audio_files.append(audio_path)

    print(f"\n完成：成功提取 {len(audio_files)}/{len(video_paths)} 个音频")
    return audio_files


if __name__ == "__main__":
    # 测试代码示例
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        extract_audio(video_path)
    else:
        print("用法: python audio_extractor.py <视频文件路径>")
        print("示例: python audio_extractor.py video.mp4")
