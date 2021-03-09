# -*- coding: utf-8 -*-


import pandas as pd
from os import walk
import Poisson

class DataBase ():
       
        
    listmembre = ['Nom commun','Genre','Espèce','Origine','Taille cm',
                  'pH','Dureté','T°C','Volume en spécifique',
                  'Mode de maintenance','Comportement global',
                  'Reproduction','Mode de reproduction','Nourriture',
                  'Particularité','Photo']
     
    def getdataBase(self):
        
        directories= 'bdd\CSV'
        listfichier=[]
        listpoisson =[]

        BDD = dict()
        
        for(repertoire,sousrepertoire,fichiers)in walk(directories):
            listfichier.extend(fichiers)
        
        
        for fichier in listfichier:
            BDD[fichier] = pd.read_csv(directories+'\\'+fichier,
               names= self.listmembre, sep = ';',header =0)
            for i in range(BDD[fichier].shape[0]):        
                P = Poisson.Poisson(BDD[fichier].loc[[i]],i)
                listpoisson.append(P)

        return listpoisson
    
    def SaveData(self,ListPoisson,path):
        
        ListPoisson.to_csv(path,sep=';',columns= self.listmembre,index= False)