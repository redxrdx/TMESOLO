# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 17:05:52 2016

@author: 3200404
"""
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import Vector2D
from soccersimulator import settings
from tools import *



# commandes basiques : 

def finition(MyState):
    return MyState.finition()
    
def conserver(MyState):
    return MyState.conserver2() 
    
def tirer(MyState):
    return MyState.tir_but()
    
def dribbler(MyState):
    MyState.dribbler() 
    

def passer(MyState):
   if (MyState.faire_passe() == True) :  
     print("faire passe ok")
     return MyState.passer()
   else : 
       return MyState.conserver2();
  


  # attaquant  
def position(MyState):
    return MyState.avant_centre()
 


  #gardien
    
def posG(MyState):
    return MyState.positionG()
def posGH(MyState):
    return MyState.positionGH()
def posGB(MyState):
    return MyState.positionGB()
def degG(MyState):
    return MyState.degager()
    
    
#classes :

def goal(MyState):   
      
     
   if (MyState.dans_perimetre() == 1 and MyState.sortieGardien() == 1   and MyState.distance_au_joueur() == 1) :
     
      return MyState.degager()
   
   elif (MyState.zone_cage() == 1):
        return MyState.suivre_jeuG()
   elif(MyState.position_balle().y < (settings.GAME_HEIGHT/2)-5):
       return MyState.positionGB()
   elif(MyState.position_balle().y > (settings.GAME_HEIGHT/2)+5):
       return MyState.positionGH()
   else:
  
      return MyState.positionG()
       
      
      
def scoreG(MyState):
   
  x = Vector2D(settings.GAME_WIDTH*3/4,settings.GAME_HEIGHT/2) 
  if (MyState.balle_chez_adv()) :
     if (MyState.dans_perimetre() == 1 or MyState.position_balle().x > settings.GAME_WIDTH - 50):
        
         return MyState.tir_but()
     else:
         return MyState.conserver2()
  else:
       return MyState.aller_vers(x)     
    
    
def defence(MyState):
 
 if (MyState.balle_chez_nous()) :
     
     y = Vector2D(settings.GAME_WIDTH/2,settings.GAME_HEIGHT/4) 
   
     if MyState.balle_en_def() == 1:   
     
         return MyState.tirer_vers(y)
     else :
         return MyState.defendre()
 
 else:
    return MyState.suivre_jeu()
 
     


def fullStrike(MyState) :
  
  
   x = Vector2D(settings.GAME_WIDTH*3/4,settings.GAME_HEIGHT/2.) 
  
   if MyState.balle_chez_nous():    
     
     if MyState.balle_au_mil() == 1:   
     
         return MyState.aller_vers(x) + MyState.tir_but()
     else:
         return MyState.avant_centre()
    
   elif MyState.balle_chez_adv() :
    
    if MyState.position_balle().x <=(settings.GAME_WIDTH*2)/3:
      return MyState.avant_centre()   
    else :
      return MyState.tir_but()
#           
#     return MyState.avant_centre()      
# 
# if MyState.balle_chez_adv() :
#
#   if (MyState.dans_perimetre() == 1 or MyState.position_balle().x > settings.GAME_WIDTH - 50):
#        return MyState.marquer()       
#   else :
#        return MyState.avant_centre()    
# elif(MyState.balle_chez_nous()):
#     
#     return MyState.avant_centre()      
# 
def j1(MyState):
     if MyState.balle_chez_nous():    
         if (MyState.distance_balle < 5):
             return MyState.conserver2()
         else:
             return MyState.defendre()
     else:
        if (MyState.position_balle().x > settings.GAME_WIDTH - 50):
            return MyState.tir_but()
        else:
            return MyState.conserver2()
    
    
def millieu(MyState) :
   
   x = Vector2D(settings.GAME_WIDTH*3/4,settings.GAME_HEIGHT/2) 
   y = Vector2D(settings.GAME_WIDTH/2,settings.GAME_HEIGHT/4.) 
   
   if MyState.balle_chez_nous():    
     
     if MyState.balle_en_def() == 1:   
     
         return MyState.aller_vers(y) + MyState.tirer_vers(x)
     else:
         return MyState.tirer_vers(x)
    
   elif MyState.balle_chez_adv() :
      if MyState.balle_au_mil() == 1:   
     
         return   MyState.tirer_vers(x)
         
      if MyState.position_balle().x <(settings.GAME_WIDTH)/1.5 :
        return MyState.tir_but()  
      else :
        return MyState.suivre_jeuM()
       


       
def lateral(MyState) :
  if (MyState.balle_chez_adv()) :    
    if MyState.centrerH() :
       
        return MyState.tirer_centreH()
   
   
    if MyState.centrerB() : 
        
        return MyState.tirer_centreB()
    else:
        return MyState.aller_centrer()        
        
  else:
           return  MyState.conserver()
           
           
def Dcentral(MyState):
  
  if MyState.balle_chez_nous():    
    
    if (MyState.distance_au_joueur() == 1 ):
         return MyState.dj2()
    elif(MyState.position_balle().x < 20 and MyState.distance_au_joueur() == 0 ):
         return MyState.defendre()
    else:    
         return MyState.positionDC()
  else:
      return MyState.positionDC()