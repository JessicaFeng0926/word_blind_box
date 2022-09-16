import os, string,sys
import csv
from typing import Tuple
import pygame
from settings import DATA_PATH,PLAY,LOGIN
from user import User
from inputbox import EnChInputBox
from button import Button

def register_check(username,password)-> Tuple[User,str]:
    '''新用户注册'''
    with open(os.path.join(DATA_PATH,'user.csv'),'r+',newline='') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row and row[0] == username:
                return None,'用户名已存在'
        if len(password)<6:
            return None, '密码至少要6位字符'
        for ch in password:
            if ch not in string.ascii_letters+"1234567890_":
                return None, '密码只能包含字母、数字和下划线' 
            
        csv_writer = csv.writer(f)
        csv_writer.writerow([username,password,0,0,0,0,0,0])
        return User(username,password),''

def register(screen,font,clock,other_imgs):
    '''处理用户注册，
    如果注册成功，返回PLAY和User
    如果注册失败，继续注册
    如果选择去登录，返回LOGIN和None
    '''
    # 用户名框
    username_label = font.render("用户名",True,(0,0,0))
    username_box = EnChInputBox(screen,300,100,200,50,font)
    # 密码框
    password_label = font.render("密码",True,(0,0,0))
    password_box = EnChInputBox(screen,300,250,200,50,font)
    password_box.switch_show()
    # 提交按钮
    submit_btn = Button(screen,350,400,100,50,font,"注册",(255,255,255),(255,130,0))
    # 去登录
    login_btn = Button(screen,280,500,250,50,font,"已有账户，去登录",(255,255,255),(255,255,0))

    # 错误标记
    error = False
    while True:
        clock.tick(30)
        screen.fill((255,255,255))
        screen.blit(username_label,(200,100))
        screen.blit(password_label,(200,250))
        username_box.draw()
        password_box.draw()
        if password_box.show:
            screen.blit(other_imgs[3],(550,250))
        else:
            screen.blit(other_imgs[4],(550,250))    
        submit_btn.draw()
        login_btn.draw()
        if error:
            error_img = font.render(msg,True,(255,0,0))
            screen.blit(error_img,(200,20))
        pygame.display.update()
        # 事件处理
        for event in pygame.event.get():
            # 退出事件
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:    
                # 注册事件
                if submit_btn.click(event):
                    username = username_box.text 
                    password = password_box.text
                    user,msg = register_check(username,password)
                    if user:
                        return PLAY,user
                    error = True    
                # 去登录
                elif login_btn.click(event):
                    return LOGIN,None
                # 文本框接受输入
                username_box.get_text(event)
                password_box.get_text(event)

                # 取消错误显示
                if event.type == pygame.KEYDOWN:
                    error = False
                # 点击小眼睛，切换明文密文
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(550,250,60,45).collidepoint(event.pos):
                        password_box.switch_show()    

if __name__ == '__main__':
    data = register_check('jay','1234567')
    print(data)