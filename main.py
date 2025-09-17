from llm import LLMClient
from spider import get_book_cover_from_douban, download_cover_image
from tts_generator import createAudio, voice_dict
from pathlib import Path
from app import make_movie


def generate_book_caption(book_info: dict) -> str:
    """
    使用LLM生成书籍的文案
    """
    llm = LLMClient()
    response = llm.chat(str(book_info))
    if response.get("error"):
        # print(f"错误: {response['message']}")
        content = ""
    else:
        # print(f"回复: {response.get('content', '无内容')}")
        content = response.get('content', '无内容')
    temp = content.split('\n')
    if "今天分享的是" != temp[0]:
        temp[0] = "今天分享的是"
        content = '\n'.join(temp)
    
    # print(content)
    return content

if __name__ == "__main__":
    root_dir = Path(__file__).parent
    file_dir = root_dir / "appdata"
    resource_dir = root_dir / "resource"
    cover_dir = resource_dir / 'covers'

    book_name = "巴别塔"
    # 使用Pathlib创建同名文件夹
    book_dir = Path(file_dir) / book_name
    book_dir.mkdir(parents=True, exist_ok=True)

    
    book_info = get_book_cover_from_douban(book_name)
    if book_info:
        # 下载封面并保存到covers文件夹中
        cover_url = book_info['pic']
        cover_path = download_cover_image(cover_url, book_name, cover_dir)
        # 生成文案
        del book_info['pic']
        content = generate_book_caption(book_info)

        # 生成音频和字幕
        voice = voice_dict.get("晓秋-女")
        audio_path = book_dir / f'{book_name}.mp3'
        createAudio(content, audio_path, voice)

        make_movie(resource_dir, cover_path, book_dir, resource_dir / "fonts" / "msyh.ttc")


