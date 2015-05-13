from Tkinter import *

import random
import math
import constant
#import numpy

class polymer:

    def __init__(self, nhead, nnext):
        self.head=nhead
        self.head.ishead=1
        self.head.ispoly=1
        self.next=[nnext]
        self.next[0].ispoly=1

    def add(self,nelse,dic):
        self.next.append(self.head)
        self.head.ishead=0
        del dic[self.head]
        self.head=nelse
        nelse.ishead=1
        self.head.ispoly=1
        dic[self.head]=self


    def move(self):

        #Update the header speed

        #coordonates of moving vector between -1 and 1
        self.head.v1=self.head.v1+(random.random()*2-1)*5
        self.head.v2=self.head.v2+(random.random()*2-1)*5
        norm=math.sqrt(self.head.v1*self.head.v1+self.head.v2*self.head.v2)

        #monomer's speed constant
        self.head.v1=self.head.v1*constant.SPEED/norm
        self.head.v2=self.head.v2*constant.SPEED/norm

        self.head.wind()

        self.head.x=self.head.x+constant.TIME*self.head.v1
        self.head.y=self.head.y+constant.TIME*self.head.v2


        self.head.update_pol()

        #Update the polymer speed

        for mono in self.next:
            mono.v1=self.head.v1
            mono.v2=self.head.v2

            mono.x=mono.x+constant.TIME*mono.v1
            mono.y=mono.y+constant.TIME*mono.v2

            mono.update_pol()


