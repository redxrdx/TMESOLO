# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:29:33 2016

@author: 3200404
"""

 

from strategie import *
from soccersimulator import SoccerTeam,Player
from decisiontree import DTreeStrategy , gen_features
import cPickle
import os

fn = os.path.join(os.path.dirname(os.path.realpath(__file__)), "millieu.pkl")
fn2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "attaque.pkl")
fn3 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "defense.pkl")
fn4 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mon_fichier.pkl")



team2j2 = SoccerTeam("team2",[Player("pique",attaqueG),Player("masherano",defenseG)])
teamREAL = SoccerTeam("team1",[Player("CR7",pointe),Player("ramos",defenseG),Player("marcelo",millieu),Player("navas",goalG)])
teamPSG4 = SoccerTeam("team1",[Player("trapp",goalG),Player("silva",central),Player("aurier",defenseG),Player("zlatan",attaqueG)])
team1 = SoccerTeam("k1",[Player("serge",joueur1)])
team12j = SoccerTeam("team1",[Player("ert",attaqueG)])
team2 = SoccerTeam("k2",[Player("serge",defenseG),Player("ramos",attaqueG)])
team4 = SoccerTeam("test",[Player("t",goalG),Player("s",defenseG),Player("a",millieu),Player("z",pointe)])

tree = cPickle.load(file(fn4))
dic = {"goal":goalG,"attaquant":attaqueG,"defenseur":defenseG,"millieu":millieu,"defenseCentral":central,"conserver":conserver,"dribbler":dribbler,"tirer":tirer,"passer":passer,"finition":finition}
treeStrat = DTreeStrategy(tree,dic,gen_features)

millieuI = cPickle.load(file(fn))
dic = {"goal":goalG,"attaquant":attaqueG,"defenseur":defenseG,"millieu":millieu,"defenseCentral":central,"conserver":conserver,"dribbler":dribbler,"tirer":tirer,"passer":passer,"finition":finition}
MStrat = DTreeStrategy(millieuI,dic,gen_features)

attaqueI = cPickle.load(file(fn2))
dic = {"goal":goalG,"attaquant":attaqueG,"defenseur":defenseG,"millieu":millieu,"defenseCentral":central,"conserver":conserver,"dribbler":dribbler,"tirer":tirer,"passer":passer,"finition":finition,"position":position}
AStrat = DTreeStrategy(attaqueI,dic,gen_features)

defenseI = cPickle.load(file(fn3))
dic = {"goal":goalG,"attaquant":attaqueG,"defenseur":defenseG,"millieu":millieu,"defenseCentral":central,"conserver":conserver,"dribbler":dribbler,"tirer":tirer,"passer":passer,"finition":finition,"position":position,"dc":central}
DStrat = DTreeStrategy(defenseI,dic,gen_features)

team2j = SoccerTeam("k2",[Player("serge",defenseG),Player("ramos",treeStrat)])
teamIA = SoccerTeam("team1",[Player("ert",MStrat),Player("ramos",goalG),Player("t",AStrat),Player("s",DStrat)])