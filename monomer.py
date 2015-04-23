##from __future__ import division
##from scipy import * 
##from pylab import *
##from scipy.integrate import odeint
##import os, time

from Tkinter import *

import random
import math
#import numpy

SPEED=20
TIME=0.1 #0.01
NB_MONO=10 #number of monomers in the cell

R=200
RAYON=5



class monomer:

    def __init__(self):
        
        #polar coordinates initialized randomly
        self.r=random.random()*R
        self.theta=random.random()*math.pi-(math.pi/2)

        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)+R
        self.y=self.r*math.sin(self.theta)+R

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
        self.x=self.r*math.cos(self.theta)+R
        self.y=self.r*math.sin(self.theta)+R

    def update_pol(self):
        x=self.x-R
        y=self.y-R
        self.r=math.sqrt(x*x+y*y)
        self.theta=math.atan2(y,x)
        #print self.r
##        self.r=math.sqrt(self.x*self.x+self.y*self.y)
##        self.theta=math.atan2(self.y,self.x)

    def move(self):

        #coordonates of moving vector between -1 and 1
        self.v1=self.v1+(random.random()*2-1)*5
        self.v2=self.v2+(random.random()*2-1)*5
        norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)

        #monomer's speed constant
        self.v1=self.v1*SPEED/norm
        self.v2=self.v2*SPEED/norm

        #wind
        if self.r>(R-50):
            braking=(50-(R-self.r))/5
            #print braking
            
            if self.x>R:
                #top right quarter
                if self.y<R:
                    self.v1=self.v1-braking
                    self.v2=self.v2+braking
                    
                #bottom right quarter
                if self.y>R:
                    self.v1=self.v1-braking
                    self.v2=self.v2-braking

            #left half
            if self.x<R:
                #top left quarter
                if self.y<R:
                    self.v1=self.v1+braking
                    self.v2=self.v2+braking

                #bottom left quarter
                if self.y>R:
                    self.v1=self.v1+braking
                    self.v2=self.v2-braking


        #coordonates updated
        #self.r=self.r+TIME*self.v1
        #self.theta=self.theta+TIME*self.v2
        self.x=self.x+TIME*self.v1
        self.y=self.y+TIME*self.v2

        #print self.v1, self.v2

        #self.update_cart()
        self.update_pol()

#-------------------------------------------------------------------------------


class boid:

    def __init__(self):

        #creation of window for animation
        self.window=Tk()
        self.window.title('cytoskeleton')

        #creation of the cell outline
        self.canevas=Canvas(self.window, width=2*R+20, height=2*R+20, bg='white')
        self.canevas.pack(padx=5,pady=5)
        center=R+10
        self.canevas.create_oval(center-R,center-R,center+R,center+R,outline="black",fill="white")

        #table of monomers
        self.monomers=[monomer() for i in xrange(NB_MONO)]

    #table of circles to draw for each monomer
        self.points=[self.canevas.create_oval(self.monomers[i].x-RAYON,self.monomers[i].y-RAYON,self.monomers[i].x+RAYON,self.monomers[i].y+RAYON,width=1,outline='blue',fill='blue') for i in xrange(NB_MONO)]


    def __repr__(self):
        for i in xrange(NB_MONO):
            print self.monomers[i]
        return ""

    def move(self):
        for i in xrange(NB_MONO):
            self.monomers[i].move()

    def draw(self):
        self.move()

        #update of points coordinates for the animation
        for i in xrange(NB_MONO):
            self.canevas.coords(self.points[i],self.monomers[i].x-RAYON,self.monomers[i].y-RAYON,self.monomers[i].x+RAYON,self.monomers[i].y+5)

        #refreash the window every 10 ms    
        self.window.after(10, self.draw)
        




#-------------------------------------------------------------------------------

envir=boid()
print envir
envir.draw()
envir.window.mainloop()
