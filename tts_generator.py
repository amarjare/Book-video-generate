import os
import asyncio
from typing import Optional, Dict
import edge_tts


voice_dict = {
    "晓通（吴语）-女": "wuu-CN-XiaotongNeural",
    "云哲（吴语）-男": "wuu-CN-YunzheNeural",
    "晓敏（粤语）-女": "yue-CN-XiaoMinNeural",
    "云松（粤语）-男": "yue-CN-YunSongNeural",
    "晓辰（多语言）-女": "zh-CN-XiaochenMultilingualNeural",
    "晓辰（标准）-女": "zh-CN-XiaochenNeural",
    "晓涵-女": "zh-CN-XiaohanNeural",
    "晓梦-女": "zh-CN-XiaomengNeural",
    "晓默-女": "zh-CN-XiaomoNeural",
    "晓秋-女": "zh-CN-XiaoqiuNeural",
    "晓柔-女": "zh-CN-XiaorouNeural",
    "晓瑞-女": "zh-CN-XiaoruiNeural",
    "晓爽-女": "zh-CN-XiaoshuangNeural",
    "晓晓（方言）-女": "zh-CN-XiaoxiaoDialectsNeural",
    "晓晓（多语言）-女": "zh-CN-XiaoxiaoMultilingualNeural",
    "晓晓（标准）-女": "zh-CN-XiaoxiaoNeural",
    "晓燕-女": "zh-CN-XiaoyanNeural",
    "晓怡-女": "zh-CN-XiaoyiNeural",
    "晓优-女": "zh-CN-XiaoyouNeural",
    "晓语（多语言）-女": "zh-CN-XiaoyuMultilingualNeural",
    "晓真-女": "zh-CN-XiaozhenNeural",
    "云峰-男": "zh-CN-YunfengNeural",
    "云浩-男": "zh-CN-YunhaoNeural",
    "云健-男": "zh-CN-YunjianNeural",
    "云杰-男": "zh-CN-YunjieNeural",
    "云熙（标准）-男": "zh-CN-YunxiNeural",
    "云夏-男": "zh-CN-YunxiaNeural",
    "云晓-男": "zh-CN-YunxiaoMultilingualNeural",
    "云阳-男": "zh-CN-YunyangNeural",
    "云野-男": "zh-CN-YunyeNeural",
    "云逸-男": "zh-CN-YunyiMultilingualNeural",
    "云泽-男": "zh-CN-YunzeNeural",
    "云登（河南）-男": "zh-CN-henan-YundengNeural",
    "晓北（辽宁）-女": "zh-CN-liaoning-XiaobeiNeural",
    "晓妮（陕西）-女": "zh-CN-shaanxi-XiaoniNeural",
    "云翔（山东）-男": "zh-CN-shandong-YunxiangNeural",
    "云熙（四川）-男": "zh-CN-sichuan-YunxiNeural",
    "晓佳（香港）-女": "zh-HK-HiuGaaiNeural",
    "晓文（香港）-女": "zh-HK-HiuMaanNeural",
    "云龙（香港）-男": "zh-HK-WanLungNeural",
    "晓辰（台湾）-女": "zh-TW-HsiaoChenNeural",
    "晓语（台湾）-女": "zh-TW-HsiaoYuNeural",
    "云哲（台湾）-男": "zh-TW-YunJheNeural"
}
voice_text = {
"晓通（吴语）-女": "好久没有拍视频了，今天拍个视频",
"云哲（吴语）-男": "先生们，女士们。大家好，阿拉现在来学习上海话",
"晓敏（粤语）-女": "雷猴，识得你我好荣幸。",
"云松（粤语）-男": "雷猴，识哒内鹅侯温很。",
"晓辰（多语言）-女": "Hello everyone, 我是晓辰，我支持多语言合成，希望能用更自然的声音陪伴你。",
"晓辰（标准）-女": "大家好，我是晓辰，我说标准的普通话，希望我的声音能给你带来清晰和愉悦。",
"晓涵-女": "大家好，我是晓涵，我的声音温柔细腻，希望能为你带来舒适的感受。",
"晓梦-女": "嗨～我是晓梦，我的声音活泼灵动，希望能为你的生活增添一抹甜意。",
"晓默-女": "你好，我是晓默，我的声音沉稳而柔和，适合讲述故事与情感。",
"晓秋-女": "大家好，我是晓秋，我的声音温和如玉，希望能陪伴你度过每一个安静的时刻。",
"晓柔-女": "你好呀，我是晓柔，我的声音轻柔似水，希望能为你带来一丝宁静。",
"晓瑞-女": "大家好，我是晓瑞，我的声音清亮悦耳，适合表达各种情感。",
"晓爽-女": "嗨，我是晓爽，我的声音爽朗明快，希望能为你带来好心情。",
"晓晓（方言）-女": "大家好，我是晓晓，我能模拟多种方言口音，让交流更有趣味性。",
"晓晓（多语言）-女": "Hello, 我是晓晓，我支持多语言合成，希望能用更自然的声音与你沟通。",
"晓晓（标准）-女": "大家好，我是晓晓，我说标准普通话，声音自然流畅，适合多种场景。",
"晓燕-女": "你好，我是晓燕，我的声音明亮柔和，希望能为你带来温暖。",
"晓怡-女": "大家好，我是晓怡，我的声音甜美自然，适合陪伴与讲述。",
"晓优-女": "嗨～我是晓优，我的声音优雅温和，希望能为你的内容增添魅力。",
"晓语（多语言）-女": "Hello, 我是晓语，我支持多语言合成，让交流更轻松自然。",
"晓真-女": "大家好，我是晓真，我的声音真实自然，希望能带给你舒适的听觉体验。",
"云峰-男": "大家好，我是云峰，我的声音沉稳有力，适合讲述与表达。",
"云浩-男": "你好，我是云浩，我的声音清澈而坚定，希望能为你带来信任感。",
"云健-男": "大家好，我是云健，我的声音阳光健康，适合传递积极的信息。",
"云杰-男": "你好，我是云杰，我的声音稳重而富有磁性，适合多种场合。",
"云熙（标准）-男": "大家好，我是云熙，我说标准普通话，声音自然柔和，适合陪伴与讲述。",
"云夏-男": "你好，我是云夏，我的声音温暖如夏，希望能为你带来轻松的感受。",
"云晓-男": "Hello everyone, 我是云晓，我支持多语言合成，让沟通更自由。",
"云阳-男": "大家好，我是云阳，我的声音明亮有力，适合表达各种内容。",
"云野-男": "你好，我是云野，我的声音自然接地气，适合讲述故事与生活。",
"云逸-男": "Hello, 我是云逸，我支持多语言合成，希望能带给你更自然的听觉体验。",
"云泽-男": "大家好，我是云泽，我的声音温和而坚定，适合表达情感与信息。",
"云登（河南）-男": "大家好，我是云登，我来自河南，河南话是中州音韵的代表，希望你喜欢我的声音。",
"晓北（辽宁）-女": "大家好，我是晓北，我来自辽宁，东北话幽默直爽，希望我的声音能让你会心一笑。",
"晓妮（陕西）-女": "大家好，我是晓妮，我来自陕西，陕西话古朴豪迈，嘹咋咧！希望你喜欢我的声音。",
"云翔（山东）-男": "大家好，我是云翔，我来自山东，山东话朴实热情，希望我的声音能让你感到亲切。",
"云熙（四川）-男": "大家好，我是云熙，我来自四川，四川话爽朗泼辣，巴适得板！希望你喜欢我的声音。",
"晓佳（香港）-女": "识哒内鹅侯温很。",
"晓文（香港）-女": "雷休姐，内爸爸给森台纵给侯嘛？",
"云龙（香港）-男": "李小姐，你爸爸嘅身体仲几好嘛？",
"晓辰（台湾）-女": "大家好，我是曉辰，我來自台灣，說國語，希望我的聲音能讓你感到舒適。",
"晓语（台湾）-女": "大家好，我是曉語，我來自台灣，說國語，聲音溫柔自然，希望能陪伴你。",
"云哲（台湾）-男": "大家好，我是雲哲，我來自台灣，說國語，聲音穩重清晰，適合表達各種內容。"
}
def getVoiceById(voiceId: str) -> Optional[str]:
    return voice_dict.get(voiceId)

