import pygame
from pathlib import Path
import random


class Cover:
    def __init__(
        self, 
        covers_dir:str, 
        img_path:str,
        screen_w:int, 
        screen_h:int, 
        percentage:int=60,
        gap:int=20,
        pos:int=5,
        fps:int=60,
        time:float=3
    ):
        """
        封面类
        covers_dir: 封面文件夹路径
        img_path: 要插入的图片路径
        screen_w: 屏幕宽度
        screen_h: 屏幕高度
        percentage: 图片高度占屏幕高度的百分比
        gap: 图片之间的间距
        pos: 要插入的位置
        """
        self.covers_dir = covers_dir
        self.img_path = img_path
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.percentage = percentage
        self.gap = gap
        self.pos = pos
        self.total_frames = int(fps*time)
        self.images = self.load_images()

    def load_images(self):
        # 读取self.file_path中所有的png或者jpg图片到列表中
        image_list = [str(p) for p in Path(self.covers_dir).glob("*.png")]
        image_list += [str(p) for p in Path(self.covers_dir).glob("*.jpg")]
        image_list += [str(p) for p in Path(self.covers_dir).glob("*.jpeg")]
        # 打乱列表
        random.shuffle(image_list)
        # 取前10张图片加载
        image_list = image_list[:10]
        # 加载图片并缩放图片到屏幕大小
        images = []
        h = int(self.screen_h*self.percentage/100)
        for image in image_list:
            img = pygame.image.load(image).convert()
            w1, h1 = img.get_size()
            # 缩放图片
            img = pygame.transform.scale(img, (int(w1*h/h1), h))

            images.append(img)

        # 加载self.img_path图片
        img = pygame.image.load(self.img_path).convert()
        w1, h1 = img.get_size()
        # 缩放图片
        img = pygame.transform.scale(img, (int(w1*h/h1), h))
        images.insert(self.pos, img)
        
        return images

    def update(self, screen:pygame.Surface, p:int, speed:int=10):
        # x,y为图片的左上角坐标, y是固定的
        y = int(self.screen_h * (100 - self.percentage)/2 / 100)
        x = self.calc_x(p, speed=speed)

        for i, img in enumerate(self.images):
            screen.blit(img, (x, y))
            x += img.get_width() + self.gap
    
    def calc_x(self, p:int,tip:int=70, speed:int=10):
        """
        计算图片的x坐标, 运动轨迹，先向左，再向右，最终停留在目标位置
        p: 第p帧
        tip: 转折点，百分比，0-100，小于tip向左，大于tip向右
        speed: 速度
        return: 图片的x坐标
        """
        # 计算目标x的坐标
        target_x = (self.screen_w - self.images[self.pos].get_width())//2
        # 计算初始x的坐标
        init_x = self.get_target_pos()
        # print((0,init_x), (210*70/100,0), (210,target_x))
        frames = int(self.total_frames*tip/100)
        if p<=frames:
            # 向左移动，x坐标减小
            x = -speed*p
        elif p<=self.total_frames:
            # 向右一点，x坐标增加。x坐标从(-speed*frames)开始，增加到(target_x-init_x)
            a = (target_x-init_x - (-speed*frames))/(self.total_frames - frames)
            k = -speed*frames - a*frames
            x = a*p + k
        else:
            x = target_x - init_x

        return x

    def get_target_pos(self):
        x = 0
        for one in self.images[:self.pos]:
            x += one.get_width() + self.gap
        return x
            
