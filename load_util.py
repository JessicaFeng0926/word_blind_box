import os
import pygame 
from settings import IMAGE_PATH, FONT_PATH, AUDIO_PATH

def load_image(img_name,size=None):
    '''根据图片的名字和尺寸加载并返回图片对象'''
    img = pygame.image.load(os.path.join(IMAGE_PATH,img_name)).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img,size)
    return img     

def load_font(font_name,size):
    '''根据字体名字和尺寸构造并返回字体对象'''
    font = pygame.font.Font(os.path.join(FONT_PATH,font_name),size)
    return font 

def load_sound(sound_name,volume=1.0):
    sound = pygame.mixer.Sound(os.path.join(AUDIO_PATH,sound_name))
    sound.set_volume(volume)
    return sound




