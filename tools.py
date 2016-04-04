# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:09:00 2016

@author: 3200404
"""

from soccersimulator import SoccerAction
from soccersimulator import Vector2D
from soccersimulator import settings
import math
import random



def miroir_p(p):       # miroir position
    return Vector2D( settings.GAME_WIDTH - p.x,p.y)

        # miroir vecteur
def miroir_v(v):
    return Vector2D(-1*v.x , v.y)  
    
def miroir_sa(action):
    return SoccerAction(miroir_v(action.acceleration),miroir_v(action.shoot))
    
def miroir_st(state):
    res = state.copy()
    res.ball.position = miroir_p(state.ball.position)
    res.ball.vitesse = miroir_v(state.ball.vitesse)
    for (id_team, id_player) in state.players :
        (res.player_state(id_team,id_player)).position = miroir_p(state.player_state(id_team,id_player).position)
        (res.player_state(id_team,id_player)).vitesse = miroir_v(state.player_state(id_team,id_player).vitesse)
    return res    
    
    
class PlayerDecorator :
    
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    

# position joueur et balle    
    def position_joueur(self):
          return self.state.player_state(self.id_team, self.id_player).position  

    def position_balle(self):
        return self.state.ball.position
    
    def distance_balle(self):
        return self.position_joueur().distance(self.state.ball.position)     


#positions pour corner    
    def cornerX(self):
        if (self.position_balle().x >= settings.GAME_WIDTH-10):
            return 1
        else:
            return 0
        
    def cornerYH(self):
        if( self.position_balle().y >= (settings.GAME_HEIGHT - 10) ):
            return 1
        else:
             return 0
          
    def cornerYB(self):
   
       if(self.position_balle().y <= (settings.GAME_HEIGHT - 80) ):
        return 1
       else :
        return 0
        
# actions concernant la balle
        
        
    def balle_chez_adv(self):
        if (self.position_balle().x >= settings.GAME_WIDTH / 2):
            return True
        else:
            return False
  
    def chercher_balle(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.non_tir())
    
    def rien(self):
        return SoccerAction(0,0)
    
    def possede_balle(self):
        if(self.distance_balle() < (settings.PLAYER_RADIUS + settings.BALL_RADIUS) ) :
          return True
        else:
            return False
        
    def balle_chez_nous(self):
         if (self.position_balle().x < settings.GAME_WIDTH / 2):
            return True
         else:
            return False
    
    def balle_en_def(self):
         if (self.position_balle().x < settings.GAME_WIDTH / 4):
            return 1
         else:
            return 0
      
    def balle_au_mil(self):
         if (self.position_balle().x <= settings.GAME_WIDTH / 2.5 and self.position_balle().x >= settings.GAME_WIDTH / 1.5 ):
            return 1
         else:
            return 0
     


# differents tirs :       
    def tirer(self):
       
      
       if (self.position_balle().y > settings.GAME_HEIGHT/2):
           return Vector2D (settings.GAME_HEIGHT,-(self.position_balle().y - settings.GAME_HEIGHT/2))
       
       if (self.position_balle().y < settings.GAME_HEIGHT/2):
           return Vector2D (settings.GAME_HEIGHT,(self.position_balle().y - settings.GAME_HEIGHT/2))
       
       return Vector2D(settings.GAME_HEIGHT,0)
        
    def non_tir (self) :
        return Vector2D(0,0);
    
    def tir_leger(self) :
      
      if (self.position_balle().y > settings.GAME_HEIGHT/2) :    
        x =0-0.5       
        return Vector2D(angle = x , norm =2)
      elif (self.position_balle().y < settings.GAME_HEIGHT/2) : 
          return Vector2D(angle = 0.5 , norm =2)
      else:
          return Vector2D(angle = 0 , norm =2)
  
    def tir_leger_alea(self) :
        
        x =random.randrange((-1),1)       
        return Vector2D(angle = x , norm =2)
 
    def dribbler(self):        
        return SoccerAction( self.position_balle()-self.position_joueur() ,self.tir_leger_alea())
        
   
    def tir_legerD(self) :
      
     return Vector2D(settings.GAME_HEIGHT,0).normalize().scale(2)
    
    def centrerH(self):
        if (self.cornerX() == 1 and self.cornerYH() == 1 ):
                   
            return True
            
    def centrerB(self):

        if (self.cornerX() == 1 and self.cornerYB() == 1 ):
            return True
            
    def aller_centrer(self):
        
         x = SoccerAction(self.position_balle() - self.position_joueur(), Vector2D(angle = 0.5 , norm =1.5))
         y = SoccerAction(self.position_balle() - self.position_joueur(), Vector2D(angle = (0.5-1) , norm =1.5))
         if (self.position_balle().y > settings.GAME_HEIGHT/2):
               return x
         else:
               return y
          
        
    def tirer_centreH(self):
     
     return SoccerAction(self.position_balle() - self.position_joueur(),Vector2D((settings.GAME_WIDTH*2) /3,settings.GAME_HEIGHT/2)-self.position_joueur())         
            
            
    def tirer_centreB(self):
     
     return SoccerAction(self.position_balle() - self.position_joueur(),Vector2D(-settings.GAME_WIDTH/2,settings.GAME_HEIGHT))            
    
#    def Aller_centre(self):
#        if (self.cornerX and self.cornerY == 1 ):
#            return        
    def tirer_vers(self, c):        
        return SoccerAction( self.position_balle()-self.position_joueur() ,Vector2D(c.x,c.y))
        
    def passer_vers(self, c):        
        return Vector2D(c.position.x,c.position.y)-self.position_joueur()
    
    def degage(self):
        return Vector2D(settings.GAME_HEIGHT,20)

    def degage_alea(self):
        return Vector2D(settings.GAME_HEIGHT,random.randrange(settings.GAME_HEIGHT/3,(2*settings.GAME_HEIGHT)/3))

    def marquer(self):
        return SoccerAction(self.position_balle() - self.position_joueur() , self.tirer())
        
    def conserver(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.tir_leger())
        
    def conserver2(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.tir_legerD())
    
    def degager(self):
        return SoccerAction(self.position_balle() - self.position_joueur(),self.degage_alea())

# deplacements et placement     
  

    def aller_vers(self, c):        
        return SoccerAction( c - self.position_joueur() ,self.non_tir())
        
        
    def position_but_adv(self):
        return (Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2))
      
   
        
    def positionG(self):
        return SoccerAction((Vector2D(5,settings.GAME_HEIGHT/2))-self.position_joueur(), self.tirer())
    
    def positionGH(self):
        return SoccerAction((Vector2D(2,settings.GAME_HEIGHT/2)+5)-self.position_joueur(), self.degage())
     
    def positionGB(self):
        return SoccerAction((Vector2D(2,settings.GAME_HEIGHT/2)-5)-self.position_joueur(), self.degage())
        
    def positionDC(self):
        return SoccerAction((Vector2D(20,settings.GAME_HEIGHT/2))-self.position_joueur(), self.tirer())
    
    def defendre (self):
        return SoccerAction(self.position_balle() - self.position_joueur(),Vector2D(settings.GAME_HEIGHT,0))
    
    def avant_centre(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH*4) /5,settings.GAME_HEIGHT/2)-self.position_joueur(),self.non_tir())

    def millieu(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH) /3,settings.GAME_HEIGHT/2)-self.position_joueur(),self.non_tir())


    def zone_cage(self):
        
        if self.position_balle().y>= (settings.GAME_HEIGHT /2)-5 and self.position_balle().y<= (settings.GAME_HEIGHT /2)+5 :
            return 1
        else:
            return 0
            
    def zone_def(self):
        if self.position_balle().y>= (settings.GAME_HEIGHT /3) and self.position_balle().y<= 2*(settings.GAME_HEIGHT /3) :
            return 1
        else:
            return 0

    
    def suivre_jeuG (self):
      return SoccerAction(Vector2D(5,self.position_balle().y)-self.position_joueur(), self.tirer())
    
    def suivre_jeu(self):
        return SoccerAction(Vector2D(settings.GAME_WIDTH /5,self.position_balle().y)-self.position_joueur(), self.tirer())
        
    def suivre_jeuM(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH)/1.8,self.position_balle().y)-self.position_joueur(), self.tirer())   
        
    def suivre_jeuDC(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH)/10,self.position_balle().y)-self.position_joueur(), self.tirer())    
    
     
    def sortieGardien(self) :
         if( self.position_balle().x < settings.GAME_WIDTH / 6 ) :
             return 1
         else:
             return 0
    def zone_de_tir(self) :
         if( self.position_balle().x > settings.GAME_WIDTH - 30) :
             return 1         
         else:
             return 0
    def dans_perimetre(self) :
        if (self.position_balle().y > settings.GAME_HEIGHT/3 and self.position_balle().y < (settings.GAME_HEIGHT*2) / 3) :
            return 1
        else:
             return 0
    def tir_but(self):
        return SoccerAction( self.position_balle()-self.position_joueur() , Vector2D(settings.GAME_WIDTH , (settings.GAME_HEIGHT)/2) - self.position_joueur())
       
    def finition(self):
        return SoccerAction( self.position_balle()-self.position_joueur() , (Vector2D(settings.GAME_WIDTH , (settings.GAME_HEIGHT)/2) - self.position_joueur()).normalize().scale(3))
           
    def distance_joueur(self,id_team,id_player):
        return self.position_joueur().distance(self.state.player_state(id_team,id_player).position)
        
    def distance_au_joueur(self):

        j = 0
        for (id_team, id_player) in self.state.players :
            if id_team != self.id_team and self.distance_joueur(id_team,id_player) < 30 and (self.state.player_state(id_team, id_player).position.x >= self.position_joueur().x):
                j=j+1
        if j != 0:
            return 1
        else :
            return 0
 
    def distance_allie(self):

        j = 0
        for (id_team, id_player) in self.state.players :
            if id_team == self.id_team and self.distance_joueur(id_team,id_player) < 30 and (self.state.player_state(id_team, id_player).position.x >= self.position_joueur().x):
                j=j+1
        if j != 0:
            return 1
        else :
            return 0
            
            
    def dj2(self):
    
        j = 0
        for (id_team, id_player) in self.state.players :
            if id_team != self.id_team and self.distance_joueur(id_team,id_player) < 30 and (self.state.player_state(id_team, id_player).position.x >= self.position_joueur().x):
                
              j=j+1
              return self.defendre_Sur(self.state.player_state(id_team, id_player))
        if j == 0 :
             return SoccerAction(0,0)
      
    def defendre_Sur(self,v):
        
        return SoccerAction(v.position - self.position_joueur(),Vector2D(settings.GAME_HEIGHT,0))
        
   
    def faire_passe(self):
        if(self.distance_balle() < 3):
            return True
        else:
            return False
   
    def passer(self):
        j = 0
        for (id_t, id_p) in self.state.players :
            if id_t == self.id_team and self.distance_joueur(id_t,id_p) <= 50:
               print("passer vers")
               return self.passer_vers(self.state.player_state(id_t, id_p))
            else:
                j = j+1
        print("j =" ,str(j))
        if j != 0 :
             return self.conserver2()
             
#     def possedeBalleAll(self):
#        j = 0
#        for (id_t, id_p) in self.state.players :
#            if id_t == self.id_team and self.state.player_state(id_t, id_p).possede_balle()
#               return self.passer_vers(self.state.player_state(id_t, id_p))
#            else:
#                j = j+1
#        print("j =" ,str(j))
#        if j != 0 :
#             return self.conserver2()
             
    def passerAll(self):
        j = 0
        for (id_t, id_p) in self.state.players :
            if (j is None and  id_t == self.id_team and id_p != self.id_player):
                j = self.state.player_state(id_t, id_p).position
                if id_t == self.id_team and self.distance_joueur(id_t,id_p) < self.distance_joueur(j):
              
                  j = self.state.player_state(id_t, id_p).position
                else:
                 continue
            else : 
                continue
        return j
        
 ######################################################################################################################
 ########################    pour le Qlearning    ######################################################
    
    

    def position_mesbuts(self):
       self.position_joueur().distance(Vector2D(0,settings.GAME_HEIGHT/2.))    
       
    def position_butsadv(self):
       self.position_joueur().distance(Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))    
    
    def distance_adversairexy(self, x , y):

        j = 0
        for (id_team, id_player) in self.state.players :
            if (id_team != self.id_team and self.distance_joueur(id_team,id_player) >= x and self.distance_joueur(id_team,id_player) < y):
                j=j+1
        if j != 0:
            return True
        else :
            return False
 
    def distance_alliexy(self,x,y):

        j = 0
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team and self.distance_joueur(id_team,id_player) >= x and self.distance_joueur(id_team,id_player)< y):
                j=j+1
        if j != 0:
            return True
        else :
            return False
            
            
    def distance_Mesbuts(self,x,y):
        
      if (self.position_mesbuts() >= x and self.position_mesbuts() < y):
        return True
      else:
        return False
  
    
              
    def distance_butsadv(self,x,y):
        
      if (self.position_butsadv() >= x and self.position_butsadv() < y):
        return True
      else:
        return False
                      
    def distance_ballexy(self,x,y):
       if self.distance_balle() >= x and self.distance_balle() < y:
       
         return True
       else:
         return False
         
        