import requests
import json
from table2ascii import table2ascii as t2a, PresetStyle
import time as clock
import string
import drawTable

def fakePlayerInfo():
    return None
        
def getSchedule(rosterID,week):
    f = open('schedule.json')
    data = json.load(f)
    return int(data['week'+str(week)][str(rosterID)])
def getOpponent(rosterID,week):
    f = open('schedule.json')
    data = json.load(f)
    return int(data['opponent'+str(week)][str(rosterID)])
def calculateWLT(roster, week,teamNames, leagueIDA,leagueIDB):
    body = []
    scores = calculateAllScores(leagueIDA,leagueIDB)
    wins, losses, ties = (0,0,0)
    
    roster = roster+1
    ScoreValue = 1
    totalSeasonScore = 0
    
    for i in range(1,getNumOfWeeks()+1):
        if(i>=week):
            ScoreValue = 0
        opponent = getOpponent(roster,i)
        weekScores = scores[str(i)]
        #print(weekScores[str(roster)])
        heroScore = float(weekScores[str(roster)]["points"])
        villianScore = float(weekScores[str(opponent)]["points"])
        totalSeasonScore += heroScore
        if(heroScore<villianScore):
            w = 'l'
            losses+=ScoreValue
        elif(heroScore==villianScore):
            w = 't'
            ties +=ScoreValue
        else:
            w = 'w'
            wins +=ScoreValue

        body.append(["Week "+str(i),teamNames[opponent-1][2],villianScore,w,heroScore])
    #print(body, wins, losses, ties)
    return body, wins, losses, ties, round(totalSeasonScore,2)

    
def calculateAllScores(leagueIDA,leagueIDB):
    time = clock.time()
    hoursBetweenRequests = 24
    try:
        
        f = open('scores.json')
        
        data = json.load(f)
        
        oldTime = data['time']
        
        passTime = time - float(oldTime)
        passTime = (passTime/60)/60
        
        if(passTime > hoursBetweenRequests):
            data = requestScores(leagueIDA,leagueIDB,time)
        
    except:
        #pass
        data = requestScores(leagueIDA,leagueIDB,time)
    return data
def requestScores(leagueIDA,leagueIDB, time):
    scores = {'time':time}
    for i in range(1,getNumOfWeeks()+1):
        rosters = {}
        scoresFromWeek = getScore(leagueIDA,leagueIDB,i)
        for score in scoresFromWeek:
            rosters.update({score['roster_id']:score})
        scores.update({str(i):rosters})
    with open('./scores.json', 'w') as f:
        json.dump(scores, f)
    return scores
def getNumOfWeeks():
    return 14
def breakDownWeeklyForOneTeam(allTeams, teamNo,allPlayers):
    team = allTeams[teamNo]
    rosterID = team['roster_id']
    players = team['players_points']
    starters = team['starters']
    playersList = list(players.keys())
    playerBreakdown = []
    
    for player in starters:
        if(player == '0'):
            playerBreakdown.append((rosterID,player,findPlayerName(player,allPlayers), fakePlayerInfo()))
        else:
            playerBreakdown.append((rosterID,player,findPlayerName(player,allPlayers), players[player]))

    for player in playersList:
        if(player in starters):
            continue
        if(player == '0'):
            playerBreakdown.append((rosterID,player,findPlayerName(player,allPlayers), fakePlayerInfo()))
        else:
            playerBreakdown.append((rosterID,player,findPlayerName(player,allPlayers), players[player]))

    return playerBreakdown

def getScore(leagueIDA,leagueIDB,week):
    url = 'https://api.sleeper.app/v1/league/'+str(leagueIDA)+'/matchups/'+str(week)
    leagueA = requests.get(url).json()
    
    url = 'https://api.sleeper.app/v1/league/'+str(leagueIDB)+'/matchups/'+str(week)
    leagueB = requests.get(url).json()
    
    combined = sortTeamsByRosterID(leagueA, leagueB, week)
    #with open('leagueCombined.csv', 'w') as f:
    #    for item in combined:
    #        json.dump(item, f)
    return combined

