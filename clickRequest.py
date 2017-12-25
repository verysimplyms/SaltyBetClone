import pyautogui
import time
import pymongo
import math

allowBets = False
previousRequest = time.time()

client = pymongo.MongoClient('localhost', 27017)
db = client['trophywagers']
collection = db['users']
bettingMatrix = []
bettingMatrix.append({'NA' : None})


def odds(p1, p2):
    p1Amount = 1
    p2Amount = 1

    print(p1)

    for values in p1.items():

        p1Amount = p1Amount + values[1]

    for values in p1.items():

        p2Amount = p2Amount + values[1]

    if p1Amount > p2Amount:
        odds = p1Amount / p2Amount
        return 1, odds

    else:
        odds = p2Amount / p1Amount
        return 2, odds

def payouts(players, winningPlayer):
    favor, multiplier = odds(players[1], players[2])

    if winningPlayer == 1:
        winners = players[1]
        losers = players[2]
    else:
        winners = players[2]
        losers = players[1]

    for i in winners:
        if favor == 1 and winners[i][0] != "NA":
            if winningPlayer == 1:
                userData = collection.find({"username": winners[i][0]})
                winnerData = [{"username": winners[i][0], "amount": (int(userData['amount']) + (math.ciel(float(winners[i][1]) / multiplier)) )}]
                collection.replace_one(winnerData, True)
            else:
                userData = collection.find({"username": winners[i][0]})
                winnerData = [{"username": winners[i][0], "amount": (int(userData['amount']) + (math.ciel(float(winners[i][1]) * multiplier)) )}]
                collection.replace_one(winnerData, True)

        elif winners[i][0] != "NA":
            if winningPlayer == 1:
                userData = collection.find({"username": winners[i][0]})
                winnerData = [{"username": winners[i][0], "amount": (int(userData['amount']) + (math.ciel(float(winners[i][1]) * multiplier)) )}]
                collection.replace_one(winnerData, True)

            else:
                userData = collection.find({"username": winners[i][0]})
                winnerData = [{"username": winners[i][0], "amount": (int(userData['amount']) + (math.ciel(float(winners[i][1]) / multiplier)) )}]
                collection.replace_one(winnerData, True)

    for i in losers:
        if losers[i][0] != "NA":
            userData = collection.find({"username": losers[i][0]})
            loserData = [{"username": losers[i][0], "amount": (int(userData['amount']) - math.ciel(float(winners[i][1])))}]
            collection.replace_one(loserData, True)


def clickRequest(winner):
    global previousRequest
    global allowBets

    if time.time() - previousRequest > 30:
        # Payouts
        try:
            payouts(bettingMatrix, winner)
            print("Payouts code was ran")
        except Exception as e:
            print(e)

        allowBets = True

        pyautogui.click(clicks=8, interval=.5)
        pyautogui.moveRel(-30, 0)

        pyautogui.click(clicks=4, interval= 10)
        pyautogui.moveRel(30, 0)

        previousRequest = time.time()
        allowBets = False
    else:
        allowBets = False