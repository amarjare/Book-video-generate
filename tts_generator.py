import os
import asyncio
from typing import Optional
import edge_tts


voice_dict = {
    "晓通-女": "wuu-CN-XiaotongNeural",
    "云哲(吴语)-男": "wuu-CN-YunzheNeural",
    "晓敏-女": "yue-CN-XiaoMinNeural",
    "云松-男": "yue-CN-YunSongNeural",
    "晓辰(多语言)-女": "zh-CN-XiaochenMultilingualNeural",
    "晓辰(标准)-女": "zh-CN-XiaochenNeural",
    "晓涵-女": "zh-CN-XiaohanNeural",
    "晓梦-女": "zh-CN-XiaomengNeural",
    "晓默-女": "zh-CN-XiaomoNeural",
    "晓秋-女": "zh-CN-XiaoqiuNeural",
    "晓柔-女": "zh-CN-XiaorouNeural",
    "晓瑞-女": "zh-CN-XiaoruiNeural",
    "晓爽-女": "zh-CN-XiaoshuangNeural",
    "晓晓(方言)-女": "zh-CN-XiaoxiaoDialectsNeural",
    "晓晓(多语言)-女": "zh-CN-XiaoxiaoMultilingualNeural",
    "晓晓(标准)-女": "zh-CN-XiaoxiaoNeural",
    "晓燕-女": "zh-CN-XiaoyanNeural",
    "晓怡-女": "zh-CN-XiaoyiNeural",
    "晓优-女": "zh-CN-XiaoyouNeural",
    "晓语(多语言)-女": "zh-CN-XiaoyuMultilingualNeural",
    "晓真-女": "zh-CN-XiaozhenNeural",
    "云峰-男": "zh-CN-YunfengNeural",
    "云浩-男": "zh-CN-YunhaoNeural",
    "云健-男": "zh-CN-YunjianNeural",
    "云杰-男": "zh-CN-YunjieNeural",
    "云熙(标准)-男": "zh-CN-YunxiNeural",
    "云夏-男": "zh-CN-YunxiaNeural",
    "云晓-男": "zh-CN-YunxiaoMultilingualNeural",
    "云阳-男": "zh-CN-YunyangNeural",
    "云野-男": "zh-CN-YunyeNeural",
    "云逸-男": "zh-CN-YunyiMultilingualNeural",
    "云泽-男": "zh-CN-YunzeNeural",
    "云登-男": "zh-CN-henan-YundengNeural",
    "晓北-女": "zh-CN-liaoning-XiaobeiNeural",
    "晓妮-女": "zh-CN-shaanxi-XiaoniNeural",
    "云翔-男": "zh-CN-shandong-YunxiangNeural",
    "云熙(四川)-男": "zh-CN-sichuan-YunxiNeural",
    "晓佳-女": "zh-HK-HiuGaaiNeural",
    "晓文-女": "zh-HK-HiuMaanNeural",
    "云龙-男": "zh-HK-WanLungNeural",
    "晓辰(台湾)-女": "zh-TW-HsiaoChenNeural",
    "晓语(台湾)-女": "zh-TW-HsiaoYuNeural",
    "云哲(台湾)-男": "zh-TW-YunJheNeural"
}

def getVoiceById(voiceId: str) -> Optional[str]:
    return voiceMap.get(voiceId)


async def _generate_audio_and_subtitles(
    text: str, 
    voice: str, 
    file_path: str, 
    rate: Optional[str] = None, 
    volume: Optional[str] = None, 
    pitch: Optional[str] = None, 
    generate_subtitles: bool = False) -> Optional[str]:
    """异步生成音频文件和字幕文件"""
    # 根据edge-tts文档，使用rate, volume, pitch参数而不是自定义SSML
    # 只传递非None的参数
    kwargs = {}
    if rate is not None:
        kwargs['rate'] = rate
    if volume is not None:
        kwargs['volume'] = volume
    if pitch is not None:
        kwargs['pitch'] = pitch
    
    communicate = edge_tts.Communicate(text, voice, **kwargs)
    
    submaker = edge_tts.SubMaker()
    # 生成音频
    with open(file_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif generate_subtitles and chunk["type"] in ["SentenceBoundary", "WordBoundary"]:
                submaker.feed(chunk)
    
    # 生成字幕文件
    subtitle_path = file_path.replace('.mp3', '.srt')
    with open(subtitle_path, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())
    
    return None

def createAudio(
    text: str, 
    file_name: str, 
    voice: str, 
    rate: Optional[str] = None, 
    volume: Optional[str] = None, 
    pitch: Optional[str] = None, 
    generate_subtitles: bool = False) -> str:

    print(f"Text without html tags: {text}")

    pwdPath = os.getcwd()
    # 本地路径
    filePath = os.path.join(pwdPath, "tts", file_name)
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    
    # 使用edge_tts模块生成音频
    try:
        subtitle_path = asyncio.run(_generate_audio_and_subtitles(text, voice, filePath, rate, volume, pitch, generate_subtitles))
        if subtitle_path:
            print(f"字幕文件已生成: {subtitle_path}")
    except Exception as e:
        print(f"生成音频时出错: {e}")
        return "error generating audio"
    
    # 返回本地文件路径
    return filePath


# 示例用法
if __name__ == "__main__":
    # 测试TTS功能
    text = """
你好，我是山东人
"""
    file_name = "test.mp3"
    voice_id = "晓秋-女"
    voice = voice_dict.get(voice_id)

    # 测试带字幕的语音
    result2 = createAudio(text, "test_with_subtitles.mp3", voice, generate_subtitles=True)
    print(f"带字幕的语音文件已生成: {result2}")