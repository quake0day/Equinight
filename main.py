
import os
import pgn
import eco
import ast
from numpy import *
from pymongo import MongoClient
import re

# database parameters for mongodb
DB_URL = 'localhost'
DB_PORT = 27017
DB_NAME = 'eco-record'
RESULT = 'result.txt'
global result_set

class MongoDB:
    def __init__(self):
        self.client = MongoClient(DB_URL, DB_PORT)
        self.db = self.client[DB_NAME]

    #def insert(playername, eco, result):
       # post = {"name": playername,   
      #          }
#data = {}


def create_eco_res():
    eco_res = [0] * 500
    return eco_res


# parse text result to a number
def parse_res(res_string):
    if "1/2-1/2" in res_string:
        res = 0.5
    elif "1-0" in res_string:
        res = 1
    elif "0-1" in res_string:
        res = 0
    return res


def cal_eco_res(dataset, eco, res):
    # parse eco
    m = re.search('(?<=[A-E])\w+', eco)
    index = int(m.group(0))
    if 'A' in eco:
        if(index >= 0 and index < 100):
            dataset[index] = dataset[index] + res
    elif 'B' in eco:
        if(index >= 0 and index < 100):
            index = index + 100
            dataset[index] = dataset[index] + res
    elif 'C' in eco:
            index = index + 200
            dataset[index] = dataset[index] + res
    elif 'D' in eco:
        if(index >= 0 and index < 100):
            index = index + 300
            dataset[index] = dataset[index] + res
    elif 'E' in eco:
        if(index >= 0 and index < 100):
            index = index + 400
            dataset[index] = dataset[index] + res
    else:
        pass
    return dataset


def save_eco(playername, eco_res):
    result_set = ["", ""]
    result_set[0] = playername
    result_set[1] = eco_res
    #print result_set
    if(find_existing_record(playername)):
        pass
    else:
        fr = open(RESULT, 'a+')
        for item in result_set:
            fr.write("%s  " % item)
        fr.write("\n")
        fr.close()
    #number_of_lines = len(fr.readlines())

    #if playername not in data:
        #data[playername] = eco


def update_existing_record(playername, new_eco_res):
    fr = open(RESULT, 'r+')
    for line in fr.readlines():
        if line.find(playername) >= 0:
            result_set = read_list_from_line(line)
            old_eco_res = ast.literal_eval(result_set[1])  # change string to list
            print old_eco_res[0]
            print new_eco_res[0]
            func = lambda x, y: x+y
            eco_res = map(func, old_eco_res, new_eco_res)
            print eco_res
            #s = line.replace("")


def read_list_from_line(line):
    result_set = ["", ""]
    data = line.split("  ")
    if(len(data) == 3):
        result_set[0] = data[0]
        result_set[1] = data[1]
    return result_set


def find_existing_record(playername):
    fr = open(RESULT, 'r+')
    for line in fr.readlines():
        if line.find(playername) >= 0:
            return True
    return False


# parse PGN file and output ECO code for each game
def parse_pgn(filename):
    path = os.path.join(filename)
    pgn_text = open(path).read()
    #pgn_game = pgn.PGNGame()
    games = pgn.loads(pgn_text)
    for game in games:
        #print game.moves
        #moves = game.moves[0]+" "+game.moves[1]+" "+game.moves[2]+" "+game.moves[3]
        #print game.result
        res = parse_res(game.result)
        eco_ = eco.from_moves(game.moves)[0][0]
        dataset = create_eco_res()
        playername = game.white
        eco_res = cal_eco_res(dataset, eco_, res)
        #save_eco(playername, eco_res)
        update_existing_record(playername, eco_res)

    #print games[0].moves
    #print pgn.dumps(games[0])


parse_pgn("./data/RR1600in2006Exp.pgn")

