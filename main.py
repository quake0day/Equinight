
import os
import pgn

def parse_pgn(filename):
	path = os.path.join(filename)
	pgn_text = open(path).read()
	pgn_game = pgn.PGNGame()

	games = pgn.loads(pgn_text)
	for game in games:
		print game.moves[0]
	#print games[0].moves
	#print pgn.dumps(games[0])



parse_pgn("./data/RR1600in2006Exp.pgn")