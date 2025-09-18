import subprocess
import os
from pathlib import Path
from typing import Optional

def merge_audio_video(
    video_path: Path,
    audio_path: Path,
    bgm_path: Path,
    effect_path: Optional[Path],
    output_path: Path,
    bgm_volume: float = 0.5,
    effect_volume: float = 0.8,
    effect_start_time: float = 1.0
) -> bool:
    """
    使用ffmpeg将视频与多个音频轨道合成
    
    Args:
        video_path: 输入视频文件路径
        audio_path: 配音文件路径
        bgm_path: 背景音乐文件路径
        effect_path: 音效文件路径（可选）
        output_path: 输出视频文件路径
        bgm_volume: 背景音乐音量（0.0-1.0）
        effect_volume: 音效音量（0.0-1.0）
        effect_start_time: 音效开始时间（秒）
    
    Returns:
        bool: 合成是否成功
    """
    try:
        # 检查输入文件是否存在
        if not video_path.exists():
            print(f"错误：视频文件不存在 {video_path}")
            return False
        if not audio_path.exists():
            print(f"错误：配音文件不存在 {audio_path}")
            return False
        if not bgm_path.exists():
            print(f"错误：背景音乐文件不存在 {bgm_path}")
            return False
        
        # 构建ffmpeg命令
        cmd = [
            'ffmpeg',
            '-y',  # 覆盖输出文件
            '-i', str(video_path),  # 输入视频
            '-i', str(audio_path),  # 输入配音
            '-i', str(bgm_path),    # 输入背景音乐
        ]
        
        # 如果有音效文件，添加到输入
        if effect_path and effect_path.exists():
            cmd.extend(['-i', str(effect_path)])
            
            # 复杂的音频混合滤镜（包含音效）
            filter_complex = (
                f"[1:a]volume=1.0[voice];"  # 配音音量
                f"[2:a]volume={bgm_volume}[bgm];"  # 背景音乐音量
                f"[3:a]volume={effect_volume},adelay={int(effect_start_time*1000)}|{int(effect_start_time*1000)}[effect];"  # 音效延迟和音量
                "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[mix1];"  # 混合配音和背景音乐
                "[mix1][effect]amix=inputs=2:duration=first:dropout_transition=2[final]"  # 添加音效
            )
            
            cmd.extend([
                '-filter_complex', filter_complex,
                '-map', '0:v',  # 使用原视频
                '-map', '[final]',  # 使用混合后的音频
            ])
        else:
            # 简单的音频混合滤镜（不包含音效）
            filter_complex = (
                f"[1:a]volume=1.0[voice];"  # 配音音量
                f"[2:a]volume={bgm_volume}[bgm];"  # 背景音乐音量
                "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[final]"  # 混合音频
            )
            
            cmd.extend([
                '-filter_complex', filter_complex,
                '-map', '0:v',  # 使用原视频
                '-map', '[final]',  # 使用混合后的音频
            ])
        
        # 输出设置
        cmd.extend([
            '-c:v', 'libx264',  # 视频编码器
            '-c:a', 'aac',      # 音频编码器
            '-b:a', '192k',     # 音频比特率
            '-shortest',        # 以最短的流为准
            str(output_path)    # 输出文件
        ])
        
        print("开始音视频合成...")
        print(f"命令: {' '.join(cmd)}")
        
        # 执行ffmpeg命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(f"音视频合成成功！输出文件：{output_path}")
            return True
        else:
            print(f"音视频合成失败！")
            print(f"错误信息：{result.stderr}")
            return False
            
    except FileNotFoundError:
        print("错误：未找到ffmpeg，请确保已安装ffmpeg并添加到系统PATH中")
        return False
    except Exception as e:
        print(f"音视频合成过程中发生错误：{str(e)}")
        return False

def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    # 测试代码
    if check_ffmpeg():
        print("ffmpeg 可用")
    else:
        print("ffmpeg 不可用，请安装ffmpeg")