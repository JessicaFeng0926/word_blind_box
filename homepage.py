import sys
import pygame
from button import Button
from settings import REGISTER, LOGIN

def homepage(screen,font,clock):
    register_btn = Button(screen,300,200,200,50,font,'注册',(255,255,255),(255,130,0))
    login_btn = Button(screen,300,400,200,50,font,'登录',(255,255,255),(255,130,0))
    

    while True:
        screen.fill((255,255,255))
        register_btn.draw()
        login_btn.draw()
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if register_btn.click(event):
                    return REGISTER
                elif login_btn.click(event):
                    return LOGIN    



