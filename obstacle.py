from Tkinter import *

import random
import math
import constant



class obstacle:

    def __init__(self):
        
        #polar coordinates initialized randomly
        self.r=random.random()*constant.R
        self.theta=random.random()*math.pi-(math.pi/2)

        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)+constant.R
        self.y=self.r*math.sin(self.theta)+constant.R

        self.v1=random.random()*2-1
        self.v2=random.random()*2-1

    def __repr__(self):
        print self.r, self.theta
        return str(self.x)+","+str(self.y)

    def get_coordcart(self):
        return(self.x,self.y)

    def get_coordpol(self):
        return(self.r,self.theta)

    def update_cart(self):
        self.x=self.r*math.cos(self.theta)+constant.R
        self.y=self.r*math.sin(self.theta)+constant.R

    def update_pol(self):
        x=self.x-constant.R
        y=self.y-constant.R
        self.r=math.sqrt(x*x+y*y)
        self.theta=math.atan2(y,x)
        #print self.r
##        self.r=math.sqrt(self.x*self.x+self.y*self.y)
##        self.theta=math.atan2(self.y,self.x)

    def near(self, obstacle, contact):
        res=0
        norm=math.sqrt((self.x-obstacle.x)*(self.x-obstacle.x)+(self.y-obstacle.y)*(self.y-obstacle.y))
        if norm<contact:
            res=1
        return res

    def move_random(self):

        #coordonates of moving vector between -1 and 1
        self.v1=self.v1+(random.random()*2-1)*5
        self.v2=self.v2+(random.random()*2-1)*5
        norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)

        #monomer's speed constant
        self.v1=self.v1*constant.SPEED/norm
        self.v2=self.v2*constant.SPEED/norm

    def wind(self):
        if self.r>(constant.R-50):
            braking=(50-(constant.R-self.r))/5
            #print braking
            
            if self.x>constant.R:
                #top right quarter
                if self.y<constant.R:
                    self.v1=self.v1-braking
                    self.v2=self.v2+braking
                    
                #bottom right quarter
                if self.y>constant.R:
                    self.v1=self.v1-braking
                    self.v2=self.v2-braking

            #left half
            if self.x<constant.R:
                #top left quarter
                if self.y<constant.R:
                    self.v1=self.v1+braking
                    self.v2=self.v2+braking

                #bottom left quarter
                if self.y>constant.R:
                    self.v1=self.v1+braking
                    self.v2=self.v2-braking


    def move(self, obstacles, monomers,fixed,num):
        obs=0
        v1=0
        v2=0

        for i in xrange(constant.NB_OBS):
            if i!=num:
                if self.near(obstacles[i], constant.CONTACT_OBS)==1:
                    v1=v1+obstacles[i].v1-self.v1
                    v2=v2+obstacles[i].v2-self.v2
                    obs+=1

        for y in xrange(constant.NB_MONO):
            if self.near(monomers[y],constant.CONTACT_MONO)==1:
                v1=v1+monomers[y].v1-self.v1
                v2=v2+monomers[y].v2-self.v2
                obs+=1

        for j in xrange(constant.NB_FIX):
            if self.near(fixed[j],constant.CONTACT_FIX)==1:
                self.v1=-self.v1
                self.v2=-self.v2
                
        if obs==0:
            self.move_random()
        else:
            self.v1=v1/obs
            self.v2=v2/obs
            norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
            self.v1=self.v1*(constant.SPEED+10)/norm
            self.v2=self.v2*(constant.SPEED+10)/norm

        self.wind()

        self.x=self.x+constant.TIME*self.v1
        self.y=self.y+constant.TIME*self.v2

        self.update_pol()                
