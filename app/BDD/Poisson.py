# -*- coding: utf-8 -*-
import EnumType
import pandas as pd
import numpy


class Poisson():

    
    def __init__(self,DataFrame,index):
        
        self.name = DataFrame['Nom commun'][index]
        self.genre = DataFrame['Genre'][index]
        self.specie = DataFrame['Espèce'][index]
        self.origine = DataFrame['Origine'][index]
        self.size = DataFrame['Taille cm'][index]
        self.pH = EnumType.pH[DataFrame['pH'][index]]
        self.dureté = DataFrame['Dureté'][index]    
        self.tank_size= DataFrame['Volume en spécifique'][index]
        self.lifestyle = DataFrame['Mode de maintenance'][index]
        self.behavior = DataFrame['Comportement global'][index]
        self.Reproduction = DataFrame['Reproduction'][index]
        self.Reproduction_mod = DataFrame['Mode de reproduction'][index]
        self.food = DataFrame['Nourriture'][index]
        self.Particularity = DataFrame['Particularité'][index]
        
        temp = DataFrame['T°C'][index]
        if type(temp) is not numpy.int64:
            if '-' in temp:            
                temp = temp.split('-')
                self.temp_min = temp[0]
                self.temp_max = temp[1]
        else:
            self.temp_min = temp - 1
            self.temp_max = temp + 1    
    
    def __str__(self):         
        return self.name+'|'+ self.genre
    
    
    name =""
    genre = ""
    specie =""
    origine = ""
    size = ""
    pH_min = ""
    pH_max = ""
    dureté = ""
    temp_min = ""
    temp_max = ""
    tank_size = ""
    lifestyle = ""
    behavior = ""
    Reproduction = ""
    Reproduction_mod = ""
    food = ""
    Particularity = ""
        