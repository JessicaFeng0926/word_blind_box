import pygame

class Button:
    '''按钮类'''
    def __init__(self,surf,left,top,width,height,font,text,font_color,bgcolor):
        self.surf = surf 
        self.rect = pygame.Rect(left,top,width,height)
        self.text_image = font.render(text,True,font_color)
        # 按钮方框的颜色
        self.bgcolor = bgcolor 


    def draw(self):
        '''把按钮绘制到指定平面上'''
        pygame.draw.rect(self.surf,self.bgcolor,self.rect)
        # 文字和按钮的矩形对齐
        text_rect = self.text_image.get_rect(center=self.rect.center)
        self.surf.blit(self.text_image,(text_rect.x,text_rect.y))

    def click(self,event):
        '''如果该按钮被点击了，就返回True，否则返回False'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True 
        return False 
