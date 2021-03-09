# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 09:00:50 2021

@author: User
"""

from enum import Enum

# =============================================================================
# class Reproduction_mod(Enum):
#     OVIPARE = 1
#     VIVIPARE = 2
# =============================================================================


class Genre(Enum):
    male =0
    female=1
    
    
    
class Level(Enum):
    
    tres_faible=0
    faible=1
    moyen =2
    difficille =3
    tres_difficile =4
    
class Origin(Enum):
    asie =0
    indonesie =1
    pacifique =2
    atlantique = 3
    afrique = 4 
    amerique = 5
    
    
class Lifestyle(Enum):
    couple =0
    solitaire = 1
    grégaire = 2

class Food(Enum):
    carnivore =0
    omnivore = 1
    
class pH(Enum):
    basique = 8
    neutre = 7
    acide = 6
    