def getPlayers():
    time = clock.time()
    hoursBetweenRequests = 24
    try:
        
        f = open('players.json')
        
        data = json.load(f)
        
        oldTime = data['time']
        
        passTime = time - float(oldTime)
        passTime = (passTime/60)/60
        
        if(passTime > hoursBetweenRequests):
            return requestPlayers(time)
        return data
    except:
        requestPlayers(time)
        
def requestPlayers(time):
    print('requestPlayers')
    url = 'https://api.sleeper.app/v1/players/nfl'
    allPlayers = requests.get(url).json()
    allPlayers['time'] = time
    with open('players.json', 'w') as f:
        json.dump(allPlayers, f)
    return allPlayers
    
def findPlayerName(player,allPlayers):
    #returns Name, Team, Pos
    if(player == '0'):
        return (' ',' ',' ')
    player = allPlayers[player]
    firstName = player['first_name']
    lastName = player['last_name']
    team = player['team']
    pos = player['position']
    return (firstName+' '+lastName,team,pos)
def getMatchups(allTeams):
    totalTeams = len(allTeams)
    totalMatchups = int(totalTeams/2)
    matchups = []
    for matchup in range(0,totalMatchups):
        matchups.append([0,0])
    for i in range(0,totalTeams):
        team = allTeams[i]
        matchup = team['matchup_id'] -1
        
        if(matchups[matchup][0] == 0):
            matchups[matchup][0] = team['roster_id']
        matchups[matchup][1] = team['roster_id']
    return matchups
def sortTeamsByRosterID(allTeamsA, allTeamsB, week):
    totalTeams = len(allTeamsA) + len(allTeamsB)
    totalTeamsA = len(allTeamsA)
    teams = []
    
    for i in range(0,totalTeams):
        teams.append(0)
    for i in range(0,totalTeams):
        team = None
        rosterID = -1
        if(i<totalTeamsA):
            team = allTeamsA[i]
            rosterID = team['roster_id']
        else:
            team = allTeamsB[i-totalTeamsA]
            rosterID = team['roster_id'] + totalTeamsA
            team['roster_id'] = rosterID
        team['matchup_id'] = getSchedule(rosterID,week)
        teams[rosterID-1] = team
    
    return teams
def getTeamNames(leagueIDA,leagueIDB):
    url = 'https://api.sleeper.app/v1/league/'+str(leagueIDA)+'/users'
    teamNamesA = requests.get(url).json()
    aLen = len(teamNamesA)
    
    url = 'https://api.sleeper.app/v1/league/'+str(leagueIDA)+'/rosters'
    ownersA = requests.get(url).json()
    
    rosterNames = []
    for owner in ownersA:
        oid = owner['owner_id']
        
        for team in teamNamesA:
            uid = team['user_id']
            if(oid == uid):
                meta = team['metadata']
                username = team['display_name']
                roserID = owner['roster_id']
                teamName = username
                try:
                    teamName = meta['team_name']
                except:
                    pass
                
                rosterNames.append((oid, username,teamName,roserID))
                
    url = 'https://api.sleeper.app/v1/league/'+str(leagueIDB)+'/users'
    teamNamesB = requests.get(url).json()
    
    url = 'https://api.sleeper.app/v1/league/'+str(leagueIDB)+'/rosters'
    ownersB = requests.get(url).json()
    for owner in ownersB:
        oid = owner['owner_id']
        
        for team in teamNamesB:
            uid = team['user_id']
            if(oid == uid):
                meta = team['metadata']
                username = team['display_name']
                roserID = owner['roster_id']
                teamName = username
                try:
                    teamName = meta['team_name']
                except:
                    pass
                
                rosterNames.append((oid, username,teamName,roserID + aLen))
    
    return rosterNames