def generate_voice_introduction(voice_name: str) -> str:
    """为每个角色生成个性化的自我介绍文本"""
    return voice_text.get(voice_name)

def generate_voice_examples() -> None:
    """为voice_dict中的每个角色生成语音示例文件"""
    print("开始生成语音角色示例文件...")
    
    # 创建目录
    example_dir = os.path.join(os.getcwd(), "example", "voice")
    if not os.path.exists(example_dir):
        os.makedirs(example_dir)
        print(f"创建目录: {example_dir}")
    
    total_voices = len(voice_dict)
    current = 0
    
    for voice_name, voice_id in voice_dict.items():
        current += 1
        print(f"正在生成 ({current}/{total_voices}): {voice_name}")
        
        # 生成介绍文本
        introduction_text = generate_voice_introduction(voice_name)
        
        # 生成文件名（使用角色名作为文件名）
        safe_filename = voice_name.replace("（", "(").replace("）", ")").replace("-", "_")
        file_name = f"{safe_filename}.mp3"
        file_path = os.path.join(example_dir, file_name)
        
        try:
            # 生成语音文件
            asyncio.run(_generate_audio_and_subtitles(
                text=introduction_text,
                voice=voice_id,
                file_path=file_path,
                generate_subtitles=False
            ))
            print(f"✓ 成功生成: {file_name}")
        except Exception as e:
            print(f"✗ 生成失败 {voice_name}: {e}")
    
    print(f"\n语音示例生成完成！共生成 {total_voices} 个文件")
    print(f"文件保存位置: {example_dir}")

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
    # 生成所有语音角色的示例文件
    generate_voice_examples()