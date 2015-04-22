from __future__ import division
from scipy import * 
from pylab import *
from scipy.integrate import odeint
import os, time

import random
import math
import numpy

SPEED=10
TIME=0.1
W=50 #cell is a 50x50 square
H=50
NB_MONO=10 #number of monomers in the cell

R=50



class monomer:

    def __init__(self):

        #polar coordinates initialized randomly
        self.r=random.random()*R
        self.theta=random.random()*math.pi-(math.pi/2)

        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)
        self.y=self.r*math.sin(self.theta)

    def __repr__(self):
        print self.r, self.theta
        return str(self.x)+","+str(self.y)

    def get_coordcart(self):
        return(self.x,self.y)

    def get_coordpol(self):
        return(self.r,self.theta)

    def update_cart(self):
        self.x=self.r*math.cos(self.theta)
        self.y=self.r*math.sin(self.theta)

    def update_pol(self):
        self.r=math.sqrt(self.x*self.x+self.y*self.y)
        self.theta=math.atan2(self.y,self.x)

    

    def move(self):

        #coordonates of moving vector between -1 and 1
        dr=random.random()*2-1
        dtheta=random.random()*2-1
        norm=math.sqrt(dr*dr+dtheta*dtheta)

        #monomer's speed constant
        dr=dr*SPEED/norm
        dtheta=dtheta*SPEED/norm

        #wind
        if self.r>(R-10):
            dr=dr-1

        #coordonates updated
        self.r=self.r+TIME*dr
        self.theta=self.theta+TIME*dtheta

        self.update_cart()


class boid:

    def __init__(self):
        self.monomers=[monomer() for i in xrange(NB_MONO)]

    def __repr__(self):
        for i in xrange(NB_MONO):
            print self.monomers[i]
        return ""

    def move(self):
        for i in xrange(NB_MONO):
            self.monomers[i].move()

    def draw(self):
        for k in xrange(100):
            self.move()
            for i in xrange(NB_MONO):
                plot(self.monomers[i].x, self.monomers[i].y,'o', color='k')

        filename = 'fichierTemp'+str('%02d' %k)+'.pdf'
        savefig(filename)
        print "Plot",  k
        clf()

        # convert est une fonction d'ImageMagick
        cmd = 'convert -delay 10 -loop 0 fichierTemp*.pdf Modele_animation_003.gif'
        print cmd

        os.system(cmd)
        os.system('del *.pdf')  # destruction des fichiers temporaires
        print "C'est fini !"

#-------------------------------------------------------------------------------

envir=boid()
envir.draw()
