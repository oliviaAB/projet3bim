import random
import math
import constant

class polymer:

    def __init__(self,monhead,monnext,dic):

        self.chain={} #key: monomer rank in polymer
                      #value: monomer
        self.length=2
        self.v1=monhead.v1
        self.v2=monhead.v2
        # self.v1_next=0
        # self.v2_next=0

        self.chain[0]=monnext
        self.chain[1]=monhead

        monhead.ishead=1
        monhead.ispoly=1
        monnext.ispoly=1

        dic[self.chain[1]]=self

        #to make sure the two monomers are at a distance 
        #of 2*RAYON-0.5 from each other
        vx=self.chain[1].x-self.chain[0].x
        vy=self.chain[1].y-self.chain[0].y
        norm=math.sqrt(vx*vx+vy*vy)
        vx=vx/norm
        vy=vy/norm

        self.chain[1].x=self.chain[0].x+2*vx*(constant.RAYON-0.5)
        self.chain[1].y=self.chain[0].y+2*vy*(constant.RAYON-0.5)

    def add(self,monnext,dic):

        #Add monomer monnext in the chain
        self.chain[self.length]=monnext
        monnext.ishead=1 #now monnext is the head
        monnext.ispoly=1 #now monnext is in a polymer
        self.chain[self.length-1].ishead=0 #previous head is 
                        #no longer the head


        #the new monomer aligns with the chain
        vx=self.chain[self.length-1].x-self.chain[self.length-2].x
        vy=self.chain[self.length-1].y-self.chain[self.length-2].y
        norm=math.sqrt(vx*vx+vy*vy)
        vx=vx/norm
        vy=vy/norm

        self.chain[self.length].x=self.chain[self.length-1].x+2*vx*(constant.RAYON-0.5)
        self.chain[self.length].y=self.chain[self.length-1].y+2*vy*(constant.RAYON-0.5)

        del dic[self.chain[self.length-1]]
        dic[monnext]=self

        self.length+=1


    def update_speed(self):

        for mono in self.chain.values():
            mono.v1=self.v1*(constant.SPEED)
            mono.v2=self.v2*(constant.SPEED)
            #mono.update_speed()
            mono.x=mono.x+constant.TIME*self.v1
            mono.y=mono.y+constant.TIME*self.v2

            mono.update_pol() 

    def move(self,monomers, obstacles,fixed):

        obs=0
        v1=0
        v2=0


        for mono in self.chain.values():
            for i in xrange(constant.NB_OBS):
                if mono.near(obstacles[i], constant.CONTACT_OBS)==1:
                    v1=v1+obstacles[i].v1-self.v1
                    v2=v2+obstacles[i].v2-self.v2
                    obs+=1

            for y in xrange(constant.NB_MONO):
                if monomers[y] not in self.chain.values():
                    if mono.near(monomers[y],constant.CONTACT_MONO)==1:
                        v1=v1+monomers[y].v1-self.v1
                        v2=v2+monomers[y].v2-self.v2
                        obs+=1


        if obs==0:
            self.v1=self.v1+(random.random()*2-1)*5
            self.v2=self.v2+(random.random()*2-1)*5
        else:
            self.v1=v1/obs
            self.v2=v2/obs


        fix=0
        for mono in self.chain.values():
            for i in xrange(constant.NB_FIX):
                if mono.near(fixed[i],constant.CONTACT_FIX):
                    fix=1

        if fix!=0:
            self.v1=-self.v1
            self.v2=-self.v2


        wind=0
        i=0
        while i<self.length and wind==0:
            if self.chain[i].r>(constant.R-50):
                wind=1
            i+=1

        if wind !=0:    
            braking=(50-(constant.R-self.chain[i-1].r-10))
            
            if self.chain[i-1].x>constant.R:
                #top right quarter
                if self.chain[i-1].y<constant.R:
                    self.v1=self.v1-braking
                    self.v2=self.v2+braking
                    
                #bottom right quarter
                if self.chain[i-1].y>constant.R:
                    self.v1=self.v1-braking
                    self.v2=self.v2-braking

            #left half
            if self.chain[i-1].x<constant.R:
                #top left quarter
                if self.chain[i-1].y<constant.R:
                    self.v1=self.v1+braking
                    self.v2=self.v2+braking

                #bottom left quarter
                if self.chain[i-1].y>constant.R:
                    self.v1=self.v1+braking
                    self.v2=self.v2-braking
       
        
        if self.v1==0 and self.v2==0:
            print '000000'
        norm=math.sqrt(self.v1*self.v1+self.v2*self.v2)

        #monomer's speed constant
        self.v1=self.v1*constant.SPEED/norm
        self.v2=self.v2*constant.SPEED/norm

        # for mono in self.chain.values():
        #     mono.v1_next=self.v1
        #     mono.v2_next=self.v2

