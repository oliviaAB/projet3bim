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
        self.v1=self.head.v1
        self.v2=self.head.v2
        
    def add(self,nelse,dic):
        self.next.append(self.head)
        self.head.ishead=0
        del dic[self.head]
        self.head=nelse
        nelse.ishead=1
        self.head.ispoly=1
        dic[self.head]=self


    def move(self,monomers, obstacles,fixed):

##        #Update the header speed
##
##        #coordonates of moving vector between -1 and 1
##        self.head.v1=self.head.v1+(random.random()*2-1)*5
##        self.head.v2=self.head.v2+(random.random()*2-1)*5
##        norm=math.sqrt(self.head.v1*self.head.v1+self.head.v2*self.head.v2)
##
##        #monomer's speed constant
##        self.head.v1=self.head.v1*constant.SPEED/norm
##        self.head.v2=self.head.v2*constant.SPEED/norm
##
##        self.head.wind()
##
##        self.head.x=self.head.x+constant.TIME*self.head.v1
##        self.head.y=self.head.y+constant.TIME*self.head.v2
##
##
##        self.head.update_pol()
##
##        #Update the polymer speed
##
##        for mono in self.next:
##            mono.v1=self.head.v1
##            mono.v2=self.head.v2
##
##            mono.x=mono.x+constant.TIME*mono.v1
##            mono.y=mono.y+constant.TIME*mono.v2
##
##            mono.update_pol()


        chain=[self.next[i] for i in xrange(len(self.next))]
        chain.append(self.head)


        obs=0
        v1=0
        v2=0

        for mono in chain:
            for i in xrange(constant.NB_OBS):
                if mono.near(obstacles[i], constant.CONTACT_OBS)==1:
                    v1=v1+obstacles[i].v1-self.v1
                    v2=v2+obstacles[i].v2-self.v2
                    obs+=1

            for y in xrange(constant.NB_MONO):
                if mono.near(monomers[y],constant.CONTACT_MONO)==1 and monomers[y].num!=mono.num:
                    v1=v1+monomers[y].v1-self.v1
                    v2=v2+monomers[y].v2-self.v2
                    obs+=1

        if obs!=0 and (v1+v2)!=0:
            self.v1=v1/obs
            self.v2=v2/obs

        else:
            self.v1=self.v1+(random.random()*2-1)*5
            self.v2=self.v2+(random.random()*2-1)*5

        fix=0
        i=0
        j=0

        print len(self.next), len(chain) 


        while i<len(chain) and fix==0:

            while j<constant.NB_FIX and fix==0:
                if chain[i].near(fixed[j], constant.CONTACT_FIX)==1:
                    fix=1
                j+=1
            i+=1

        if fix!=0:
            print 'BUTE'
            self.v1=-self.v1
            self.v2=-self.v2


        wind=0
        i=0
        while i<len(chain) and wind==0:
            if chain[i].r>(constant.R-50):
                wind=1
            i+=1

        if wind !=0:    
            braking=(50-(constant.R-chain[i-1].r))/5
            
            if chain[i-1].x>constant.R:
                #top right quarter
                if chain[i-1].y<constant.R:
                    self.v1=self.v1-braking
                    self.v2=self.v2+braking
                    
                #bottom right quarter
                if chain[i-1].y>constant.R:
                    self.v1=self.v1-braking
                    self.v2=self.v2-braking

            #left half
            if chain[i-1].x<constant.R:
                #top left quarter
                if chain[i-1].y<constant.R:
                    self.v1=self.v1+braking
                    self.v2=self.v2+braking

                #bottom left quarter
                if chain[i-1].y>constant.R:
                    self.v1=self.v1+braking
                    self.v2=self.v2-braking


        norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
        #monomer's speed constant
        self.v1=self.v1*constant.SPEED/norm
        self.v2=self.v2*constant.SPEED/norm

        for mono in chain:
            mono.v1=self.v1
            mono.v2=self.v2
            mono.x=mono.x+constant.TIME*mono.v1
            mono.y=mono.y+constant.TIME*mono.v2

            mono.update_pol()

                             
                             
                        


