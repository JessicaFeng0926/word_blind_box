import os,sys 
import csv
import pygame
from settings import DATA_PATH, REGISTER, PLAY
from user import User
from inputbox import EnChInputBox
from button import Button

def login_check(username,password)->User:
    '''登录验证'''
    user = None
    # 如果用户名和密码都正确，就返回一个用户
    # 用户名 密码 级别 0一拳 1鸣人 2路飞 3伍六七 4柯南
    with open(os.path.join(DATA_PATH,'user.csv')) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row and row[0] == username and row[1]==password:
                user = User(username,
                password,
                level=int(row[2]),
                p0=int(row[3]),
                p1=int(row[4]),
                p2=int(row[5]),
                p3=int(row[6]),
                p4=int(row[7]),
                )
                break        
            
    # 否则就返回None
    return user 

def login(screen,font,clock,other_imgs):
    '''处理用户登录
    如果登录成功，返回PLAY和User，可以开始游戏
    如果登录失败，继续登录
    如果用户选择重新注册，返回REGISTER和None
    '''
    # 用户名框
    username_label = font.render("用户名",True,(0,0,0))
    username_box = EnChInputBox(screen,300,100,200,50,font)
    # 密码框
    password_label = font.render("密码",True,(0,0,0))
    password_box = EnChInputBox(screen,300,250,200,50,font)
    password_box.switch_show()
    # 错误提示
    error = False
    error_img = font.render('用户名或密码错误',True,(255,0,0))
    # 提交按钮
    submit_btn = Button(screen,350,400,100,50,font,"登录",(255,255,255),(255,130,0))
    # 去注册
    register_btn = Button(screen,280,500,250,50,font,"还未注册，去注册",(255,255,255),(255,255,0))
    while True:
        clock.tick(30)
        screen.fill((255,255,255))
        screen.blit(username_label,(200,100))
        screen.blit(password_label,(200,250))
        username_box.draw()
        password_box.draw()
        # 画密码框旁边的小眼睛
        if password_box.show:
            screen.blit(other_imgs[3],(550,250))
        else:
            screen.blit(other_imgs[4],(550,250))
        submit_btn.draw()
        register_btn.draw()
        if error == True:
            screen.blit(error_img,(200,20))
        pygame.display.update()
        # 事件处理
        for event in pygame.event.get():
            # 退出事件
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                # 提交事件
                if submit_btn.click(event):
                    username = username_box.text 
                    password = password_box.text 
                    user = login_check(username,password)
                    if user:
                        return PLAY,user
                    error = True
                # 去注册页事件    
                elif register_btn.click(event):
                    return REGISTER,None    
                
                # 文本框输入处理
                username_box.get_text(event)
                password_box.get_text(event)
                # 只要用户开始重新输入，就不再显示错误信息
                if event.type == pygame.KEYDOWN:
                    error = False
                # 用户点击眼睛，切换密码框的明文密文
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(550,250,60,45).collidepoint(event.pos):
                        password_box.switch_show()    

if __name__ == '__main__':
    user = login_check('jessicaaaa','123456')
    print(user)