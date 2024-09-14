# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 12:18:56 2024

@author: sstew
"""

import numpy as np
import json 
import random as r
def listUnPlayedTeams(schedule,i,week):
    listTeams = []
    for j in range(0,schedule.shape[0]):
        if(i == j):
            continue
        if(schedule[j,week] != -1):
            continue
        Valid = True
        for w in range(0,schedule.shape[1]):
            if(schedule[i,w]==j):
                Valid = False
                break
        
        if(Valid):
            listTeams.append(j)
    return listTeams

def createSchedule(numTeams:int, numWeeks:int):
    schedule = np.ones((numTeams, numWeeks)) * -1
    jump = 0
    w = -1
    while (w +1 < numWeeks):
        w += 1
        try:
            for i in range(0, numTeams):
                if(schedule[i,w] == -1 ):
                    playableTeams = listUnPlayedTeams(schedule,i,w)
                    
                    j =r.choice(playableTeams)
                    
                    schedule[(i),w] = j
                    schedule[(j),w] = i
        except:
            schedule[:,w] = np.ones((numTeams)) * -1
            w += -1
    return schedule
def verifySchedule(schedule):     
    for i in range(0,schedule.shape[0]):
        for w in range(0,schedule.shape[1]):
            j = int(schedule[i,w])
            
            if(not schedule[j,w] == i):
                return False
    return True
def saveSchedule():
    output = {}
    for w in range(0,schedule.shape[1]):
        weekly = {}
        opponents = {}
        uniqueness = 1
        shuffle = []
        for i in range(0,schedule.shape[0]):
            shuffle.append(i)
        r.shuffle(shuffle)
        for i in shuffle:
            j = int(schedule[i,w])
            if(str(j+1) not in weekly.keys()):
                weekly.update({str(i+1): str(uniqueness)})
                uniqueness +=1
            else:
                matchID = weekly[str(j+1)]
                weekly.update({str(i+1): matchID})
            opponents.update({str(i+1):str(j+1)})
        output.update({"week"+str(w+1):weekly})  
        output.update({"opponent"+str(w+1):opponents})
    with open('./schedule.json', 'w') as f:
        json.dump(output, f)
schedule = createSchedule(20,14)
if(verifySchedule(schedule)):
    saveSchedule()