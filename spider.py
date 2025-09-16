"""
功能，用户输入一本书的名字，返回这本书的封面图片，
并保存到covers文件夹中，文件名为 书名.jpg
"""

import requests
import os
import json
from urllib.parse import quote
import time
import random
from typing import Dict, Optional


def get_book_cover_from_douban(book_name: str) -> Optional[Dict]:
    """
    从豆瓣获取书籍封面图片
    """
    try:
        # 豆瓣图书搜索API
        search_url = f"https://book.douban.com/j/subject_suggest?q={quote(book_name)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://book.douban.com/'
        }
        
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                # 获取第一个搜索结果的封面图片URL
                book_info = data[0]
                # {'title': '巴别塔', 'url': 'https://book.douban.com/subject/36463571/', 'pic': 'https://img1.doubanio.com/view/subject/s/public/s34640760.jpg', 'author_name': '[美]匡灵秀', 'year': '2023', 'type': 'b', 'id': '36463571'}
                # print(book_info)
                return book_info
        return None
        
    except Exception as e:
        print(f"从豆瓣获取封面失败: {e}")
        return None


def download_cover_image(cover_url: str, book_title: str, save_folder: str = 'Covers') -> Optional[str]:
    """
    下载封面图片并保存到指定文件夹
    """
    try:
        # 确保保存文件夹存在
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        # 清理文件名中的非法字符
        safe_filename = "".join(c for c in book_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_filename}.jpg"
        filepath = os.path.join(save_folder, filename)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(cover_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"封面图片已保存: {filepath}")
            return filepath
        else:
            print(f"下载失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"下载封面图片失败: {e}")
        return None


def get_book_cover(book_name: str) -> Optional[str]:
    """
    主函数：获取书籍封面图片
    """
    print(f"正在搜索《{book_name}》的封面图片...")
    
    # 首先尝试从豆瓣获取
    book_info = get_book_cover_from_douban(book_name)
    
    # 如果豆瓣失败，尝试Open Library
    if not book_info:
        raise Exception("从豆瓣获取封面失败")
    
    if book_info and book_info.get('pic'):
        print(f"找到封面图片: {book_info['title']}")
        filepath = download_cover_image(book_info['pic'], book_info['title'])
        
        if filepath:
            return filepath
        else:
            print("下载封面图片失败")
            return None
    else:
        print(f"未找到《{book_name}》的封面图片")
        return None


if __name__ == "__main__":
    book_name = input("请输入书名: ")
    result = get_book_cover(book_name)
    
    if result:
        print(f"成功！封面已保存到: {result}")
    else:
        print("获取封面失败，请检查网络连接或尝试其他书名。")