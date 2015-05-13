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
import monomer
import constant
import obstacle
import polymer
import obstacle_fixed
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
        self.monomers=[monomer.monomer() for i in xrange(constant.NB_MONO)]
        #table of obstacles
        self.obstacles=[obstacle.obstacle() for i in xrange(constant.NB_OBS)]
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

    def move(self):
        for i in xrange(constant.NB_OBS):
            self.obstacles[i].move(self.obstacles,self.monomers,self.fixed,i)
            #print "OBS", self.obstacles[i].v1,self.obstacles[i].v2
            
        for i in xrange(constant.NB_MONO):
            self.monomers[i].move(self.obstacles,self.monomers,self.fixed, self.polymers, i)
            #print "MONO", self.monomers[i].v1,self.monomers[i].v2

        for i in self.polymers.values():
            i.move()

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