def createMatchupTable(allTeams, matchups, allPlayers, week, teamNames):
    body = []
    for game in matchups:
        player1 = game[0]-1
        player2 = game[1]-1
        player1Name = str(teamNames[player1][1])
        player1Team = str(teamNames[player1][2])
        player2Name = str(teamNames[player2][1])
        player2Team = str(teamNames[player2][2])
        player1Score = str(allTeams[player1]['points'])
        player2Score = str(allTeams[player2]['points'])
        
        if(len(player1Name)>11):
            player1Name=player1Name[:8] +'...'
        if(len(player2Name)>11):
            player2Name=player2Name[:8]+'...'
        if(len(player1Team)>20):
            player1Team=player1Team[:17] +'...'
        if(len(player2Team)>20):
            player2Team=player2Team[:17]+'...'
        
        body.append([player1Name,player1Team,player1Score,' vs ',player2Score,player2Team,player2Name])
    header = ["Player","Team", "Score", "W "+str(week), "Score", "Team","Player"]    
    drawTable.drawMatchupTable(header, body, week)

def createHeadToHeadTable(allTeams, matchups, allPlayers, week, teamNames, matchupNumber):
    body = []
    header = []
    footer = []
    index = 0
    for game in matchups:
        index +=1
        if(index == matchupNumber):
            player1 = game[0]-1
            player2 = game[1]-1
            player1Name = str(teamNames[player1][1])
            player1Team = str(teamNames[player1][2])
            player2Name = str(teamNames[player2][1])
            player2Team = str(teamNames[player2][2])
            player1Score = str(allTeams[player1]['points'])
            player2Score = str(allTeams[player2]['points'])
            
            header = [[player1Name,'','','','','','','',player2Name],[player1Team,'', "Proj. ", "Score",'', "Score", "Proj. ",'', player2Team]]
            team1 = None
            team2 = None
            for team in allTeams:
                if(team['roster_id'] == player1):
                    if(team1==None):
                        team1=team
                    else:
                        team2 = team
                        break
            totalScore1 = 0
            totalScore2 = 0
            totalProjectedScore1 = 0
            totalProjectedScore2 = 0
            
                
            team1 = breakDownWeeklyForOneTeam(allTeams, player1, allPlayers)
            team2 = breakDownWeeklyForOneTeam(allTeams, player2, allPlayers)
            
                #rosterID,player,findPlayerName(player,allPlayers), players[player]
            length = len(team1)
            if(length<len(team2)):
                length = len(team2)
            for i in range(0,length):
                if(i<len(team1)):
                    rosterSpot1 = team1[i]
                else:
                    rosterSpot1 = (None,None,('empty','NA'))
                if(i<len(team2)):
                    rosterSpot2 = team2[i]
                else:
                    rosterSpot2 = (None,None,('empty','NA'))
                
                projected1 = getProjectionsForPlayer(rosterSpot1[1], allPlayers, week)['fantasyPoints']
                projected2 = getProjectionsForPlayer(rosterSpot2[1], allPlayers, week)['fantasyPoints']
                
                if(rosterSpot1[0] is not None):
                    if(rosterSpot1[3] is not None):
                        score1 = rosterSpot1[3]
                    else:
                        score1 = 0.0
                else:
                    score1 = 0.0
                    
                if(rosterSpot2[0] is not None):
                    if(rosterSpot2[3] is not None):
                        score2 = rosterSpot2[3]
                    else:
                        score2 = 0.0
                else:
                    score2 = 0.0
                    
                if(i<len(allTeams[player1]['starters'])):
                    
                    totalScore1 += float(score1)
                    totalScore2 += float(score2)
                    totalProjectedScore1 += float(projected1)
                    totalProjectedScore2 += float(projected2)
                body.append([rosterSpot1[2][0],rosterSpot1[2][1],projected1,score1,'', score2, projected2,rosterSpot2[2][1],rosterSpot2[2][0]])
                
            
            footer = ['','',"{:.2f}".format(totalProjectedScore1) , "{:.2f}".format(totalScore1),'', "{:.2f}".format(totalScore2), "{:.2f}".format(totalProjectedScore2),'', '']
        
        #body.append([player1Name,player1Team,player1Score,' vs ',player2Score,player2Team,player2Name])
        
    drawTable.drawSingleMatchupTable(header, body, footer, matchupNumber, week) 
