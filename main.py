
import os
import pgn
import eco

from numpy import *
from pymongo import MongoClient
import re

# database parameters for mongodb
DB_URL = 'localhost'
DB_PORT = 27017
DB_NAME = 'eco-record'


class MongoDB:
    def __init__(self):
        self.client = MongoClient(DB_URL, DB_PORT)
        self.db = self.client[DB_NAME]

    #def insert(username, eco, result):
       # post = {"name": username,   
      #          }
#data = {}


def create_eco_res():
    eco_res = [0] * 500
    return eco_res

    #print eco_res
#def parse_res(res_string):
#   if "1/2-1/2"


def update_eco_res(dataset, eco, res):
    # parse eco
    m = re.search('(?<=[A-E])\w+', eco)

    if 'A' in eco:
        index = int(m.group(0))
        if(index >= 0 and index < 100):
            dataset[index] = dataset[index] + res
    elif 'B' in eco:
        m = re.search('(?<=[A-E])\w+', eco)
        print int(m.group(0))
    elif 'C' in eco:
        m = re.search('(?<=[A-E])\w+', eco)
        print int(m.group(0))
    elif 'D' in eco:
        m = re.search('(?<=[A-E])\w+', eco)
        print int(m.group(0))
    else:
        pass


def save_eco(username, eco_res):
    if username not in data:
        data[username] = eco


# parse PGN file and output ECO code for each game
def parse_pgn(filename):
    path = os.path.join(filename)
    pgn_text = open(path).read()
    #pgn_game = pgn.PGNGame()

    games = pgn.loads(pgn_text)
    for game in games:
        #print game.moves
        #moves = game.moves[0]+" "+game.moves[1]+" "+game.moves[2]+" "+game.moves[3]
        print game.white
        print game.result
        print eco.from_moves(game.moves)[0][0]
    #print games[0].moves
    print pgn.dumps(games[0])


parse_pgn("./data/RR1600in2006Exp.pgn")

