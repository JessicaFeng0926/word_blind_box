import os,sys,math

import pygame 
from Pinyin2Hanzi import DefaultDagParams,dag,simplify_pinyin


class EnChInputBox():
    
    # 拼音转汉字需要使用的一个对象
    dagparams = DefaultDagParams()

    def __init__(self,surf,left,top,width,height,font):
        self.surf = surf
        self.font = font
        self.rect = pygame.Rect(left,top,width,height)
        self.list = []
        self.active = False
        # 光标
        self.cursor = True
        # 光标闪烁计数器
        self.count = 0
        self.delete = False
        # 中/英
        self.english = True 
        # 存拼音
        self.pinyin = []
        # 候选汉字
        self.candidates = []
        # 汉字页数
        self.page = 0
        # 是否明文
        self.show = True

    def draw(self):
        # 画框
        pygame.draw.rect(self.surf,(0,0,0),self.rect,1)
        # 投放文字
        self._draw_text()
        # 删除文字
        self._delete()
        # 绘制中英文标志
        self._draw_lang()
        # 画输入法拼音和备选汉字
        self._draw_imd()
    
    
    def get_text(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 聚焦或失焦
            self._get_focused(event)
        elif event.type == pygame.KEYUP:
            # 停止删除
            self._stop_deleting(event)
        elif event.type == pygame.KEYDOWN and self.active:
            # 切换中英文输入法
            self._switch_lang(event)
            # 开始删除
            self._start_deleting(event)
            # 获取英文或中文输入
            if self.english:
                self._get_english(event)
            else:
                self._get_chinese(event)    
    
    @property
    def text(self):
        return ''.join(self.list)

    def clear(self):
        '''清空文本框'''
        self.list.clear()
        self.pinyin.clear()    
        self.candidates.clear()
    
    def switch_show(self):
        '''切换明文密文'''
        self.show = not self.show 

    def _draw_text(self):
        '''绘制文本框里的文字和光标'''
        # 画文字
        text = ''.join(self.list)
        start = 0
        # 明文
        if self.show:
            while self.font.size(text[start:])[0] >= self.rect.width-10:
                start += 1
            text_pic = self.font.render(text[start:],True,(0,0,0))  
        # 密文      
        else:
            while self.font.size((len(text)*"*")[start:])[0] >= self.rect.width-10:
                start += 1
            text_pic = self.font.render((len(text)*"*")[start:],True,(0,0,0)) 

        self.surf.blit(text_pic,(self.rect.x+5,self.rect.y+10))
        # 画光标
        self._draw_cursor(text_pic.get_rect().width)
    
    def _draw_cursor(self,text_width):
        '''绘制光标'''
        # 光标计数器更新
        self.count += 1
        if self.count == 20:
            self.count = 0 
            self.cursor = not self.cursor
        # 绘制竖线
        if self.active and self.cursor:
            x = self.rect.x+5+text_width
            pygame.draw.line(self.surf,(0,0,0),\
                (x,self.rect.y+5),(x,self.rect.y+self.rect.height-5),1)

    def _delete(self):
        '''删除文字'''
        if self.delete and self.count%3==0:
            if self.english or not self.pinyin:
                if self.list:
                    self.list.pop()
            else:
                self.pinyin.pop()
                # 删除了一个拼音，联想出来的备选汉字就应该跟着发生变化 
                self._pinyin2hanzi()

    def _draw_lang(self):
        '''画中/英标记'''
        lang = '英' if self.english else '中'
        lang_img = self.font.render(lang,True,(0,0,0),(253,245,230))
        self.surf.blit(lang_img,(self.rect.x+10+self.rect.width,self.rect.y))
    
    def _draw_imd(self):
        '''画拼音和备选汉字'''
        if self.pinyin:
            # 画拼音
            pinyin_pic = self.font.render(''.join(self.pinyin),True,(200,0,0),(253,245,230))
            pinyin_height = pinyin_pic.get_rect().height
            self.surf.blit(pinyin_pic,(self.rect.x-50,
            self.rect.y+self.rect.height))
            
            # 画汉字
            chs = []
            for i,ch in enumerate(self.candidates[self.page*5:self.page*5+5]):
                chs.append(str((i+1)))
                chs.append(ch+' ')
            ch_pic = self.font.render(''.join(chs),True,(200,0,0),(253,245,230))
            self.surf.blit(ch_pic,(self.rect.x-50,
            self.rect.y+self.rect.height+pinyin_height))
    
    def _pinyin2hanzi(self):
        '''按照目前的拼音更新备选汉字列表'''
        pinyin = simplify_pinyin(''.join(self.pinyin))
        result = dag(self.dagparams,[pinyin],path_num=100)
        
        # 加入新的备选汉字之前，要把之前的备选汉字清空
        self.candidates.clear()
        for item in result:
            self.candidates.extend(item.path)
        self.page = 0

    def _get_english(self,event):
        '''获取英文输入'''
        if   event.key >= 65 and event.key<=90  \
            or event.key>=97 and event.key<=122\
            or event.key >= 48 and event.key <= 57:
            self.list.append(event.unicode)
        elif event.key == pygame.K_SPACE:
            self.list.append(' ')
    
    def _get_chinese(self,event):
        '''获取中文输入'''
        # 输入的是拼音，就存入拼音列表，并且更新候选汉字
        if   event.key >= 65 and event.key<=90  or event.key>=97 and event.key<=122:
            
            self.pinyin.append(event.unicode.lower())
            self._pinyin2hanzi()
            
        # 输入的是数字
        # 如果现在有此号码的候选汉字，就把汉字存入文本列表
        # 否则就把阿拉伯数字存入文本列表
        elif event.key>=48 and event.key <= 57:
           
            num = int(event.unicode) if event.unicode in '123456789' else 10
            current_candicates = self.candidates[self.page*5:self.page*5+5]
            if len(current_candicates) >= num:
                self.list.append(current_candicates[num-1])
            else:
                self.list.append(event.unicode)
            self.pinyin.clear()
            self.candidates.clear()
        # 输入的是空格，如果此时有候选汉字，就把第一个汉字存入文字列表
        # 如果此时没有候选汉字，就把空格存入文字列表
        # 清空现有的拼音和候选汉字
        elif event.key == pygame.K_SPACE:
            if self.candidates:
                self.list.append(self.candidates[self.page*5])
                self.candidates.clear()
            else:
                self.list.append(' ')
            self.pinyin.clear()
                    
        # 按加号和减号可以翻页
        elif event.key == pygame.K_MINUS:
            self._get_previous_page()
        elif event.key == pygame.K_EQUALS:
            self._get_next_page()

    
    
    def _get_previous_page(self):
        if self.page>0:
            self.page -= 1
    
    def _get_next_page(self):
        if self.page < math.ceil(len(self.candidates)/10)-1:
            self.page += 1
    def _get_focused(self,event):
        '''聚焦或失焦'''
        if self.rect.collidepoint(event.pos):
            self.active = True
        else:
            self.active = False

    def _start_deleting(self,event):
        '''开始删除'''
        if event.key == pygame.K_BACKSPACE:
            self.delete = True

    def _stop_deleting(self,event):
        '''停止删除'''
        if event.key == pygame.K_BACKSPACE:
            self.delete = False  
                
                    
    def _switch_lang(self,event):
        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            self.english = not self.english
            if self.english:
                self.pinyin.clear()
                self.candidates.clear()
    
    

if __name__ == '__main__':
    # 切换工作目录
    path = os.path.dirname(__file__)
    os.chdir(path)
    # pygame基本设置
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    font = pygame.font.Font("msyh.ttf",30)
    
    # 问题列表
    questions = [
        '你最喜欢的动漫人物是谁？',
        '写一个你喜欢的地方',
        '你最讨厌的家务是什么？',
        ]
    # 问题序号    
    qnum = 0    
    
    # 存放答案
    answers = []
    # 输入答案的文本框
    answer_box = EnChInputBox(screen,250,200,320,50,font)

    # 提示语
    cimg = font.render("按 回车 进行下一步",True,(0,0,255),(187,255,255))

    while True:
        clock.tick(30)
        screen.fill((255,255,255))
        
        # 如果答完了，就显示最终的结果
        if qnum == 3:
            aimg = font.render(f'{answers[0]}在{answers[1]}{answers[2]}。',True,(0,0,0))
            aimg_rect = aimg.get_rect(center=screen.get_rect().center)
            screen.blit(aimg,(aimg_rect.x,aimg_rect.y))
        
        # 没答完，就继续展示问题、答案文本框和提示语
        else:    
            # 问题图片
            qimg = font.render(questions[qnum],True,(0,0,0))
            screen.blit(qimg,(250,110))
            screen.blit(cimg,(500,400))
            answer_box.draw()
            

            

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                answer_box.get_text(event)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if qnum < 3:
                            answers.append(answer_box.text)
                            answer_box.clear()
                            qnum += 1

                        
                            


        

