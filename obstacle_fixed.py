from Tkinter import *

import random
import math
import constant
import polymer
#import numpy


class obstacle_fixed:

    def __init__(self):
        
        #polar coordinates initialized randomly
        self.r=random.random()*(constant.R-constant.RAYON_FIX) #to prevent fixed obstacles from being on the limit of the cell
        self.theta=random.random()*math.pi-(math.pi/2)

        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)+constant.R
        self.y=self.r*math.sin(self.theta)+constant.R

    def __repr__(self):
        print self.r, self.theta
        return str(self.x)+","+str(self.y)

    def get_coordcart(self):
        return(self.x,self.y)

    def get_coordpol(self):
        return(self.r,self.theta)





