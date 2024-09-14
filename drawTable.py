import cv2
import numpy as np
from table2ascii import table2ascii
def getFont():
    #return font, fontScale,thickness,color
    return  cv2.FONT_HERSHEY_SIMPLEX, 1, 2, (255,255,255)
def getDiscordColor():
    return (53, 48, 46) 
def getTextHeight():
    return 35
def standardizeText(text):
    approvedCharacters = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnoprstuvwxyz.'
    
    for char in text:
        if(char not in approvedCharacters):
            #print(char)
            text = text.replace(char,' ')
    return text
def padTextToSameSize(text, maxWidth=300, rightAlign = False, middleAlign = False, color = getFont()[3]):
    text = standardizeText(text)
    width = int(round(maxWidth *1.2))
    textHeight = getTextHeight()
    img = np.zeros((textHeight, width, 3), dtype=np.uint8)
    img[:,:] = getDiscordColor()
    font, fontScale,thickness,c = getFont()
    img = cv2.putText(img, text, (0,26), font, fontScale, color, thickness, cv2.LINE_AA)
    for i in range(0,width):
        j = width - i -1
        if(img[:,j].sum() != (getDiscordColor()[0]+getDiscordColor()[1]+getDiscordColor()[2])*img.shape[0]):
           
            break
    if(j>maxWidth):
        #print(text)
        return padTextToSameSize(text[:-4]+'...',maxWidth,rightAlign =rightAlign,middleAlign = middleAlign,color=color  )
    #print(j)
    #cv2.imwrite('./text.png', img[:,0:j])
    if(rightAlign):
        #print('right')
        img2 = np.zeros((textHeight, maxWidth, 3), dtype=np.uint8)
        img2[:,:] = getDiscordColor()
        img2[:,int(maxWidth-j):maxWidth] = img[:,0:j]
        return img2
    if(middleAlign):
        #print('middle')
        img2 = np.zeros((textHeight, maxWidth, 3), dtype=np.uint8)
        img2[:,:] = getDiscordColor()
        #print(maxWidth,img[:,0:j].shape[1])
        x1 = int(round((maxWidth-j)/2))
        x2 = x1+j
        #print(x1,x2,x2-x1)
        img2[:,x1:x2] = img[:,0:j]
        return img2
    return img[:,0:j]
def addText(img,text, loc, width:int = None, right:bool = False, middleAlign:bool = False):
    if(width is None or not right):
        x1= loc[0]
        x2 = loc[0]+text.shape[0]
       
        y1 = loc[1]
        y2 = loc[1]+text.shape[1]
       
        #print(x1,x2,y1,y2, x2-x1,y2-y1,text.shape)
        img[x1:x2,y1:y2,:] = text[:,:,:]
        return img
    if(middleAlign):
        x1= loc[0]
        x2 = loc[0]+text.shape[0]
       
        y1 = int(round(loc[1]+ (width - text.shape[1])/2))
        y2 = int(round(loc[1]+ (width - text.shape[1])/2)) +text.shape[1]
        img[x1:x2,y1:y2,:] = text[:,:,:]
        return img
        
    x1= loc[0]
    x2 = loc[0]+text.shape[0]
   
    y1 = loc[1]+ width - text.shape[1]
    y2 = loc[1]+ width
    
    img[x1:x2,y1:y2,:] = text[:,:,:]
    return img
   
