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


    def move(self,obstacles,fixed):

        chain=[self.next[i] for i in xrange(len(self.next))]
        chain.append(self.head)

        #for mono in chain:
            

        # #Update the header speed
        # v1=0
        # v2=0
        # obs=0
        # for i in xrange(constant.NB_OBS):
        #     if self.head.near(obstacles[i], constant.CONTACT_OBS)==1:
        #         obstacles[i].v1=-obstacles[i].v1
        #         obstacles[i].v2=-obstacles[i].v2
        #         v1=v1+obstacles[i].v1-self.head.v1
        #         v2=v2+obstacles[i].v2-self.head.v2
        #         obs+=1

        # if obs!=0:
        #     self.head.v1=v1/obs
        #     self.head.v2=v2/obs

        # for j in xrange(constant.NB_FIX):
        #     if self.head.near(fixed[j],constant.CONTACT_FIX)==1:
        #         self.head.v1=-self.head.v1
        #         self.head.v2=-self.head.v2

        # else:
        #     #coordonates of moving vector between -1 and 1
        #     self.head.v1=self.head.v1+(random.random()*2-1)*5
        #     self.head.v2=self.head.v2+(random.random()*2-1)*5

        # norm=math.sqrt(self.head.v1*self.head.v1+self.head.v2*self.head.v2)

        # #monomer's speed constant
        # self.head.v1=self.head.v1*constant.SPEED/norm
        # self.head.v2=self.head.v2*constant.SPEED/norm

        # self.head.wind()

        # self.head.x=self.head.x+constant.TIME*self.head.v1
        # self.head.y=self.head.y+constant.TIME*self.head.v2


        # self.head.update_pol()

        # #Update the polymer speed
        # v1=0
        # v2=0
        # obs=0
        # fix=0
        # for mono in self.next:

        #     mono.v1=self.head.v1
        #     mono.v2=self.head.v2

        #     for i in xrange(constant.NB_OBS):
        #         if mono.near(obstacles[i], constant.CONTACT_OBS)==1:
        #             #obstacles[i].v1=-obstacles[i].v1
        #             #obstacles[i].v2=-obstacles[i].v2
        #             v1=v1+obstacles[i].v1-mono.v1
        #             v2=v2+obstacles[i].v2-mono.v2
        #             obs+=1

        #     for j in xrange(constant.NB_FIX):
        #         if self.head.near(fixed[j],constant.CONTACT_FIX)==1  and mono==self.next[-1]:
        #             self.head.v1=-self.head.v1
        #             self.head.v2=-self.head.v2
        #             fix+=1

        #     mono.x=mono.x+constant.TIME*mono.v1
        #     mono.y=mono.y+constant.TIME*mono.v2

        #     mono.update_pol()

        # if obs!=0 and fix==0: 
        #     self.head.v1=v1/obs
        #     self.head.v2=v2/obs

        #---------------------------------------

        # chain=[self.next[i] for i in xrange(len(self.next))]
        # chain.append(self.head)

        # self.head.wind()

        # v1=self.head.v1
        # v2=self.head.v2

        # for mono in chain:
        #     obs=0
        #     for i in xrange(constant.NB_OBS):
        #         if mono.near(obstacles[i], constant.CONTACT_OBS)==1:
        #             v1=v1+obstacles[i].v1-self.head.v1
        #             v2=v2+obstacles[i].v2-self.head.v2
        #             obs+=1

        #     for j in xrange(constant.NB_FIX):
        #         if mono.near(fixed[j],constant.CONTACT_FIX)==1:
        #             v1=-self.head.v1
        #             v2=-self.head.v2

        #     if obs==0:
        #         v1=v1+(random.random()*2-1)*5
        #         v2=v2+(random.random()*2-1)*5

        #     else:
        #         v1=v1/obs
        #         v2=v2/obs
                
                
        # for mono in chain:
        #     norm=math.sqrt(v1*v1+v2*v2)
        #     mono.v1=mono.v1*(constant.SPEED+10)/norm
        #     mono.v2=mono.v2*(constant.SPEED+10)/norm


        #     mono.x=mono.x+constant.TIME*mono.v1
        #     mono.y=mono.y+constant.TIME*mono.v2

        #     mono.update_pol()

