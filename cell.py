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
import os

state=True
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

        self.monboutonSTOP=Button(self.window,text='Stop',command=self.end) #self.window.quit
        self.monboutonSTOP.pack(side="left")

        self.monboutonTHEORIE=Button(self.window,text='Donnees theoriques',command=self.end) #self.window.quit
        self.monboutonTHEORIE.pack(side="right")

        self.monboutonSIMULATIONS=Button(self.window,text='Resume des simulations',command=self.res_sim) #self.window.quit
        self.monboutonSIMULATIONS.pack(side="right")

        self.monboutonRESTART=Button(self.window,text='Lancer',command=self.start) #self.window.quit
        self.monboutonRESTART.pack(side="left")

        #table of monomers
        self.monomers=[objet.monomer() for i in xrange(constant.NB_MONO)]
        #table of obstacles
        self.obstacles=[objet.obstacle() for i in xrange(constant.NB_OBS)]
        #table of fixed obstacles
        self.fixed=[obstacle_fixed.obstacle_fixed() for i in xrange(constant.NB_FIX)]
        #table of polymers (dictionnary)
        self.polymers={}
        self.nb_polymers=0

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
            i.move(self.monomers, self.obstacles, self.fixed)

        self.nb_polymers=len(self.polymers.keys())

        for i in xrange(constant.NB_OBS):
            self.obstacles[i].update_speed()

        for i in xrange(constant.NB_MONO):
            if self.monomers[i].ispoly==0:
                self.monomers[i].update_speed()

        for i,poly in enumerate(self.polymers.values()):
            poly.update_speed()


    def draw(self):
        if (state):
            self.move()

        #update of points coordinates for the animation
        for i in xrange(constant.NB_MONO):
            self.canevas.coords(self.points_mono[i],self.monomers[i].x-constant.RAYON,self.monomers[i].y-constant.RAYON,self.monomers[i].x+constant.RAYON,self.monomers[i].y+constant.RAYON)

        for i in xrange(constant.NB_OBS):
            self.canevas.coords(self.points_obs[i],self.obstacles[i].x-constant.RAYON -3,self.obstacles[i].y-constant.RAYON,self.obstacles[i].x+constant.RAYON +3,self.obstacles[i].y+constant.RAYON)


        #refreash the window every 10 ms    
        self.window.after(1, self.draw)

    def end(self):

        #save datas into a .txt with all previous simulations
        donnees=open("polymers.txt","a")
        txt=str(constant.NB_MONO)+" "+str(constant.NB_OBS)+" "+str(self.nb_polymers)
        for poly in self.polymers.values():
            txt=txt+" "+str(poly.length)
        txt=txt+"\n"
        donnees.write(txt)
        donnees.close()

        #count how many polymers for each chain length
        length_poly={}
        for poly in self.polymers.values():
            if length_poly.has_key(poly.length):
                length_poly[poly.length]+=1
            else:
                length_poly[poly.length]=1

        donnees2=open("monomers.txt","w")

        for l in length_poly.keys():
            donnees2.write(str(l)+" "+str(length_poly[l])+"\n")

        donnees2.close()

        fichier=open("commandeGNU.txt","w")

        comm2="plot 'monomers.txt' using 1:2 with lines title 'Nombre de polymeres formes en fonction de leur longueur' \n"
        fichier.write(comm2)
        fichier.close()
        os.system("gnuplot "+"commandeGNU.txt --persist")

        #self.window.quit()
        global state
        state=False


    def res_sim(self):
        fichier=open("commandeGNU.txt","w")
        comm1="plot 'polymers.txt' using 1:3 with points title 'Nombre de polymeres formes en fonction du nombre de monomeres initial'\n"
        fichier.write(comm1)
        fichier.close()
        os.system("gnuplot "+"commandeGNU.txt --persist")

        global state
        state=False

    def start(self):
        global state
        state=True




#-------------------------------------------------------------------------------
def simulation():
    envir=cell()
    #print envir
    envir.draw()
    envir.window.mainloop()


#fenetre de depart

windowPRINC=Tk()
windowPRINC.title('Cytoskeleton Modelisation')

FramePRINC = Frame(windowPRINC, borderwidth=2, relief=GROOVE)
FramePRINC.pack(side=LEFT, padx=60, pady=60)

# canevasPRINC=Canvas(windowPRINC, width=2*constant.R+20, height=2*constant.R+20, bg='white')
# canevasPRINC.pack(padx=5,pady=5)

mono_init = Scale(FramePRINC, from_=20, to=100, orient  = HORIZONTAL)
mono_init.pack()



monboutonSTART=Button(FramePRINC,text='Lancer la simulation',command=simulation) #self.window.quit
monboutonSTART.pack(side="left")

constant.NB_MONO = mono_init.get()
print constant.NB_MONO

windowPRINC.mainloop()

