# the main program for calculating the avarages and exact probability

from matchExtractor import *
from teamsReplaceDict import *
from pathlib import Path
import json
import math

isMatchDayFinish = False

# loads the input data
def loadMatchDayData(fileName):
    path = Path(f'{fileName}.json')
    contents = path.read_text()
    loadedFile = json.loads(contents)
    return loadedFile

# calculates teams and league averages
def calculateAverages(dataDict):
    numberOfTeams = len(dataDict)
    sumAveragesGoalsScoredHome = 0
    sumAveragesGoalsAllowedHome = 0
    sumAveragesGoalsScoredAway = 0
    sumAveragesGoalsAllowedAway = 0
    for teamData in dataDict.values():
        teamData['agsh'] = round(teamData['gsh'] / teamData['gph'], 2)
        sumAveragesGoalsScoredHome += teamData['agsh']
        teamData['agah'] = round(teamData['gah'] / teamData['gph'], 2)
        sumAveragesGoalsAllowedHome += teamData['agah']
        teamData['agsa'] = round(teamData['gsa'] / teamData['gpa'], 2)
        sumAveragesGoalsScoredAway += teamData['agsa']
        teamData['agaa'] = round(teamData['gaa'] / teamData['gpa'], 2)
        sumAveragesGoalsAllowedAway += teamData['agaa']
    
    leagueAverageGoalsScoredHome = sumAveragesGoalsScoredHome / numberOfTeams
    leagueAverageGoalsAllowedHome = sumAveragesGoalsAllowedHome / numberOfTeams
    leagueAverageGoalsScoredAway = sumAveragesGoalsScoredAway / numberOfTeams
    leagueAverageGoalsAllowedAway = sumAveragesGoalsAllowedAway / numberOfTeams
    leagueAverages = [leagueAverageGoalsScoredHome, leagueAverageGoalsAllowedHome, 
            leagueAverageGoalsScoredAway, leagueAverageGoalsAllowedAway]
    return leagueAverages

# calculates teams Attacking and Defensive Strength and expected to score goals coefficients
def calculateTeamsAttackingDefensiveStrength(matchDayList, leagueAverages, dataDict):
    teamsExpextedToScoreList = []
    for match in matchDayList:
        homeTeam = match['homeTeam']
        awayTeam = match['awayTeam']
        homeTeamAttackingStrength = round(dataDict[homeTeam]['agsh'] / leagueAverages[0], 2)
        homeTeamDefensiveStrength = round(dataDict[homeTeam]['agah'] / leagueAverages[1], 2)
        awayTeamAttackingStrength = round(dataDict[awayTeam]['agsa'] / leagueAverages[2], 2)
        awayTeamDefensiveStrength = round(dataDict[awayTeam]['agaa'] / leagueAverages[3], 2)

        homeTeamExpectedToScore = round(homeTeamAttackingStrength * awayTeamDefensiveStrength * leagueAverages[0],2)
        awayTeamExpectedToScore =  round(awayTeamAttackingStrength * homeTeamDefensiveStrength * leagueAverages[2], 2)
        teamsExpextedToScoreList.append({homeTeam : homeTeamExpectedToScore, 
                                                awayTeam : awayTeamExpectedToScore})
    print(teamsExpextedToScoreList)
    return teamsExpextedToScoreList

def calculateProbability(teamsExpextedToScoreList):
    exactProbabilityStr = ""
    for match in teamsExpextedToScoreList:
        exactProbabilityStr += '\n'
        for key, value in match.items():
            probabilityList = []
            for k in range (0, 5):
               p = ((value**k*(math.e)**(-value)))/(math.factorial(k))
               probabilityList.append(f'{k}-{round(p*100, 2)}%')
            exactProbabilityStr += key +':' + str(probabilityList) + " \n"
            probabilityList = []
    
    path = Path("probabilityFile.txt")  
    path.write_text(exactProbabilityStr)   


