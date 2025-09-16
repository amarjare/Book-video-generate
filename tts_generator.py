import os
import re
import asyncio
from edge_tts import Communicate

voiceMap = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "yunjian": "zh-CN-YunjianNeural",
    "yunxi": "zh-CN-YunxiNeural",
    "yunxia": "zh-CN-YunxiaNeural",
    "yunyang": "zh-CN-YunyangNeural",
    "xiaoqiu": "zh-CN-XiaoqiuNeural",
    "xiaobei": "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}


def getVoiceById(voiceId):
    return voiceMap.get(voiceId)


# 删除html标签
def remove_html(string):
    regex = re.compile(r'<[^>]+>')
    return regex.sub('', string)


async def _generate_audio_and_subtitles(text, voice, file_path, rate=None, volume=None, pitch=None, generate_subtitles=False):
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
    
    communicate = Communicate(text, voice, **kwargs)
    
    subtitles = []
    with open(file_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif generate_subtitles and chunk["type"] in ["SentenceBoundary", "WordBoundary"]:
                subtitles.append(chunk)
    
    # 生成字幕文件
    if generate_subtitles and subtitles:
        subtitle_path = file_path.replace('.mp3', '.srt')
        _generate_srt_file(subtitles, subtitle_path)
        return subtitle_path
    
    return None

def _generate_srt_file(subtitles, subtitle_path):
    """生成SRT字幕文件"""
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        for i, subtitle in enumerate(subtitles, 1):
            if subtitle['type'] == 'SentenceBoundary':
                # 将微秒转换为SRT时间格式
                start_time = _microseconds_to_srt_time(subtitle['offset'])
                end_time = _microseconds_to_srt_time(subtitle['offset'] + subtitle['duration'])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{subtitle['text']}\n\n")

def _microseconds_to_srt_time(microseconds):
    """将微秒转换为SRT时间格式 (HH:MM:SS,mmm)"""
    total_seconds = microseconds / 10000000  # 转换为秒
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def createAudio(text, file_name, voiceId, rate=None, volume=None, pitch=None, generate_subtitles=False):
    new_text = remove_html(text)
    print(f"Text without html tags: {new_text}")
    voice = getVoiceById(voiceId)
    if not voice:
        return "error params"

    pwdPath = os.getcwd()
    # 本地路径
    filePath = os.path.join(pwdPath, "tts", file_name)
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    
    # 使用edge_tts模块生成音频
    try:
        subtitle_path = asyncio.run(_generate_audio_and_subtitles(new_text, voice, filePath, rate, volume, pitch, generate_subtitles))
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
    text = """今天分享的是
巴别塔

语言即权力，亦是牢笼
我们靠翻译彼此靠近
也在翻译中背叛彼此

银条刻下异邦的词汇
便能窃取神的力量，维系帝国
高塔之下，是无声的掠夺与牺牲

我们在此迷失，也在此寻找归途
巴别塔，是奇迹，也是诅咒"""
    file_name = "test.mp3"
    voice_id = "xiaoqiu"
    
    # 测试普通语音
    # result1 = createAudio(text, "test_normal.mp3", voice_id)
    # print(f"普通语音文件已生成: {result1}")
    
    # 测试带字幕的语音
    result2 = createAudio(text, "test_with_subtitles.mp3", voice_id, generate_subtitles=True)
    print(f"带字幕的语音文件已生成: {result2}")