def createScheduleTable(allTeams, matchups, allPlayers, week, teamNames, matchupNumber, matchupButtonNo, leagueIDA,leagueIDB):
    body = []
    header = []
    footer = []
    index = 0
    player = None
    for game in matchups:
        index +=1
        if(index == matchupNumber):
            
            if(matchupButtonNo==1):
                player = game[0]-1
            else:
                player = game[1]-1
            break
    
    #print(teamNames)
    header = [teamNames[player][2], '','opponent score', 'WLT',teamNames[player][2]+' score']
    body, wins, losses, ties,totalSeasonScore = calculateWLT(player, week,teamNames, leagueIDA,leagueIDB)
    return drawTable.drawScheduleTable(header, body, player, week)
    
    
    
def createSingleTeamTable():
    #drawSingleTeamTable([['Kirk Cousins',23,25, 'QB'],['Adrian Peterson',13,15, 'RB'],['Aaaaaaaaaaaaaaron Rodgers', 1,1,'FLEX']])
    body = []
    header = []
    footer = []
    index = 0
    teamName = ''
    teamOwner = ''
    for game in matchups:
        index +=1
        if(index == matchupNumber):
            player1 = game[matchupPlayerSelected]-1
            
            teamOwner = str(teamNames[player1][1])
            teamName = str(teamNames[player1][2])
            
            player1Score = str(allTeams[player1]['points'])
            
            header = [player1Name,'', "Proj. ", "Score",'', "Score", "Proj. ",'', player2Name]
            team1 = None
            team2 = None
            for team in allTeams:
                if(team['roster_id'] == player1):
                    if(team1==None):
                        team1=team
                        break
            totalScore1 = 0
            totalScore2 = 0
            totalProjectedScore1 = 0
            totalProjectedScore2 = 0
            
                
            team1 = breakDownWeeklyForOneTeam(allTeams, player1, allPlayers)
            
                #rosterID,player,findPlayerName(player,allPlayers), players[player]
            for i in range(0,len(team1)):
                rosterSpot1 = team1[i]
                rosterSpot2 = team2[i]
                
                projected1 = getProjectionsForPlayer(rosterSpot1[1], allPlayers, week)['fantasyPoints']
                
                score1 = rosterSpot1[3]
                
                if(i<len(allTeams[player1]['starters'])):
                    totalScore1 += float(score1)
                    
                    totalProjectedScore1 += float(projected1)
                    
                body.append([rosterSpot1[2][0],rosterSpot1[2][1],projected1,score1,'', score2, projected2,rosterSpot2[2][1],rosterSpot2[2][0]])
                #
            
            #footer = ['','',"{:.2f}".format(totalProjectedScore1) , "{:.2f}".format(totalScore1),'', "{:.2f}".format(totalScore2), "{:.2f}".format(totalProjectedScore2),'', '']
        
        #body.append([player1Name,player1Team,player1Score,' vs ',player2Score,player2Team,player2Name])
    #values, teamName, teamOwner, button1, button2, week    
    drawTable.drawSingleTeamTable( body, footer, matchupNumber,week)    
def getProjections(week,allPlayers):
    
    time = clock.time()
    hoursBetweenRequests = 1
    try:
        
        f = open(str(week)+'.json')
        
        data = json.load(f)
        
        oldTime = data['time']
        
        passTime = time - float(oldTime)
        passTime = (passTime/60)/60
        
        if(passTime > hoursBetweenRequests):
            return requestProjections(week,time,allPlayers)
        return data
    except:
        #pass
        return requestProjections(week,time,allPlayers)
