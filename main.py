import sys
import pygame 
from login import login
from register import register
from homepage import homepage
from game import Game
from load_util import load_font, load_image, load_sound
from settings import HOMEPAGE,REGISTER,LOGIN,PLAY,WIDTH,HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# 加载字体
fonts = [
    load_font('msyh.ttf',30),
    load_font('msyh.ttf',20),
]


# 加载图片
# 大图片
big_imgs = [
    load_image('0.png',(400,400)),
    load_image('1.png',(300,400)),
    load_image('2.png',(320,400)),
    load_image('3.png',(250,400)),
    load_image('4.png',(400,400)),
    ]   
# 中图片    
medium_imgs = [
    load_image('5.png',(150,150)),
    load_image('6.png',(140,150)),
    load_image('7.png',(75,150)),
    load_image('8.png',(130,150)),
    load_image('9.png',(140,150)),
]  
# 小图片    
small_imgs = []  
for i in range(10,15):
    small_imgs.append(load_image(f'{i}.png',(40,40)))

# 其他图片
other_imgs = [
    load_image('question.jpg',(40,40)), 
    load_image('礼盒.png',(450,450)),  
    load_image('纸屑.png',(400,400)),
    load_image('眼睛.png',(60,45)),
    load_image('闭眼睛.png',(60,45)),
]



# 加载音乐
sounds = [
    load_sound('0.wav',0.05),
    load_sound('1.wav',0.2),
    load_sound('2.wav',0.05),
    load_sound('3.wav',0.05),
    load_sound('4.wav',0.05),
]

# 游戏页面默认从主页开始显示
game_page = HOMEPAGE

while True:
    if game_page == HOMEPAGE:
        game_page = homepage(screen,fonts[0],clock)
    elif game_page == REGISTER:
        game_page,user = register(screen,fonts[0],clock,other_imgs) 
    elif game_page == LOGIN:
        game_page,user = login(screen,fonts[0],clock,other_imgs)
    elif game_page == PLAY:
        game = Game(screen,clock,user,big_imgs,medium_imgs,small_imgs,other_imgs,sounds,fonts)
        game.run()
         


