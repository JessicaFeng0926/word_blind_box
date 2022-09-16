import os
import csv
from settings import DATA_PATH, TOP_LEVEL
class User:
    def __init__(self,username,password,level=0,p0=0,p1=0,p2=0,p3=0,p4=0):
        self.username = username
        self.password = password 
        self.level = level
        self.presents = {0:p0,1:p1,2:p2,3:p3,4:p4}


    def upgrade(self):
        '''用户升级'''
        # 最高可以达到TOP_LEVEL 但是单词表里并不会提供TOP_LEVEL对应的单词
        # 这个级别的意思是可以随机抽取所有背过的级别的单词来听写
        if self.level < TOP_LEVEL:
            self.level += 1

    def get_new_present(self,present_key):
        '''抽到一个新的盲盒，更新礼物字典'''
        self.presents[present_key] += 1
    
    def __repr__(self):
        return f'<User {self.username}>'