def calculateProbability1(teamsExpextedToScoreList):
    finalDict = []
    for match in teamsExpextedToScoreList:
        matchProbabilityList = []
        for key, value in match.items():
            probabilityDict = {}
            for k in range (0, 5):
               p = ((value**k*(math.e)**(-value)))/(math.factorial(k))
               probabilityDict[k] = round(p, 2)
            matchProbabilityList.append(probabilityDict) 
        dict1 = matchProbabilityList[0]
        dict2 = matchProbabilityList[1]
        sumHomeTeamWin = ((dict1[1] * dict2[0]) + (dict1[2] * dict2[0]) + (dict1[2] * dict2[1]) +
                            (dict1[3] * dict2[0]) + (dict1[3] * dict2[1]) + (dict1[3] * dict2[2]) +
                            (dict1[4] * dict2[0]) + (dict1[4] * dict2[1]) + (dict1[4] * dict2[2]) + (dict1[4] * dict2[3]))
      
        sumAwayTeamWin = ((dict2[1] * dict1[0]) + (dict2[2] * dict1[0]) + (dict2[2] * dict1[1]) +
                            (dict2[3] * dict1[0]) + (dict2[3] * dict1[1]) + (dict2[3] * dict1[2]) +
                            (dict2[4] * dict1[0]) + (dict2[4] * dict1[1]) + (dict2[4] * dict1[2]) + (dict2[4] * dict1[3]))

        sumDraw = ((dict1[0]*dict2[0])+(dict1[1]*dict2[1])+(dict1[2]*dict2[2])+(dict1[3]*dict2[3])+(dict1[4]*dict2[4]))

        finalDict.append([round(1 / sumHomeTeamWin,2), round(1 / sumDraw, 2), round(1 / sumAwayTeamWin,2)])
    print('*****************************************************************')
    print(finalDict)

# update the data after the match day
def updateAfterMatchDay(matchDayResults, laLigaTeamsDataDict):  
    for  match in matchDayResults:
        homeTeam = match['homeTeam']
        awayTeam = match['awayTeam']
        laLigaTeamsDataDict[homeTeam]['gsh'] += match['homeGoalsScored']
        laLigaTeamsDataDict[homeTeam]['gah'] += match['awayGoalsScored']
        laLigaTeamsDataDict[homeTeam]['gph'] += 1
        laLigaTeamsDataDict[awayTeam]['gsa'] += match['awayGoalsScored']
        laLigaTeamsDataDict[awayTeam]['gaa'] += match['homeGoalsScored']
        laLigaTeamsDataDict[awayTeam]['gpa'] += 1

# replace the teams names with more clear once
def replaceTeamsNames(teamsList):
    for match in teamsList:
        for key in ['homeTeam', 'awayTeam']:
             if match[key] in replacements:
                 match[key] = replacements[match[key]]
    return teamsList

# creates a main file after the match day
def dataForNextMatchDay(dataDict, fileName):
    path = Path(f'{fileName}.json')
    contents = json.dumps(dataDict, indent=0)
    path.write_text(contents)

laLigaTeamsDataDict = loadMatchDayData('mainData')
if not isMatchDayFinish:
# Load the data for the current match day
    laLigaTeamsDataWithAveragesDict = loadMatchDayData('mainData')
    matchGetter()
    matchDayList = loadMatchDayData('matchDayList')
    matchDayList=replaceTeamsNames(matchDayList)

# Calculate averages for each team and the league and 
    leagueAvarages = calculateAverages(laLigaTeamsDataWithAveragesDict)

# Calculate each team Attacking & Deffensive Strenght and 
# expected to score goals for their current game
    teamsExpextedToScoreList=calculateTeamsAttackingDefensiveStrength(matchDayList, leagueAvarages, laLigaTeamsDataWithAveragesDict )
    calculateProbability1(teamsExpextedToScoreList)


# Update data after the match day
if isMatchDayFinish:
    #resultsGetter()
    matchDayResults = loadMatchDayData('matchDayResults')
    matchDayResults=replaceTeamsNames(matchDayResults)
    updateAfterMatchDay(matchDayResults, laLigaTeamsDataDict)
    # Create an output file after the match day with updated data (an input file for the next match day)
    dataForNextMatchDay(laLigaTeamsDataDict, fileName = 'mainDataNew')





