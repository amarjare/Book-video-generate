import pygame
from pathlib import Path
import random

class Cover(pygame.sprite.Sprite):
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
        time:float=3.5 
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

        super().__init__()
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
    
    def calc_x(self, p:int,tip:int=110, speed:int=10):
        """
        计算图片的x坐标, 运动轨迹，先向左，再向右，最终停留在目标位置
        p: 第p帧
        tip: 转折点，0-self.total_frames，小于tip向左，大于tip向右
        return: 图片的x坐标
        """
        # 计算目标x的坐标
        target_x = (self.screen_w - self.images[self.pos].get_width())//2
        # 计算初始x的坐标
        init_x = self.get_target_pos()
        # print((0,init_x), (210*70/100,0), (210,target_x))
        if p<=tip:
            # 向左移动，x坐标减小
            x = -speed*p
        elif p<=self.total_frames:
            # 向右一点，x坐标增加。x坐标从(-speed*tip)开始，增加到(target_x-init_x)
            a = (target_x-init_x - (-speed*tip))/(self.total_frames - tip)
            k = -speed*tip - a*tip
            x = a*p + k
        else:
            x = target_x - init_x

        return x

    def get_target_pos(self):
        x = 0
        for one in self.images[:self.pos]:
            x += one.get_width() + self.gap
        return x
            
class BoxSprite(pygame.sprite.Sprite):
    def __init__(
        self, 
        fps:int, 
        screen_w:int, 
        screen_h:int, 
        cover_w:int,
        cover_h:int,
        time:float=3.5,
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
        super().__init__()
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
)
box = BoxSprite(
    fps=60,
    screen_w=screen_w,
    screen_h=screen_h,
    cover_w=cover.images[pos].get_width(),
    cover_h=cover.images[pos].get_height(),
    time=3.5,
    percentage=200,
)

p = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill("purple")
    # 绘制精灵
    cover.update(screen, p)
    box.update(screen, p)
    p += 1
    if p%60==0:
        print('第', p//60, '秒')

    pygame.display.flip()
    clock.tick(60)

pygame.quit()