def requestProjections(week, time, allPlayers):
    print("Requesting new projections")
    url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLProjections"
    querystring = {"week":week,
    "archiveSeason":"2024",
    "twoPointConversions":"2",
    "passYards":".04",
    "passAttempts":"-.5",
    "passTD":"4",
    "passCompletions":"0",
    "passInterceptions":"-2",
    "pointsPerReception":"0.6",
    "twoPointConversions":"2",
    "carries":"0",
    "rushYards":".1",
    "rushTD":"6",
    "fumbles":"-2",
    "receivingYards":".1",
    "receivingTD":"6",
    "targets":"0",
    "fgMade":"3",
    "fgMissed":"-1",
    "xpMade":"1",
    "xpMissed":"-1"}
    headers = {
        "x-rapidapi-key": "16ae5bc9c9msh685c1a434ca0ce8p114238jsn876e4b1f06d1",
        "x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    data = associateProjectionsWithPlayer(data, allPlayers)
    new_data = {"time":str(time)}
    data['time'] = str(time)
    with open(str(week)+'.json', 'w') as f:
        json.dump(data, f)
    
    return data

def associateProjectionsWithPlayer(projections, allPlayers):
    projectionPlayers = projections['body']["playerProjections"]
    defProjections = projections['body']["teamDefenseProjections"]
    dictionary = {}
    for playerID in list(allPlayers.keys()):
        player = allPlayers[playerID]
        if(type(player) is not dict):
            
            continue
        
        firstName = player['first_name']
        lastName = player['last_name']
        team = player['team']
        pos = player['position']
        
        fullName = firstName+' '+lastName
        temp = {'longName':fullName,'team':team,'pos':pos,'fantasyPoints':0}
        if(compare(pos,"DEF")):
            for projectionID in list(defProjections.keys()):
               projection = defProjections[projectionID]
               if(compare(projection['teamAbv'],team)):
                   
                   temp={'longName':fullName,'team':team,'pos':pos,'fantasyPoints':projection['fantasyPointsDefault']}
                   
                   break
            dictionary[playerID]=temp
        else:
            for projectionID in list(projectionPlayers.keys()):
                points = 0.0
                projection = projectionPlayers[projectionID]
                if(not compare(projection["longName"],fullName)):
                    continue
                #if(not compare(projection['team'],team)):
                #    continue
                if(not compare(projection['pos'],pos)):
                    if(not( compare(projection['pos'],'PK') and compare(pos,'K'))):
                        
                        continue
                    else:
                        points += 3.3   * float(projection['Kicking']['fgMade'])
                        points += 1   * float(projection['Kicking']['xpMade'])
                        points += -1   * float(projection['Kicking']['fgMissed'])
                        points += -1   * float(projection['Kicking']['xpMissed'])
                        
                else:
                    points += 0.1   * float(projection['Rushing']['rushYds'])
                    points += 0.1   * float(projection['Receiving']["recYds"])
                    points += 0.04  * float(projection['Passing']["passYds"])
                    
                    points += 6.0   * float(projection['Rushing']['rushTD'])
                    points += 6.0   * float(projection['Receiving']["recTD"])
                    points += 4.0   * float(projection['Passing']["passTD"])
                    
                    
                    points += 0.6   * float(projection['Receiving']["receptions"])
                    
                    points += 2.0   * float(projection['twoPointConversion'])
                    
                    points += -2.0   * float(projection['fumblesLost'])
                    points += -1.0  * float(projection['Passing']["int"])

                if(not (fullName == None) and not (pos == None) and not (projection['fantasyPoints'] == None)):
                    temp={'longName':fullName,'team':team,'pos':pos,'fantasyPoints':round(points, 2)}
                    break
            dictionary[playerID]=temp
    return dictionary
            
def compare(s1, s2):
    if(s1 is None):
        if(s2 is None):
            return True
        return False
    if(s2 is None):
        return False
    s1 = s1.lower()
    s2 = s2.lower()
    
    if('iii' in s1):
        s1 = s1.replace('iii','')
    if('ii' in s1):
        s1 = s1.replace('ii','')
    if('sr.' in s1):
        s1 = s1.replace('sr.','')
    if('jr.' in s1):
        s1 = s1.replace('jr.','')
        
    if('iii' in s2):
        s2 = s2.replace('iii','')
    if('ii' in s2):
        s2 = s2.replace('ii','')
    if('sr.' in s2):
        s2 = s2.replace('sr.','')
    if('jr.' in s2):
        s2 = s2.replace('jr.','')
    
    s1 = s1.replace(" ", "")
    s2 = s2.replace(" ", "")
    
    return s1.lower() == s2.lower()
    
def getAllForWeek(leagueIDA,leagueIDB,week):
    allTeams = getScore(leagueIDA,leagueIDB,week)
    teamNames = getTeamNames(leagueIDA,leagueIDB)
    matchups = getMatchups(allTeams)
    allPlayers = getPlayers()
    return createMatchupTable(allTeams, matchups, allPlayers,week,teamNames)
def getMatchupFromWeekAndButton(leagueIDA,leagueIDB,week, button):
    #print(week, button)
    allTeams = getScore(leagueIDA,leagueIDB,week)
    teamNames = getTeamNames(leagueIDA,leagueIDB)
    matchups = getMatchups(allTeams)
    allPlayers = getPlayers()
    return createHeadToHeadTable(allTeams, matchups, allPlayers,week,teamNames,button)    
def getNFLState():
    url = 'https://api.sleeper.app/v1/state/nfl'
    return requests.get(url).json()
    
def getProjectionsForPlayer(playerID, allPlayers, week):
    if(playerID is None):
        return {'fantasyPoints':0.0}
    data = getProjections(week, allPlayers)
    if(playerID == '0'):
        return {'fantasyPoints':0.0}
    return data[playerID]
        
def createTeamTable(allTeams, teamNo,allPlayers, leagueIDA,leagueIDB, week):
    teamNames = getTeamNames(leagueIDA,leagueIDB)
    teamPlayers = breakDownWeeklyForOneTeam(allTeams, teamNo, allPlayers)
    teamID = teamPlayers[0][0]
    values = []
    #['Kirk Cousins',23,25, 'QB']
    for player in teamPlayers:
        values.append([player[2][0],player[3],0,player[2][2],player[2][1]])
    drawTable.drawSingleTeamTable(values, teamNames[teamNo][2], teamNames[teamNo][1])
    
def createScheduleFromWeekAndTwoButtons(leagueIDA,leagueIDB,week, matchupNo,matchupSelect):
    schedule = []
    allTeams = getScore(leagueIDA,leagueIDB,week)
    teamNames = getTeamNames(leagueIDA,leagueIDB)
    matchups = getMatchups(allTeams)
    allPlayers = getPlayers()
    return createScheduleTable(allTeams, matchups, allPlayers, week, teamNames, matchupNo, matchupSelect, leagueIDA,leagueIDB)
        
def createTeamTableFromDiscord(teamID,week,leagueIDA,leagueIDB):    
    allTeams = getScore(leagueIDA,leagueIDB,week)
    teamNames = getTeamNames(leagueIDA,leagueIDB)
    matchups = getMatchups(allTeams)
    allPlayers = getPlayers()
    createTeamTable(allTeams, teamID,allPlayers, leagueIDA,leagueIDB,week)
def swapForWLT(scores, i , j):
    temp = scores[i]
    scores[i] = scores[j]
    scores[j] = temp
    return scores

def sortbyWLT(scores):
    for i in range(0,len(scores)):
        for j in range(i,len(scores)):
            w1 = scores[j][2]
            w2 = scores[i][2]
            if(w2 < w1):
                scores = swapForWLT(scores,i,j)
            elif(w1 == w2):
                t1 = scores[j][3]
                t2 = scores[i][3]
                if(t2 < t1):
                    scores = swapForWLT(scores,i,j)
                elif(t2 == t1):
                    ss1 = scores[j][5]
                    ss2 = scores[i][5]
                    if(ss2 < ss1):
                        scores = swapForWLT(scores,i,j)
    return scores
    
def createStandings(leagueIDA,leagueIDB,week):
    
    teamNames = getTeamNames(leagueIDA,leagueIDB)
    
    totalTeams = len(teamNames)
    scores = []
    for roster in range(0,totalTeams):
        body, w, l, t,totalSeasonScore = calculateWLT(roster, week,teamNames, leagueIDA,leagueIDB)
        teamName = teamNames[roster][2]
        playerName = teamNames[roster][1]
        scores.append([playerName,teamName,w,l,t,totalSeasonScore])
    scores = sortbyWLT(scores)
    header = ['Player','Team','Wins','Losses','Ties','SeasonScore']
    drawTable.drawStandings(header, scores, week)