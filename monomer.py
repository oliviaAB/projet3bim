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
import constant
#import numpy



class monomer:

    def __init__(self):
        
        #polar coordinates initialized randomly
        self.r=random.random()*constant.R
        self.theta=random.random()*math.pi-(math.pi/2)

        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)+constant.R
        self.y=self.r*math.sin(self.theta)+constant.R

        self.v1=random.random()*2-1
        self.v2=random.random()*2-1

        self.ispoly=0 #to know if the monomer is in a polymer
        self.ishead=0 #to know if the monomer is the head of the polymer (then ishead=-1), else, to know which monomer is the head of the polymer
                        # if not in a polymer, ishead=-1


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


    def move(self, obstacles, monomers,fixed, polymers, num):
        obs=0
        v1=0
        v2=0


        #if the monomer is not in a polymer
        if self.ispoly==0:

            for i in xrange(constant.NB_OBS):
                if self.near(obstacles[i], constant.CONTACT_OBS)==1:
                    v1=v1+obstacles[i].v1-self.v1
                    v2=v2+obstacles[i].v2-self.v2
                    obs+=1

            for y in xrange(constant.NB_MONO):
                if y!=num:
                # if self.near(monomers[y], CONTACT_MONO)==1:
                #     v1=v1+monomers[y].v1-self.v1
                #     v2=v2+monomers[y].v2-self.v2
                #     obs+=1

                    if self.near(monomers[y], constant.CONTACT_POL)==1:

                        #if the monomer self hits is already the head of a polymer
                        #if monomers[y].ishead==1:
                        if polymers.has_key(monomers[y]):

                            polymers[monomers[y]].add(monomers[num],polymers)
                            vectX=(polymers[monomers[num]].next[-1].x-polymers[monomers[num]].next[-2].x)
                            vectY=(polymers[monomers[num]].next[-1].y-polymers[monomers[num]].next[-2].y)
                            normvect=math.sqrt(vectX*vectX+vectY*vectY)
                            vectX=vectX/normvect
                            vectY=vectY/normvect
                            self.x=polymers[monomers[num]].next[-1].x+vectX*constant.CONTACT_MONO
                            self.y=polymers[monomers[num]].next[-1].y+vectY*constant.CONTACT_MONO
                            # normY=math.sqrt(monomers[y].v1*monomers[y].v1+monomers[y].v2*monomers[y].v2)
                            # self.x=monomers[y].x+monomers[y].v1*CONTACT_MONO/normY
                            # self.y=monomers[y].y+monomers[y].v2*CONTACT_MONO/normY
                            
                            #print "HAAAAAAAAA"

                            # new=polymers[y]
                            # new.append(y)
                            # polymers[num]=new
                            # del polymers[y] 
                            # self.ispoly=1
                            # monomers[y].ishead=num

                         #if the monomer self hits is alone
                        elif monomers[y].ispoly==0:
                            polymers[monomers[num]]=polymer(monomers[num],monomers[y])
                            #print monomers[num].ishead
                            #print polymers.has_key(monomers[num])


                        else:
                            v1=v1+monomers[y].v1-self.v1
                            v2=v2+monomers[y].v2-self.v2
                            obs+=1




            fix=0
            for j in xrange(constant.NB_FIX):
                if self.near(fixed[j],constant.CONTACT_FIX)==1:
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
                self.v1=self.v1*(constant.SPEED+10)/norm
                self.v2=self.v2*(constant.SPEED+10)/norm

            if fix!=0:
                norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
                self.v1=self.v1*(constant.SPEED+10)/norm
                self.v2=self.v2*(constant.SPEED+10)/norm

            self.wind()

            self.x=self.x+constant.TIME*self.v1
            self.y=self.y+constant.TIME*self.v2

        self.update_pol()
                

#-------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------


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


    def move(self):

        #Update the header speed

        #coordonates of moving vector between -1 and 1
        self.head.v1=self.head.v1+(random.random()*2-1)*5
        self.head.v2=self.head.v2+(random.random()*2-1)*5
        norm=math.sqrt(self.head.v1*self.head.v1+self.head.v2*self.head.v2)

        #monomer's speed constant
        self.head.v1=self.head.v1*constant.SPEED/norm
        self.head.v2=self.head.v2*constant.SPEED/norm

        self.head.wind()

        self.head.x=self.head.x+constant.TIME*self.head.v1
        self.head.y=self.head.y+constant.TIME*self.head.v2


        self.head.update_pol()

        #Update the polymer speed

        for mono in self.next:
            mono.v1=self.head.v1
            mono.v2=self.head.v2

            mono.x=mono.x+constant.TIME*mono.v1
            mono.y=mono.y+constant.TIME*mono.v2

            mono.update_pol()