class BoxSprite:
    def __init__(
        self, 
        fps:int, 
        screen_w:int, 
        screen_h:int, 
        cover_w:int,
        cover_h:int,
        time:float=3,
        percentage:int=90,
    ):
        """
        盒子类
        fps: 帧率
        screen_w: 屏幕宽度
        screen_h: 屏幕高度
        cover_w: 封面宽度
        cover_h: 封面高度
        time: 时间
        percentage: 初始位置百分比
        """
        self.fps = fps
        self.total_frames = int(time * fps)

        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cover_w = cover_w
        self.cover_h = cover_h

        self.max_h = int(self.screen_h*percentage/100)
        self.min_h = self.cover_h + 20

    def get_pos(self, delta_h:float=0):
        h = int(self.max_h-delta_h)
        w = int(h*self.cover_w/self.cover_h)

        y = int((self.screen_h - h)/2)
        x = int((self.screen_w - w)/2)
        return pygame.rect.Rect(x, y, w, h)

    
    def update(self, screen:pygame.Surface, p: int):
        """
        p: 第p帧
        3.5秒内到指定位置，大概就是当p=fps*3.5时，位置到达指定位置
        """
        # 白框最小高度
        per_h = (self.max_h - self.min_h) / self.total_frames
        # 每帧减小高度
        if p < self.total_frames:
            delta_h = per_h * p
        else:
            delta_h = (self.max_h - self.min_h)

        pygame.draw.rect(screen, (255, 255, 255), self.get_pos(delta_h), 3)

class Background:
    def __init__(self, backgrounds_dir: str, screen_w: int, screen_h: int, fps: int = 60, switch_time: float = 10):
        """
        背景类
        backgrounds_dir: 背景图片文件夹路径
        screen_w: 屏幕宽度
        screen_h: 屏幕高度
        fps: 帧率
        switch_time: 每张图片显示时间（秒）
        """
        self.backgrounds_dir = backgrounds_dir
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.fps = fps
        self.switch_time = switch_time
        self.total_frames = int(fps * switch_time)
        self.images = self.load_images()
        self.num_images = len(self.images)

    def load_images(self):
        # 读取所有png图片到列表
        image_list = [str(p) for p in Path(self.backgrounds_dir).glob("*.jpg")]
        images = []
        for image in image_list:
            img = pygame.image.load(image).convert()
            img_w, img_h = img.get_size()
            scale_w = self.screen_w / img_w
            scale_h = self.screen_h / img_h
            scale = max(scale_w, scale_h)  # 按长边等比例缩放，保证不会出现短边
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            scaled_img = pygame.transform.smoothscale(img, (new_w, new_h))
            images.append(scaled_img)
        return images

    def update(self, screen: pygame.Surface, p: int):
        if self.num_images == 0:
            return

        idx = (p // self.total_frames) % self.num_images
        img = self.images[idx]

        # 获取原始图片的尺寸
        img_w, img_h = img.get_size()

        # 计算绘制位置，保持图片中心与屏幕中心对齐
        x = (self.screen_w - img_w) / 2
        y = (self.screen_h - img_h) / 2
        # 将图片绘制到屏幕上
        screen.blit(img, (x, y))


def get_screen_size(mode:str, zoom:int=150):
    """
    获取屏幕大小
    mode: 屏幕比例
    zoom: 缩放比例
    return: 屏幕大小
    """
    if mode == "16:9":
        return int(1920*100/zoom), int(1080*100/zoom)
    elif mode == "9:16":
        return int(1080*100/zoom), int(1920*100/zoom),

# pygame setup
pygame.init()
screen_w, screen_h = get_screen_size("16:9", 200)

# print(screen_w, screen_h)
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
running = True
fps = 60
# 创建精灵
pos=5   # 封面出现的位置
cover = Cover(
    covers_dir="covers",
    img_path="文城.jpg",
    screen_w=screen_w,
    screen_h=screen_h,
    percentage=50,
    gap=20,
    pos=pos,
    fps=fps
)
box = BoxSprite(
    fps=fps,
    screen_w=screen_w,
    screen_h=screen_h,
    cover_w=cover.images[pos].get_width(),
    cover_h=cover.images[pos].get_height(),
    percentage=200,
)
background = Background(
    backgrounds_dir="backgrounds",
    screen_w=screen_w,
    screen_h=screen_h,
    fps=fps,
    switch_time=10
)

p = 0
# 播放背景音乐
pygame.mixer.init()
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.play(-1)  # 循环播放


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill("purple")
    # 绘制精灵
    # 前3.5s
    if p<=4*fps:
        cover.update(screen, p)
        box.update(screen, p)
    else:
        background.update(screen, p)

    
    p += 1
    if p%60==0:
        print('第', p//60, '秒')

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
pygame.mixer.music.stop()  # 停止音乐播放






