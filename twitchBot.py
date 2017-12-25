#Originally by enderminecraft34
# https://www.youtube.com/watch?v=C8zdnAwtKkU

import sys
import socket
import clickRequest
from clickRequest import collection

import math
import pprint
from bson.objectid import ObjectId


### Options (Don't edit)
SERVER = "irc.twitch.tv"  # server
PORT = 6667  # port
### Options (Edit this)
PASS = input("Enter OAUTH Key: ")  # bot password can be found on https://twitchapps.com/tmi/
BOT = "trophywagers"  # Bot's name [NO CAPITALS]
CHANNEL = "trophywagers"  # Channal name [NO CAPITALS]
OWNER = "trophywagers"  # Owner's name [NO CAPITALS]

### Functions

def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode())

def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user
def getMessage(line):
    global message
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message
def joinchat():
    readbuffer_join = "".encode()
    Loading = True
    while Loading:
        readbuffer_join = s.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        temp = readbuffer_join.split("\n")
        readbuffer_join = readbuffer_join.encode()
        readbuffer_join = temp.pop()
        for line in temp:
            Loading = loadingCompleted(line)
   # sendMessage(s, "Chat room joined!")
    print("Bot has joined " + CHANNEL + " Channel!")

def loadingCompleted(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True
### Code runs
s_prep = socket.socket()
s_prep.connect((SERVER, PORT))
s_prep.send(("PASS " + PASS + "\r\n").encode())
s_prep.send(("NICK " + BOT + "\r\n").encode())
s_prep.send(("JOIN #" + CHANNEL + "\r\n").encode())
s = s_prep
joinchat()
readbuffer = ""


def Console(line):
    # gets if it is a user or twitch server
    if "PRIVMSG" in line:
        return False
    else:
        return True

def ircLoop():
    while True:
            try:
                readbuffer = s.recv(1024)
                readbuffer = readbuffer.decode()
                temp = readbuffer.split("\n")
                readbuffer = readbuffer.encode()
                readbuffer = temp.pop()
            except:
                temp = ""
            for line in temp:
                if line == "":
                    break
                # So twitch doesn't timeout the bot.
                if "PING" in line and Console(line):
                    msgg = "PONG tmi.twitch.tv\r\n".encode()
                    s.send(msgg)
                    print(msgg)
                    break
                # get user
                user = getUser(line)
                # get message send by user
                message = getMessage(line)
                # for you to see the chat from CMD
                print(user + " > " + message)
                # sends private msg to the user (start line)
                PMSG = "/w " + user + " "

    ################################# Command ##################################
    ############ Here you can add as meny commands as you wish of ! ############
    ############################################################################

                if user == OWNER and "!command" in message:
                    sendMessage(s, "This can only be used by the owner")
                    break
                #if "!private" in message:
                #    sendMessage(s, PMSG + "This is a private message send to the user")
                #    break
                #if "!global" in message:
                #   sendMessage(s, "This is a global message send to the chat")
                #    break
                if "!bet" in message and user != 'nightbot':
                    try:
                        amount = message.split()
                        botBetOn = amount[2]
                        amount = amount[1]

                        if (float(amount).is_integer() and float(amount) > 0):

                            if (int(botBetOn) == 1 or int(botBetOn) == 2) and clickRequest.allowBets:
                                print("The bot is getting betted on")
                                if collection.find({"username": user}).count() <= 0:
                                    collection.insert({"username": user, "amount": 100})

                                userData = collection.find_one({"username": user})

                                #pprint.pprint(userData)
                                if int(amount) > int(userData["amount"]):
                                    amount = int(userData["amount"])
                                try:
                                    if len(clickRequest.bettingMatrix) < 3:
                                        clickRequest.bettingMatrix.append([])
                                        clickRequest.bettingMatrix.append([])
                                        clickRequest.bettingMatrix[1].append({'NA' : 1})
                                        clickRequest.bettingMatrix[2].append({'NA' : 1})

                                    clickRequest.bettingMatrix[int(botBetOn)].append({user : amount})
                                except:
                                    print("Actual matrix is issue")
                    except ValueError:
                        print("Invalid amount - Value Error")
                    except IndexError:
                        print("Invalid amount - Index Error")
                    except:
                        print(sys.exc_info()[0])
                        raise
                    break

                if "!odds" in message:
                    if not clickRequest.allowBets:
                        favor, displayOdds = clickRequest.odds(clickRequest.bettingMatrix[1], clickRequest.bettingMatrix[2])
                        if favor == 1:
                            oddsString = displayOdds + ": 1"
                            sendMessage(s, oddsString)
                        else:
                            oddsString = "1 : " + displayOdds
                            sendMessage(s, oddsString)
                    else:
                        print("Bets not yet available")
    ############################################################################