def drawSingleTeamTable(values, teamName, teamOwner, button1, button2, week):
    height = 1460
    width = 750
    lineGap = 10
    maxWidthofName = 300
    maxWidthofPos = 100
    maxWidthofProj = 120
    maxWidthofScore = 120
    textHeight = getTextHeight()
    bglinemult = 1.5
   
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
   
    img = np.zeros((height, width, 3), dtype=np.uint8)
   
    img[:,:] = getDiscordColor()
    columnStart = []#[20,70,120,170,220,270,320]
    for i in range(0,len(values)+1):
        columnStart.append(20+50*i)
   
    lineColor = (255,255,255)
    lineThickness = 2
   
    
   
    img = cv2.line(img, (lineGap,columnStart[0]+textHeight+lineGap), (width-lineGap,columnStart[0]+textHeight+lineGap),lineColor, lineThickness)
   
   
    index = 0
    img = addText(img,padTextToSameSize(teamName,maxWidthofName),(columnStart[index],20),maxWidthofName,True)
   
    for value in values:
        index +=1
        name = value[0]
        name= padTextToSameSize(name,maxWidthofName)
        
        
        projectedScore = value[1]
        projectedScore = padTextToSameSize(str(float(projectedScore)), maxWidthofProj)
        
        actualScore = value[2]
        actualScore = padTextToSameSize(str(float(actualScore)), maxWidthofScore)
        
        pos = value[3]
        if(index ==7):
            pos = 'FLEX'
        if(index > 9):
            pos = 'BEN'
        pos = padTextToSameSize(pos,maxWidthofPos)
        img = cv2.line(img, (lineGap,columnStart[index]+textHeight+lineGap), (width-lineGap,columnStart[index]+textHeight+lineGap),backgroundLineColor, lineThickness)
        if(index == 9):
            img = cv2.line(img, (lineGap,columnStart[index]+textHeight+lineGap), (width-lineGap,columnStart[index]+textHeight+lineGap),lineColor, lineThickness)
        img = addText(img,name,(columnStart[index],20), maxWidthofName, True)
       
        img = addText(img,pos,(columnStart[index],20 + maxWidthofName +lineGap*2), maxWidthofPos, True)
        
        img = addText(img,projectedScore,(columnStart[index],20 + maxWidthofName+maxWidthofPos +lineGap*4), maxWidthofProj, True)
        
        img = addText(img,actualScore,(columnStart[index],20 + maxWidthofName+maxWidthofPos+maxWidthofProj +lineGap*6), maxWidthofScore, True)
    img = cv2.line(img, (lineGap,lineGap), (width-lineGap,lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,lineGap), (lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (width-lineGap,lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,height-lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    cv2.imwrite('./button1'+str(button1)+'-button2'+str(button2)+'-week'+str(week)+'.png', img)
    
def getButton(text,maxWidthofButton, index, middleAlign= False):
    if(index == 0):
        return padTextToSameSize(text,maxWidthofButton, middleAlign= middleAlign)
    else:
        button = cv2.imread(r"./emojiNumbers/"+str(index)+'.png', 1)
        button = cv2.resize(button, (getTextHeight(), getTextHeight()))
        return button
def getWLT(text,maxWidthofButton, index, middleAlign= False):
    if(index == 0):
        return padTextToSameSize('',maxWidthofButton, middleAlign= middleAlign)
    else:
        button = cv2.imread(r"./emojiNumbers/"+str(text)+'.png', 1)
        button = cv2.resize(button, (getTextHeight(), getTextHeight()))
        return button
        
def drawMatchupRow(img,row, columnHeight, index):
#["Player","Team", "Score", " ", "Score", "Team","Player"]    
#str(float(projectedScore)), maxWidthofProj
    maxWidthOfPlayer = 200
    maxWidthofTeam =300
    maxWidthofScore = 120
    maxWidthofButton = 80
    lineGap = 10
    textHeight = getTextHeight()
    lineThickness = 2
    bglinemult = 1.5
    
    color = getFont()[3]
    altColor = (int(round(color[0]/bglinemult)),int(round(color[1]/bglinemult)),int(round(color[2]/bglinemult)))
    
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
    
    player1 =   padTextToSameSize(str(row[0]),maxWidthOfPlayer, color =altColor)
    team1 =     padTextToSameSize(str(row[1]),maxWidthofTeam)
    score1 =    padTextToSameSize(str(row[2]),maxWidthofScore)
    button =    getButton(str(row[3]),maxWidthofButton, index, middleAlign= False)
    score2 =    padTextToSameSize(str(row[4]),maxWidthofScore, rightAlign= False)
    team2 =     padTextToSameSize(str(row[5]),maxWidthofTeam, rightAlign= False)
    player2 =   padTextToSameSize(str(row[6]),maxWidthOfPlayer, rightAlign= False, color = altColor)
    
    startDistance = 20
    img = addText(img,player1    ,(columnHeight,startDistance), maxWidthOfPlayer, False)
    startDistance += maxWidthOfPlayer + lineGap*2
    img = addText(img,team1      ,(columnHeight,startDistance), maxWidthofTeam, False)
    startDistance += maxWidthofTeam + lineGap*2
    img = addText(img,score1     ,(columnHeight,startDistance), maxWidthofScore, False)
    startDistance += maxWidthofScore + lineGap*2
    img = addText(img,button     ,(columnHeight,startDistance), maxWidthofButton, True, middleAlign=True)
    startDistance += maxWidthofButton + lineGap*2
    img = addText(img,score2     ,(columnHeight,startDistance), maxWidthofScore, False)
    startDistance += maxWidthofScore + lineGap*2
    img = addText(img,team2      ,(columnHeight,startDistance), maxWidthofTeam, False)
    startDistance += maxWidthofTeam + lineGap*2
    img = addText(img,player2    ,(columnHeight,startDistance), maxWidthOfPlayer, False)
    
    img = cv2.line(img, (lineGap,columnHeight+textHeight+lineGap), (img.shape[1]-lineGap,columnHeight+textHeight+lineGap),backgroundLineColor, lineThickness)
    return img
    
def drawMatchupTable(header, values, week):
    height = (len(values)+2) * 50 + 40
    width = 1500
    lineGap = 10

    textHeight = 28
    bglinemult = 1.5
   
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
   
    img = np.zeros((height, width, 3), dtype=np.uint8)
   
    img[:,:] = getDiscordColor()
    columnStart = []#[20,70,120,170,220,270,320]
    for i in range(1,len(values)+2):
        columnStart.append(20+50*i)
   
    lineColor = (255,255,255)
    lineThickness = 2
    
    WEEKNO = padTextToSameSize("WEEK" +header[3][1:],200)
    img = addText(img,WEEKNO    ,(20,-10), img.shape[1], True,middleAlign=True)
    header[3] = ' '
    index = 0
    img = drawMatchupRow(img, header, columnStart[index], index)
    img = cv2.line(img, (lineGap,columnStart[0]+textHeight+lineGap), (width-lineGap,columnStart[0]+textHeight+lineGap),lineColor, lineThickness)
    
    for value in values:
        index +=1
        img = drawMatchupRow(img, value, columnStart[index], index)
        
    img = cv2.line(img, (lineGap,lineGap), (width-lineGap,lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,lineGap), (lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (width-lineGap,lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,height-lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    cv2.imwrite('./images/week'+str(week)+'Matchups.png', img)
#drawSingleTeamTable([['Kirk Cousins',23,25, 'QB'],['Adrian Peterson',13,15, 'RB'],['Aaaaaaaaaaaaaaron Rodgers', 1,1,'FLEX']])

def drawSingleMatchupRow(img,row, columnHeight, index, footer = False):
#player1Name,'', "Proj. Score", "Score",'', "Score", "Proj. Score",'', player2Name]
#roster1Name,'team', "Proj. Score", "Score",'POS', "Score", "Proj. Score",'team', roster1Name]
#str(float(projectedScore)), maxWidthofProj
    maxWidthOfPlayer = 300
    maxWidthofTeam =80
    maxWidthofScore = 110
    maxWidthofProjectScore = maxWidthofScore
    maxWidthofPos = 80
    lineGap = 10
    textHeight = getTextHeight()
    lineThickness = 2
    bglinemult = 1.5
    
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
    color = getFont()[3]
    altColor = (int(round(color[0]/bglinemult)),int(round(color[1]/bglinemult)),int(round(color[2]/bglinemult)))
    finalIndexBeforeBench = 10
    if(index > finalIndexBeforeBench):
        color = (backgroundLineColor[0]*bglinemult,backgroundLineColor[1]*bglinemult,backgroundLineColor[2]*bglinemult)
        altColor = color
    if(footer):
        altColor = (color[0]*bglinemult,color[1]*bglinemult,color[2]*bglinemult)
        color = getFont()[3]
    player1 =   padTextToSameSize(str(row[0]),maxWidthOfPlayer, color = color)
    team1 =     padTextToSameSize(str(row[1]),maxWidthofTeam, color = color)
    pscore1 =   padTextToSameSize(str(row[2]),maxWidthofProjectScore, color = altColor)
    score1 =    padTextToSameSize(str(row[3]),maxWidthofScore, color = color)
    pos =       padTextToSameSize(['','','QB','RB','RB','WR','WR','TE','FLEX','K','DEF',
    'BEN','BEN','BEN','BEN','IR',''][index],maxWidthofPos,rightAlign= False, color = altColor)
    score2 =    padTextToSameSize(str(row[5]),maxWidthofScore, rightAlign= False, color = color)
    pscore2 =   padTextToSameSize(str(row[6]),maxWidthofProjectScore, rightAlign= False, color = altColor)
    team2 =     padTextToSameSize(str(row[7]),maxWidthofTeam, rightAlign= False, color = color)
    player2 =   padTextToSameSize(str(row[8]),maxWidthOfPlayer, rightAlign= False, color = color)
    
    startDistance = 20
    img = addText(img,player1    ,(columnHeight,startDistance), maxWidthOfPlayer, False)
    if(footer):
        button =    getButton(1,textHeight, 1, middleAlign= False)
        img = addText(img,button    ,(columnHeight,startDistance), maxWidthOfPlayer, right=True, middleAlign=True)
    startDistance += maxWidthOfPlayer + lineGap*2
    
    img = addText(img,team1      ,(columnHeight,startDistance), maxWidthofTeam, False)
    startDistance += maxWidthofTeam + lineGap*2
    
    img = addText(img,pscore1     ,(columnHeight,startDistance), maxWidthofProjectScore, False)
    startDistance += maxWidthofProjectScore + lineGap*2
    
    img = addText(img,score1     ,(columnHeight,startDistance), maxWidthofScore, False)
    startDistance += maxWidthofScore + lineGap*2
    
    if(not footer):
        img = addText(img,pos     ,(columnHeight,startDistance), maxWidthofPos, False, middleAlign=False)
    startDistance += maxWidthofPos + lineGap*2
    
    
    
    img = addText(img,score2     ,(columnHeight,startDistance), maxWidthofScore, False)
    startDistance += maxWidthofScore + lineGap*2
    
    img = addText(img,pscore2     ,(columnHeight,startDistance), maxWidthofProjectScore, False)
    startDistance += maxWidthofProjectScore + lineGap*2
    
    img = addText(img,team2      ,(columnHeight,startDistance), maxWidthofTeam, False)
    startDistance += maxWidthofTeam + lineGap*2
    
    
    img = addText(img,player2    ,(columnHeight,startDistance), maxWidthOfPlayer, False)
    if(footer):
        button =    getButton(2,textHeight, 2, middleAlign= False)
        img = addText(img,button    ,(columnHeight,startDistance), maxWidthOfPlayer, right=True, middleAlign=True)
    if(index == finalIndexBeforeBench):
        backgroundLineColor = getFont()[3]
    img = cv2.line(img, (lineGap,columnHeight+textHeight+lineGap), (img.shape[1]-lineGap,columnHeight+textHeight+lineGap),backgroundLineColor, lineThickness)
    return img
    
def drawSingleMatchupTable(header, values,footer,buttonNo, week):
    height = (len(values)+3) * 50 + 40
    width = 1470
    lineGap = 10

    textHeight = 28
    bglinemult = 1.5
   
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
   
    img = np.zeros((height, width, 3), dtype=np.uint8)
   
    img[:,:] = getDiscordColor()
    columnStart = []#[20,70,120,170,220,270,320]
    for i in range(0,len(values)+3):
        columnStart.append(20+50*i)
   
    lineColor = (255,255,255)
    lineThickness = 2
  
    index = 0
    img = drawSingleMatchupRow(img, header[0], columnStart[index], index)
    index +=1
    img = drawSingleMatchupRow(img, header[1], columnStart[index], index)
    img = cv2.line(img, (lineGap,columnStart[1]+textHeight+lineGap), (width-lineGap,columnStart[1]+textHeight+lineGap),lineColor, lineThickness)
    
    for value in values:
        index +=1
        img = drawSingleMatchupRow(img, value, columnStart[index], index)
    
    img = cv2.line(img, (lineGap,columnStart[index]+textHeight+lineGap), (width-lineGap,columnStart[index]+textHeight+lineGap),lineColor, lineThickness)
    
    img = drawSingleMatchupRow(img, footer, columnStart[index+1], index+1, footer= True)

    
    img = cv2.line(img, (lineGap,lineGap), (width-lineGap,lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,lineGap), (lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (width-lineGap,lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,height-lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    
    
    
    cv2.imwrite('./images/button'+str(buttonNo)+'-week'+str(week)+'Matchups.png', img)
def drawSingleScheduleRow(img, value, columnHeight, index,w):
    maxWidthOfWeek = 300
    maxWidthOfPlayer = 500
    maxWidthofResult = 30
    maxWidthofScore = 300
    lineGap = 10
    textHeight = getTextHeight()
    lineThickness = 2
    bglinemult = 1.5
    
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
    color = getFont()[3]
    altColor = (int(round(color[0]/bglinemult)),int(round(color[1]/bglinemult)),int(round(color[2]/bglinemult)))
    finalIndexBeforeBench = 10
    if(index > w):
        color = (backgroundLineColor[0]*bglinemult,backgroundLineColor[1]*bglinemult,backgroundLineColor[2]*bglinemult)
        altColor = color
    if(index < w):
        color = (backgroundLineColor[0]*bglinemult*bglinemult,backgroundLineColor[1]*bglinemult*bglinemult,backgroundLineColor[2]*bglinemult*bglinemult)
        altColor = color
    week =      padTextToSameSize(str(value[0]),maxWidthOfWeek, color = color)
    player =     padTextToSameSize(str(value[1]),maxWidthOfPlayer, color = color)
    heroScore =  padTextToSameSize(str(value[2]),maxWidthofScore, color = color)
    result =   getWLT(str(value[3]),maxWidthofResult, index, middleAlign= False)
    villianScore = padTextToSameSize(str(value[4]),maxWidthofScore, color = color)
    
    startDistance = 20
    img = addText(img,week    ,(columnHeight,startDistance), maxWidthOfWeek, False)
    startDistance += maxWidthOfWeek + lineGap*2
    
    img = addText(img,player      ,(columnHeight,startDistance), maxWidthOfPlayer, False)
    startDistance += maxWidthOfPlayer + lineGap*2
    
    img = addText(img,heroScore      ,(columnHeight,startDistance), maxWidthofScore, False)
    startDistance += maxWidthofScore + lineGap*2
    if(index < w):
        img = addText(img,result     ,(columnHeight,startDistance), maxWidthofResult, False)
    if(index == w):
        result =   getWLT('p',maxWidthofResult, index, middleAlign= False)
        img = addText(img,result     ,(columnHeight,startDistance), maxWidthofResult, False)
    startDistance += maxWidthofResult+100 + lineGap*2
    
    img = addText(img,villianScore      ,(columnHeight,startDistance), maxWidthofScore, False)
    startDistance += maxWidthofScore + lineGap*2
    
    img = cv2.line(img, (lineGap,columnHeight+textHeight+lineGap), (img.shape[1]-lineGap,columnHeight+textHeight+lineGap),backgroundLineColor, lineThickness)
    return img
def drawScheduleTable(header, values, team, week):
    height = (len(values)+1) * 50 + 40
    width = 1700
    lineGap = 10

    textHeight = 28
    bglinemult = 1.5
   
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
   
    img = np.zeros((height, width, 3), dtype=np.uint8)
   
    img[:,:] = getDiscordColor()
    columnStart = []#[20,70,120,170,220,270,320]
    for i in range(0,len(values)+3):
        columnStart.append(20+50*i)
   
    lineColor = (255,255,255)
    lineThickness = 2
  
    index = 0
    img = drawSingleScheduleRow(img, header, columnStart[index], index, week)
    
    img = cv2.line(img, (lineGap,columnStart[0]+textHeight+lineGap), (width-lineGap,columnStart[0]+textHeight+lineGap),lineColor, lineThickness)
    
    for value in values:
        index +=1
        img = drawSingleScheduleRow(img, value, columnStart[index], index, week)
         
    #img = cv2.line(img, (lineGap,columnStart[index]+textHeight+lineGap), (width-lineGap,columnStart[index]+textHeight+lineGap),lineColor, lineThickness)
    
    #img = drawSingleScheduleRow(img, footer, columnStart[index+1], index+1, footer= True)

    
    img = cv2.line(img, (lineGap,lineGap), (width-lineGap,lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,lineGap), (lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (width-lineGap,lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,height-lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    
    path = './images/schedule'+str(team)+'-week'+str(week)+'.png'
    cv2.imwrite(path, img)
    return team,week

def drawStandingsRow(img, value, columnHeight, index,w):
    maxWidthOfPlayer = 300
    maxWidthOfTeam = 500
    maxWidthofResult = 150
    maxWidthofSeasonScore = 300
    lineGap = 10
    textHeight = getTextHeight()
    lineThickness = 2
    bglinemult = 1.5
        #['Player','Team','Wins','Losses','Ties','SeasonScore']
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
    color = getFont()[3]
    finalIndexBeforeBench = 10

    player =      padTextToSameSize(str(value[0]),maxWidthOfPlayer, color = color)
    team  =     padTextToSameSize(str(value[1]),maxWidthOfTeam, color = color)
    w =  padTextToSameSize(str(value[2]),maxWidthofResult, color = color)
    l =  padTextToSameSize(str(value[3]),maxWidthofResult, color = color)
    t =  padTextToSameSize(str(value[4]),maxWidthofResult, color = color)
    seasonScore = padTextToSameSize(str(value[5]),maxWidthofSeasonScore, color = color,rightAlign = True)
    
    startDistance = 20
    img = addText(img,player    ,(columnHeight,startDistance), maxWidthOfPlayer, False)
    startDistance += maxWidthOfPlayer + lineGap*2
    
    img = addText(img,team      ,(columnHeight,startDistance), maxWidthOfTeam, False)
    startDistance += maxWidthOfTeam + lineGap*2
    
    img = addText(img,w      ,(columnHeight,startDistance), maxWidthofResult, False)
    startDistance += maxWidthofResult + lineGap*2
    
    img = addText(img,l      ,(columnHeight,startDistance), maxWidthofResult, False)
    startDistance += maxWidthofResult + lineGap*2
    
    img = addText(img,t      ,(columnHeight,startDistance), maxWidthofResult, False)
    startDistance += maxWidthofResult + lineGap*2
    
    img = addText(img,seasonScore     ,(columnHeight,startDistance), maxWidthofSeasonScore, False)
    startDistance += maxWidthofSeasonScore+100 + lineGap*2
    
    img = cv2.line(img, (lineGap,columnHeight+textHeight+lineGap), (img.shape[1]-lineGap,columnHeight+textHeight+lineGap),backgroundLineColor, lineThickness)
    return img
    
def drawStandings(header, values, week):
    height = (len(values)+1) * 50 + 40
    width = 1700
    lineGap = 10

    textHeight = 28
    bglinemult = 1.5
   
    backgroundColor = getDiscordColor()
    backgroundLineColor = (backgroundColor[0]*bglinemult,backgroundColor[1]*bglinemult,backgroundColor[2]*bglinemult)
   
    img = np.zeros((height, width, 3), dtype=np.uint8)
   
    img[:,:] = getDiscordColor()
    columnStart = []#[20,70,120,170,220,270,320]
    for i in range(0,len(values)+3):
        columnStart.append(20+50*i)
   
    lineColor = (255,255,255)
    lineThickness = 2
  
    index = 0
    img = drawStandingsRow(img, header, columnStart[index], index, week)
    
    img = cv2.line(img, (lineGap,columnStart[0]+textHeight+lineGap), (width-lineGap,columnStart[0]+textHeight+lineGap),lineColor, lineThickness)
    
    for value in values:
        index +=1
        img = drawStandingsRow(img, value, columnStart[index], index, week)
         
    #img = cv2.line(img, (lineGap,columnStart[index]+textHeight+lineGap), (width-lineGap,columnStart[index]+textHeight+lineGap),lineColor, lineThickness)
    
    #img = drawSingleScheduleRow(img, footer, columnStart[index+1], index+1, footer= True)

    
    img = cv2.line(img, (lineGap,lineGap), (width-lineGap,lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,lineGap), (lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (width-lineGap,lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    img = cv2.line(img, (lineGap,height-lineGap), (width-lineGap,height-lineGap),lineColor, lineThickness)
    
    path = './images/standings-week'+str(week)+'.png'
    cv2.imwrite(path, img)
    return week