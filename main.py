
import os
import pgn
import eco
import ast
from numpy import *
from numpy.random import random
import peach as p
from os import remove, close
from tempfile import mkstemp
from shutil import move
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

"""
x = array( [
    [ 0., 0. ], [ 0., 1. ], [ 0., 2. ], [ 1., 0. ], [ 1., 1. ], [ 1., 2. ],
    [ 2., 0. ], [ 2., 1. ], [ 2., 2. ], [ 5., 5. ], [ 5., 6. ], [ 5., 7. ],
    [ 6., 5. ], [ 6., 6. ], [ 6., 7. ], [ 7., 5. ], [ 7., 6. ], [ 7., 7. ] ] )

mu = array( [
    [ 0.7, 0.3 ], [ 0.7, 0.3 ], [ 0.7, 0.3 ], [ 0.7, 0.3 ], [ 0.7, 0.3 ],
    [ 0.7, 0.3 ], [ 0.7, 0.3 ], [ 0.7, 0.3 ], [ 0.7, 0.3 ], [ 0.3, 0.7 ],
    [ 0.3, 0.7 ], [ 0.3, 0.7 ], [ 0.3, 0.7 ], [ 0.3, 0.7 ], [ 0.3, 0.7 ],
    [ 0.3, 0.7 ], [ 0.3, 0.7 ], [ 0.3, 0.7 ] ] )

x = array([['A','B'],['A','B'],['A','B'],['A','B'],['A','B'],['A','B']])
print x
mu = array([[ 0.7, 0.3 ],[ 0.7, 0.3 ],[ 0.7, 0.3 ],[ 0.7, 0.3 ],[ 0.7, 0.3 ],[ 0.7, 0.3 ]])
print mu
m = 1.25
#fcm = p.FuzzyCMeans(x, mu, m)

print fcm(emax=0)
print fcm.mu
"""



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
        update_existing_record(playername, eco_res)
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
            try:
                old_eco_res = ast.literal_eval(result_set[1])  # change string to list
            except Exception, e:
                raise e
            #print old_eco_res[0]
            #print new_eco_res[0]
            func = lambda x, y: x+y
            eco_res = map(func, old_eco_res, new_eco_res)
            eco_res_str = playername+"  "+convert_list_to_string(eco_res)
            old_eco_res_str = playername+"  "+convert_list_to_string(old_eco_res)
            #print eco_res_str
            #print old_eco_res_str
            replace(RESULT, old_eco_res_str, eco_res_str)


def replace(file_path, pattern, subst):
    # create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #remove original file
    remove(file_path)
    #move new file
    move(abs_path, file_path)


def convert_list_to_string(list):
    return "".join(str(list))


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
        save_eco(playername, eco_res)


parse_pgn("./data/RR1600in2006Exp.pgn")
