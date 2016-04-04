from soccersimulator import *
from tools import *

class PADState(SoccerState):
    """ Etat d'un tour du jeu. Contient la balle (MobileMixin), l'ensemble des configurations des joueurs, le score et
    le numero de l'etat.
    """
    def __init__(self, **kwargs):
        SoccerState.__init__(self,**kwargs)
        self.cur_score = 0

    def apply_actions(self, actions=None):
        sum_of_shoots = Vector2D()
        if actions:
            for k, c in self._configs.items():
                if k in actions:
                    act = actions[k].copy()
                    if k[0] == 1 and self.player_state(k[0],k[1]).vitesse.norm>0.01:
                        act.shoot = Vector2D()
                    sum_of_shoots += c.next(self.ball, act)
        self.ball.next(sum_of_shoots)
        self.step += 1
        dball = [(it,ip) for it,ip in self.players
                 if self.player_state(it,ip).position.distance(self.ball.position)<settings.BALL_RADIUS+settings.PLAYER_RADIUS]
        mines = [(it,ip) for it,ip in dball if it ==1 ]
        others = [(it,ip) for it,ip in dball if it==2 ]
        if len(others)==0 or len(mines)>0 or self.ball.vitesse.norm>1:
            self.cur_score += 1
        else:
            self._score[1]=max(self._score[1],self.cur_score)
            self.cur_score=0
            self._score[2]+=1
            self._winning_team = 2
        if self.ball.position.x < 0:
            self.ball.position.x = -self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y < 0:
            self.ball.position.y = -self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y
        if self.ball.position.x > settings.GAME_WIDTH:
            self.ball.position.x = 2 * settings.GAME_WIDTH - self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y > settings.GAME_HEIGHT:
            self.ball.position.y = 2 * settings.GAME_HEIGHT - self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y

    def reset_state(self, nb_players_1=0, nb_players_2=0):
        SoccerState.reset_state(self,nb_players_1,nb_players_2)
        self.ball = Ball.from_position(self.player(1,0).position.x,self.player(1,0).position.y)
        self.cur_score = 0


class fonceur(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     def compute_strategy(self,state,id_team,id_player):
       p = state.player_state(id_team,id_player)   
       return SoccerAction(state.ball.position - p.position,Vector2D(-(settings.GAME_HEIGHT),0))

class passeur1(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     def compute_strategy(self,state,id_team,id_player):
       MyState = PlayerDecorator(state ,id_team , id_player) 
       if (MyState.possede_balle()):
            j = MyState.passerAll()
            z = Vector2D(settings.GAME_WIDTH*1/4,settings.GAME_HEIGHT/2) 
            return MyState.tirer_vers(j) 
       else:
            return MyState.aller_vers(z) 
            
            
class passeur2(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     def compute_strategy(self,state,id_team,id_player):
       MyState = PlayerDecorator(state ,id_team , id_player) 
       if (MyState.possede_balle()):
            j = MyState.passerAll()
            y = Vector2D(settings.GAME_WIDTH/2,settings.GAME_HEIGHT/4) 
            return MyState.tirer_vers(j)
       else : 
           return MyState.aller_vers(y) 
      
                
class passeurArret(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     def compute_strategy(self,state,id_team,id_player):
       MyState = PlayerDecorator(state ,id_team , id_player) 
       if (MyState.possede_balle() and self.state.player_state(self.id_team, self.id_player).vitesse.norm < 0.01):
            j = MyState.passerAll()
            a = Vector2D(settings.GAME_WIDTH/3,settings.GAME_HEIGHT/3) 
            return MyState.tirer_vers(j)
       else : 
           return MyState.aller_vers(a)   
           
 class passeur4(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     def compute_strategy(self,state,id_team,id_player):
       MyState = PlayerDecorator(state ,id_team , id_player) 
       if (MyState.possede_balle()):
            j = MyState.passerAll()
            x = Vector2D(settings.GAME_WIDTH/4,settings.GAME_HEIGHT/3) 
            return MyState.tirer_vers(j)
       else : 
           return MyState.aller_vers(y)       
           
           
team2= SoccerTeam("T1",[Player("1", passeur1()),Player("2",passeur2())])
#team4= SoccerTeam("T1",[Player("1", PasseStrategy()),Player("2",PasseStrategy()),Player("3",PasseStrategy()),Player("4",PasseStrategy())])

team1 = SoccerTeam("T2",[Player("1", fonceur())])
#team3 = SoccerTeam("T2",[Player("1", FonceurStrategy()),Player("2", FonceurStrategy()),Player("3",FonceurStrategy())])

match1 = SoccerMatch(team2,team1)
match = SoccerMatch(team2,team1,init_state=PADState.create_initial_state(2,1))
show(match)
#match = SoccerMatch(team4,team3,init_state=PADState.create_initial_state(4,3))
#show(match)