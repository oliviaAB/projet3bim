import random
import math


SPEED=10
TIME=0.1
W=50 #cell is a 50x50 square
H=50
NB_MONO=10 #number of monomers in the cell



class monomer:

    def __init__(self):

        #coordonnates initialized in the cell
        self.x=random.uniform(0,W)
        self.y=random.uniform(0,H)

    def __repr__(self):
        #print self.x, self.y
        return str(self.x)+","+str(self.y)

    def get__coord(self):
        return(self.x,self.y)

    def move(self):

        #coordonates of moving vector between -1 and 1
        dx=random.random()*2-1
        dy=random.random()*2-1
        norm=math.sqrt(dx*dx+dy*dy)

        #monomer's speed constant
        dx=dx*SPEED/norm
        dy=dy*SPEED/norm

        self.x=self.x+TIME*dx
        self.y=self.y+TIME*dy


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

#-------------------------------------------------------------------------------

envir=boid()
print envir
envir.move()
print envir
