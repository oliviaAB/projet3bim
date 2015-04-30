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

SPEED=20
TIME=0.1 #0.1

NB_MONO=20 #number of monomers in the cell
NB_OBS=5 #number of obstacles in the cell
NB_FIX=1 #number of fixed obstacles in the cell

R=200
RAYON=5
RAYON_FIX=20

CONTACT_MONO=5
CONTACT_OBS=7
CONTACT_FIX=22
CONTACT_POL=8


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

        self.ispoly=0 #to know if the monomer is in a polymer
        self.ishead=-1 #to know if the monomer is the head of the polymer (then ishead=-1), else, to know which monomer is the head of the polymer
                        # if not in a polymer, ishead=-1


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
        self.v1=self.v1*SPEED/norm
        self.v2=self.v2*SPEED/norm

    def wind(self):
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


    def move(self, obstacles, monomers,fixed, polymers, num):
        obs=0
        v1=0
        v2=0


        #if the monomer is not in a polymer
        if self.ispoly==0:

            for i in xrange(NB_OBS):
                if self.near(obstacles[i], CONTACT_OBS)==1:
                    v1=v1+obstacles[i].v1-self.v1
                    v2=v2+obstacles[i].v2-self.v2
                    obs+=1

            for y in xrange(NB_MONO):
                if y!=num:
                # if self.near(monomers[y], CONTACT_MONO)==1:
                #     v1=v1+monomers[y].v1-self.v1
                #     v2=v2+monomers[y].v2-self.v2
                #     obs+=1

                    if self.near(monomers[y], CONTACT_POL)==1:
                        if polymers.has_key(y):
                            new=polymers[y]
                            new.append(y)
                            polymers[num]=new
                            del polymers[y] 
                            self.ispoly=1
                            monomers[y].ishead=num

                        elif monomers[y].ispoly==0:
                            polymers[num]=[y]
                            monomers[y].ishead=num

                        else:
                            v1=v1+monomers[y].v1-self.v1
                            v2=v2+monomers[y].v2-self.v2
                            obs+=1




            fix=0
            for j in xrange(NB_FIX):
                if self.near(fixed[j],CONTACT_FIX)==1:
                    self.v1=-self.v1
                    self.v2=-self.v2
                    fix=1
                    
                
        #if the monomer didn't hit anything, then random movment
            if obs==0:
               self.move_random()


            #else, take into consideration objects hit
            else:
                self.v1=v1/obs
                self.v2=v2/obs
                norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
                self.v1=self.v1*(SPEED+10)/norm
                self.v2=self.v2*(SPEED+10)/norm

            if fix!=0:
                norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
                self.v1=self.v1*(SPEED+10)/norm
                self.v2=self.v2*(SPEED+10)/norm

            self.wind()

            self.x=self.x+TIME*self.v1
            self.y=self.y+TIME*self.v2

        self.update_pol()
                

#-------------------------------------------------------------------------------

class obstacle:

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
        self.v1=self.v1*SPEED/norm
        self.v2=self.v2*SPEED/norm

    def wind(self):
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


    def move(self, obstacles, monomers,fixed,num):
        obs=0
        v1=0
        v2=0

        for i in xrange(NB_OBS):
            if i!=num:
                if self.near(obstacles[i], CONTACT_OBS)==1:
                    v1=v1+obstacles[i].v1-self.v1
                    v2=v2+obstacles[i].v2-self.v2
                    obs+=1

        for y in xrange(NB_MONO):
            if self.near(monomers[y],CONTACT_MONO)==1:
                v1=v1+monomers[y].v1-self.v1
                v2=v2+monomers[y].v2-self.v2
                obs+=1

        for j in xrange(NB_FIX):
            if self.near(fixed[j],CONTACT_FIX)==1:
                self.v1=-self.v1
                self.v2=-self.v2
                
        if obs==0:
            self.move_random()
        else:
            self.v1=v1/obs
            self.v2=v2/obs
            norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
            self.v1=self.v1*(SPEED+10)/norm
            self.v2=self.v2*(SPEED+10)/norm

        self.wind()

        self.x=self.x+TIME*self.v1
        self.y=self.y+TIME*self.v2

        self.update_pol()                

#-----------------------------------------------------------------------------

class obstacle_fixed:

    def __init__(self):
        
        #polar coordinates initialized randomly
        self.r=random.random()*(R-RAYON_FIX) #to prevent fixed obstacles from being on the limit of the cell
        self.theta=random.random()*math.pi-(math.pi/2)

        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)+R
        self.y=self.r*math.sin(self.theta)+R

    def __repr__(self):
        print self.r, self.theta
        return str(self.x)+","+str(self.y)

    def get_coordcart(self):
        return(self.x,self.y)

    def get_coordpol(self):
        return(self.r,self.theta)

#-----------------------------------------------------------------------------

class cell:

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
        #table of obstacles
        self.obstacles=[obstacle() for i in xrange(NB_OBS)]
        #table of fixed obstacles
        self.fixed=[obstacle_fixed() for i in xrange(NB_FIX)]
        #table of polymers (dictionnary)
        self.polymers={}

        #table of circles to draw for each monomer
        self.points_mono=[self.canevas.create_oval(self.monomers[i].x-RAYON,self.monomers[i].y-RAYON,self.monomers[i].x+RAYON,self.monomers[i].y+RAYON,width=1,outline='blue',fill='blue') for i in xrange(NB_MONO)]
        #table of circles to draw for each obstacle
        self.points_obs=[self.canevas.create_oval(self.obstacles[i].x-RAYON,self.obstacles[i].y-RAYON,self.obstacles[i].x+RAYON,self.obstacles[i].y+RAYON ,width=1,outline='green',fill='green') for i in xrange(NB_OBS)]
        #table of circles to draw for each fixed obstacle
        self.points_fix=[self.canevas.create_oval(self.fixed[i].x-RAYON_FIX,self.fixed[i].y-RAYON_FIX,self.fixed[i].x+RAYON_FIX,self.fixed[i].y+RAYON_FIX,width=1,outline='red',fill='red') for i in xrange(NB_FIX)]


    def __repr__(self):
        for i in xrange(NB_MONO):
            print self.monomers[i]
        return ""

    def move(self):
        for i in xrange(NB_OBS):
            self.obstacles[i].move(self.obstacles,self.monomers,self.fixed,i)
            #print "OBS", self.obstacles[i].v1,self.obstacles[i].v2
            
        for i in xrange(NB_MONO):
            self.monomers[i].move(self.obstacles,self.monomers,self.fixed, self.polymers, i)
            #print "MONO", self.monomers[i].v1,self.monomers[i].v2

    def draw(self):
        self.move()

        #update of points coordinates for the animation
        for i in xrange(NB_MONO):
            self.canevas.coords(self.points_mono[i],self.monomers[i].x-RAYON,self.monomers[i].y-RAYON,self.monomers[i].x+RAYON,self.monomers[i].y+RAYON)

        for i in xrange(NB_OBS):
            self.canevas.coords(self.points_obs[i],self.obstacles[i].x-RAYON -3,self.obstacles[i].y-RAYON,self.obstacles[i].x+RAYON +3,self.obstacles[i].y+RAYON)


        #refreash the window every 10 ms    
        self.window.after(10, self.draw)
        




#-------------------------------------------------------------------------------

envir=cell()
print envir
envir.draw()
envir.window.mainloop()
