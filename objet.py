from Tkinter import *

import random
import math
import constant
import polymer

class objet:

    def __init__(self):
       
    	#polar coordinates initialized randomly
        self.r=random.random()*constant.R
        self.theta=random.random()*math.pi-(math.pi/2)
        #cartesian coordinates updated
        self.x=self.r*math.cos(self.theta)+constant.R
        self.y=self.r*math.sin(self.theta)+constant.R

        self.v1=random.random()*2-1
        self.v2=random.random()*2-1

        self.v1_next=0
        self.v2_next=0

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
        self.v1_next=self.v1+(random.random()*2-1)*5
        self.v2_next=self.v2+(random.random()*2-1)*5
        norm=math.sqrt(self.v1_next*self.v1_next+self.v2_next*self.v2_next)

        #monomer's speed constant
        self.v1_next=self.v1_next*constant.SPEED/norm
        self.v2_next=self.v2_next*constant.SPEED/norm

    def wind(self):
        if self.r>(constant.R-50):
            braking=(50-(constant.R-self.r))*constant.SPEED/20
            #print braking
            
            if self.x>constant.R:
                #top right quarter
                if self.y<constant.R:
                    self.v1_next=self.v1-braking
                    self.v2_next=self.v2+braking
                    
                #bottom right quarter
                if self.y>constant.R:
                    self.v1_next=self.v1-braking
                    self.v2_next=self.v2-braking

            #left half
            if self.x<constant.R:
                #top left quarter
                if self.y<constant.R:
                    self.v1_next=self.v1+braking
                    self.v2_next=self.v2+braking

                #bottom left quarter
                if self.y>constant.R:
                    self.v1_next=self.v1+braking
                    self.v2_next=self.v2-braking

    def update_speed(self):

        norm=math.sqrt(self.v1_next*self.v1_next+self.v2_next*self.v2_next)
        self.v1=self.v1_next*(constant.SPEED)/norm
        self.v2=self.v2_next*(constant.SPEED)/norm

        if self.v1==0 and self.v2==0:
            print '000000'

        self.x=self.x+constant.TIME*self.v1
        self.y=self.y+constant.TIME*self.v2

        self.update_pol() 


#-------------------------------------------------------------------


class obstacle(objet):

    def __init__(self):

        objet.__init__(self)


    def move(self, obstacles, monomers,fixed, num):

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
                
        if obs==0:
            self.move_random()
        else:
            self.v1_next=v1/obs
            self.v2_next=v2/obs
            # norm=math.sqrt(self.v1_next*self.v1_next+self.v2_next*self.v2_next)
            # self.v1_next=self.v1_next*(constant.SPEED+10)/norm
            # self.v2_next=self.v2_next*(constant.SPEED+10)/norm

        for j in xrange(constant.NB_FIX):
            if self.near(fixed[j],constant.CONTACT_FIX)==1:
                self.v1_next=-self.v1
                self.v2_next=-self.v2

        self.wind()

        # self.x=self.x+constant.TIME*self.v1
        # self.y=self.y+constant.TIME*self.v2

        # self.update_pol()   


#-------------------------------------------------------------------


class monomer(objet):

    def __init__(self):
        objet.__init__(self)

        self.ispoly=0 #to know if the monomer is in a polymer
        self.ishead=0 #to know if the monomer is the head of the polymer (then ishead=-1), else, to know which monomer is the head of the polymer
                        # if not in a polymer, ishead=-1

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
                        if monomers[y].ishead==1:
                            polymers[monomers[y]].add(monomers[num],polymers)

                            #print "HAAAAAAAAA"

                            # new=polymers[y]
                            # new.append(y)
                            # polymers[num]=new
                            # del polymers[y] 
                            # self.ispoly=1
                            # monomers[y].ishead=num

                         #if the monomer self hits is alone
                        elif monomers[y].ispoly==0:
                            polymers[monomers[num]]=polymer.polymer(monomers[num],monomers[y],polymers)
                            #print monomers[num].ishead
                            #print polymers.has_key(monomers[num])


                        else:
                            v1=v1+monomers[y].v1-self.v1
                            v2=v2+monomers[y].v2-self.v2
                            obs+=1


                    
                
        #if the monomer didn't hit anything, then random movment
            if obs==0:
               self.move_random()


            #else, take into consideration objects hit
            elif obs!=0:
                self.v1_next=v1/obs
                self.v2_next=v2/obs
                # norm=math.sqrt(self.v1_next*self.v1_next+self.v2_next*self.v2_next)
                # self.v1_next=self.v1_next*(constant.SPEED+10)/norm
                # self.v2_next=self.v2_next*(constant.SPEED+10)/norm

            # if fix!=0:
            #     norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)
            #     self.v1_next=self.v1_next*(constant.SPEED+10)/norm
            #     self.v2_next=self.v2_next*(constant.SPEED+10)/norm



            fix=0
            for j in xrange(constant.NB_FIX):
                if self.near(fixed[j],constant.CONTACT_FIX)==1:
                    self.v1_next=-self.v1
                    self.v2_next=-self.v2
                    fix=1

            self.wind()

            # self.x=self.x+constant.TIME*self.v1
            # self.y=self.y+constant.TIME*self.v2

            # self.update_pol()
