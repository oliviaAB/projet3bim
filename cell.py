#------------------------------------------------------------------------------
#                                 Projet 3BIM
#                          Cytoskeleton modelisation
#              ANGELIN-BONNET Olivia, GURJAO CARINO, PIAT Alexis
#------------------------------------------------------------------------------

# Hypotheses:
# 1: aux bords de la cellule, les monomeres subissent du "vent": le bord est plus
#     visqueux, ils ralentissent tout en etant devies de leur trajectoire avec
#     une force proportionnelle a leur proximite a la membrane

# 2: Lorsqu'un monomere percute un obstacle (cad lorsqu'il est suffisamment proche,
#     ils rebondissent l'un contre l'autre



from Tkinter import *

import random
import math
#import numpy
#import monomer
import constant
#import obstacle
import polymer
import obstacle_fixed
import objet
#-----------------------------------------------------------------------------

class cell:

    def __init__(self):

        #creation of window for animation
        self.window=Tk()
        self.window.title('cytoskeleton')

        #creation of the cell outline
        self.canevas=Canvas(self.window, width=2*constant.R+20, height=2*constant.R+20, bg='white')
        self.canevas.pack(padx=5,pady=5)
        center=constant.R+10
        self.canevas.create_oval(center-constant.R,center-constant.R,center+constant.R,center+constant.R,outline="black",fill="white")

        #table of monomers
        self.monomers=[objet.monomer(i) for i in xrange(constant.NB_MONO)]
        #table of obstacles
        self.obstacles=[objet.obstacle(i) for i in xrange(constant.NB_OBS)]
        #table of fixed obstacles
        self.fixed=[obstacle_fixed.obstacle_fixed() for i in xrange(constant.NB_FIX)]
        #table of polymers (dictionnary)
        self.polymers={}

        #table of circles to draw for each monomer
        self.points_mono=[self.canevas.create_oval(self.monomers[i].x-constant.RAYON,self.monomers[i].y-constant.RAYON,self.monomers[i].x+constant.RAYON,self.monomers[i].y+constant.RAYON,width=1,outline='blue',fill='blue') for i in xrange(constant.NB_MONO)]
        #table of circles to draw for each obstacle
        self.points_obs=[self.canevas.create_oval(self.obstacles[i].x-constant.RAYON,self.obstacles[i].y-constant.RAYON,self.obstacles[i].x+constant.RAYON,self.obstacles[i].y+constant.RAYON ,width=1,outline='green',fill='green') for i in xrange(constant.NB_OBS)]
        #table of circles to draw for each fixed obstacle
        self.points_fix=[self.canevas.create_oval(self.fixed[i].x-constant.RAYON_FIX,self.fixed[i].y-constant.RAYON_FIX,self.fixed[i].x+constant.RAYON_FIX,self.fixed[i].y+constant.RAYON_FIX,width=1,outline='red',fill='red') for i in xrange(constant.NB_FIX)]


    def __repr__(self):
        for i in xrange(constant.NB_MONO):
            print self.monomers[i]
        return ""

    def contact(self, monoA, monoB):
        centerx=(monoA.x+monoB.x)/2
        centery=(monoA.y+monoB.y)/2

                    #vector bewteen the two monomers
        vectx=monoA.x-monoB.x
        vecty=monoA.y+monoB.y

        normvect=math.sqrt(vectx*vectx+vecty*vecty)
        nx=vectx/normvect
        ny=vecty/normvect
 
        gx=-ny
        gy=nx

        vAn=nx*monoA.v1+ny*monoA.v2
        vAg=gx*monoA.v1+gy*monoA.v2
                    
        vBn=nx*monoB.v1+ny*monoB.v2
        vBg=gx*monoB.v1+gy*monoB.v2

        save=vAn

        vAn=vBn
        vBn=save

        vAx=nx*vAn+gx*vAg
        vAy=ny*vAn+gy*vAg
        normA=math.sqrt(vAx*vAx+vAy*vAy)


        vBx=nx*vBn+gx*vBg
        vBy=ny*vBn+gy*vBg
        normB=math.sqrt(vBx*vBx+vBy*vBy)

        monoA.v1=vAx/normA
        monoA.v2=vAy/normB

        monoB.v1=vBx/normB
        monoB.v2=vBy/normB

        monoA.x=monoA.x+constant.TIME*monoA.v1
        monoA.y=monoA.y+constant.TIME*monoA.v2

        monoA.update_pol()

        monoB.x=monoB.x+constant.TIME*monoB.v1
        monoB.y=monoB.y+constant.TIME*monoB.v2

        monoB.update_pol()


    def move(self):
        for i in xrange(constant.NB_OBS):
            self.obstacles[i].move(self.obstacles,self.monomers,self.fixed,i)
            #print "OBS", self.obstacles[i].v1,self.obstacles[i].v2
            
        for i in xrange(constant.NB_MONO):
            self.monomers[i].move(self.obstacles,self.monomers,self.fixed, self.polymers, i)
            #print "MONO", self.monomers[i].v1,self.monomers[i].v2

        for i in self.polymers.values():
            i.move(self. monomers, self.obstacles, self.fixed)


        for monoA in self.monomers:
            for  monoB in self.monomers:
                if monoA.num!=monoB.num and monoA.near(monoB, constant.CONTACT_MONO)==1:
                    self.contact(monoA,monoB)

            for obs in self.obstacles:
                if monoA.near(obs, constant.CONTACT_OBS):
                    self.contact(monoA, obs)


        for obsA in self.obstacles:
            for obsB in self.obstacles:
                if obsA.num!=obsB.num and obsA.near(obsB, constant.CONTACT_OBS)==1:
                    self.contact(obsA, obsB)


    def draw(self):
        self.move()

        #update of points coordinates for the animation
        for i in xrange(constant.NB_MONO):
            self.canevas.coords(self.points_mono[i],self.monomers[i].x-constant.RAYON,self.monomers[i].y-constant.RAYON,self.monomers[i].x+constant.RAYON,self.monomers[i].y+constant.RAYON)

        for i in xrange(constant.NB_OBS):
            self.canevas.coords(self.points_obs[i],self.obstacles[i].x-constant.RAYON -3,self.obstacles[i].y-constant.RAYON,self.obstacles[i].x+constant.RAYON +3,self.obstacles[i].y+constant.RAYON)


        #refreash the window every 10 ms    
        self.window.after(10, self.draw)


#-------------------------------------------------------------------------------

envir=cell()
print envir
envir.draw()
envir.window.mainloop()


