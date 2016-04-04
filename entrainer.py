""" Permet de jouer et d'entrainer une strategie
    * changer les strategies ajoutees
    * utilisation : python entrainer prefix_fichier_exemple
    par defaut ajoute au fichier d'exemples sil existe deja
    (extension : .exp pour le fichier exemple)
"""

from soccersimulator import  SoccerMatch, show, SoccerTeam,Player,KeyboardStrategy
from strategie import *
import sys

if __name__=="__main__":
    prefix = "tree"
    if len(sys.argv)>1:
        prefix = sys.argv[1]    
    keytest = KeyboardStrategy(fn = "mon_fichier")
    keytest.add("d",defenseG)
   # keytest.add("a",attaqueG)
    keytest.add("z",millieu)
    keytest.add("f",finition)
    keytest.add("t",tirer)
    keytest.add("c",conserver)
    keytest.add("g",dribbler)
    keytest.add("q",passer)
    keytest.add("x",position)   
#    keytest.add("c",central)
#    keytest.add("g",posG)
#    keytest.add("d",posGH)
#    keytest.add("c",posGB)   
#    keytest.add("x",degG)
    
   
    team_noob = SoccerTeam("keyb",[Player("KBs",millieu),Player("Defense",defenseG),Player("taaaaaa",attaqueG),Player("Dg",goalG)])
    teama4 = SoccerTeam("test",[Player("t",defenseG),Player("Defense",keytest)])
    teamPSG4 = SoccerTeam("team1",[Player("trapp",attaqueG),Player("silva",defenseG)])
#    ,Player("aurier",defenseG),Player("zlatan",attaqueG)])

    match = SoccerMatch(teama4,teamPSG4,3000)
    show(match)
    keytest.write("mon_fichier.exp",True)
