import sys,random,os
import csv
import pygame
from settings import DATA_PATH, DIFFICULTY, TOP_LEVEL
from user import User
from load_util import load_font
from inputbox import EnChInputBox
from button import Button

class Game:
    def __init__(self,screen,clock,user,
    big_imgs,medium_imgs,small_imgs,other_imgs,sounds,fonts):
        self.screen = screen
        self.clock = clock
        self.user = user
        self.level = user.level if user.level < TOP_LEVEL else random.randint(0,TOP_LEVEL-1)
        self.big_imgs = big_imgs
        self.medium_imgs = medium_imgs
        self.small_imgs = small_imgs
        self.other_imgs = other_imgs
        self.sounds = sounds
        self.fonts = fonts
        # 队友
        self.parter = None 
        for i in range(5):
            if self.user.presents[i]:
                self.parter = i 
                break
        # 连续写对单词的次数
        self.combo = 0
        # 更新单词列表、正在猜的单词以及提示
        self._update_words()
        # 正在答题
        self.answering = True
        # 答题输入框
        self.answer_box = EnChInputBox(screen,100,350,200,50,fonts[0])
        # 提交按钮
        self.submit_btn = Button(screen,100,450,100,50,fonts[0],
        '提交',(255,255,255),(255,130,0))
        # 下一关按钮
        self.next_btn = Button(screen,100,400,150,50,fonts[0],
        '下一关',(255,255,255),(255,130,0))
        # 新抽到的礼物
        self.new_present = None

    def _load_words(self):
        '''根据用户当前的级别加载15个单词,打乱顺序后返回'''
        # 如果已经达到了最高等级，就从所有级别的单词里随机抽取一个级别
        level = self.level 
        with open(os.path.join(DATA_PATH,'words.csv')) as f:
            csv_reader = csv.reader(f)
            for num,row in enumerate(csv_reader):
                if num == level:
                    random.shuffle(row)
                    return row

    def _update_word(self):
        '''更新要猜的单词'''
        # 正在猜的单词和中文含义
        self.word, self.meaning = self.words.pop().split()
        # 正在猜的单词的提示
        self.hint_img = self._get_hint()

    def _update_words(self):
        '''更新单词列表以及要猜的单词'''
        self.words = self._load_words()
        self._update_word()

    

    def _show_presents(self):
        '''把用户目前拥有的所有礼物展示出来
        如果某个礼物还没有得到，就显示一个问号的图片
        '''
        presents = self.user.presents
        for i in range(5):
            num = presents[i]
            if num:
                self.screen.blit(self.small_imgs[i],(300+i*100,20))
            else:
                self.screen.blit(self.other_imgs[0],(300+i*100,20))
            num_img = self.fonts[1].render(f'X{num}',True,(0,0,0))
            self.screen.blit(num_img,(345+i*100,30))

    def _show_level_and_bar(self):
        '''显示当前等级和进度条'''
        level_img = self.fonts[1].render(f'Level {self.user.level}',True,(0,0,0))
        self.screen.blit(level_img,(20,20))
        colors = []
        for i in range(10):
            colors.append((20+i*20,220-i*20,50))
        for i in range(self.combo):
            pygame.draw.rect(self.screen,colors[i],(95+i*20,25,20,20))
        for i in range(10):
            pygame.draw.rect(self.screen,(0,0,0),(95+i*20,25,20,20),2)

    def _get_hint(self):
        '''获取当前单词的提示'''
        n = random.randrange(0,len(self.word))
        hint = ''
        for i in range(len(self.word)):
            if i == n:
                hint += self.word[i]+' '
            else:
                hint += '_ '    
        hint_img = self.fonts[1].render(hint,True,(0,0,0))
        return hint_img
    
    def _show_partner(self):
        '''如果有队友，就显示队友'''
        if self.parter is not None:
            self.screen.blit(self.medium_imgs[self.parter],(100,100))
    def _show_dictation(self):
        '''显示中文、提示、输入框、提交按钮'''
        # 中文
        meaning_img = self.fonts[0].render(self.meaning,True,(0,0,0))
        self.screen.blit(meaning_img,(100,250))
        # 提示
        self.screen.blit(self.hint_img,(100,300))
        # 输入框
        self.answer_box.draw()
        # 提交按钮
        self.submit_btn.draw()

    def _show_present_box(self):
        '''显示礼物盒子'''
        self.screen.blit(self.other_imgs[1],(350,100))
    
    def _check_answer(self,answer):
        '''检查答案
        如果答对了，连对次数加1
        如果连对次数已经达到10，就要设置成非答题状态
        如果答错了，连对次数回到0
        '''
        self.answer_box.clear()
        if answer.lower() == self.word:
            self.combo += 1
            # 连对10次，用户要升级，单词表也要升级,要抽取一个礼物
            if self.combo == DIFFICULTY:
                self.answering = False 
                self.user.upgrade()
                self.level = self.user.level if self.user.level < TOP_LEVEL else random.randint(0,TOP_LEVEL-1)
                self._update_words()
                num = random.randrange(0,100)
                if num < 22:
                    self.new_present = 0
                elif num < 44:
                    self.new_present = 1
                elif num < 66:
                    self.new_present = 2
                elif num < 83:
                    self.new_present = 3
                else:
                    self.new_present = 4    
                self.user.presents[self.new_present] += 1 
            # 连对没有达到10次，看看单词表是否为空    
            else:
                if self.words:
                    self._update_word()
                else:
                    self._update_words()
        # 答错了，连对回到0，看还有没有单词可以pop决定要不要重新加载单词表
        else:
            self.combo = 0       
            if self.words:
                self._update_word()
            else:
                self._update_words()
        
    def _show_new_present(self):
        '''展示礼物、纸屑、播放音乐'''
        self.screen.blit(self.big_imgs[self.new_present],(350,100))
        self.screen.blit(self.other_imgs[2],(350,100))
        if not pygame.mixer.get_busy():
            self.sounds[self.new_present].play()
            
    def _choose_partner(self,event):
        '''选择队友'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(5):
                if pygame.Rect(300+i*100,20,40,40).collidepoint(event.pos):
                    if self.user.presents[i]:
                        # 如果当前的搭档不是他，就换成他
                        if self.parter != i:
                            self.parter = i 
                        # 如果当前的搭档已经是他了，就换成空白
                        else:
                            self.parter = None
                    else:
                        self.parter = None

    def _write_to_disk(self):
        '''在游戏退出之前，把用户最新的信息更新到csv文件里'''
        rows = []
        with open(os.path.join(DATA_PATH,'user.csv'),'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if row and row[0] == self.user.username:
                    presents = self.user.presents
                    row[2] = self.user.level
                    row[3] = presents[0]
                    row[4] = presents[1]
                    row[5] = presents[2]
                    row[6] = presents[3]
                    row[7] = presents[4]
                rows.append(row)   
        # newline='' 就不会有空行
        # r+是read and append 而我想覆盖 所以必须分别read和write         
        with open(os.path.join(DATA_PATH,'user.csv'),'w',newline='') as f:        
            csv_writer = csv.writer(f)
            csv_writer.writerows(rows)
    

    def run(self):
        '''游戏的主体'''
        
        while True:
            self.clock.tick(30)
            self.screen.fill((255,255,255))

            # 显示右上角的已获得礼物列表
            self._show_presents()
            # 显示左上角当前等级、进度条(10个格子)
            self._show_level_and_bar()
            # 如果是答题状态，显示队友、中文、提示、输入框、提交按钮、礼物盒
            if self.answering:
                self._show_partner()
                self._show_dictation()
                self._show_present_box()
            # 如果不是答题状态，显示抽中的礼物、纸屑、下一关,播放音乐
            else:
                self._show_new_present()
                self.next_btn.draw() 
                
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._write_to_disk()
                    pygame.quit()
                    sys.exit()
                else:
                    if self.answering:
                        self.answer_box.get_text(event)
                        self._choose_partner(event)
                        # 文本框不为空才能提交，避免提交上一个单词的时候误点两次提交按钮
                        # 导致还没有看到下一题就提交了空的字符串，影响成绩
                        if self.submit_btn.click(event) and self.answer_box.text:
                            self._check_answer(self.answer_box.text)
                    else:
                        if self.next_btn.click(event):
                            self.answering = True
                            self.sounds[self.new_present].stop()
                            self.combo = 0


    
            













if __name__ == '__main__':
    pass
