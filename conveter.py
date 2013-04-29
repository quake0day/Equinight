import os
RESULT = 'result.txt'
RESULT_CSV = 'result.csv'
fk = open(RESULT_CSV,'w+')
fr = open(RESULT, "r+")
for line in fr.readlines():
	name = line.split("  ")[0]
	name_piece = name.split(",")
	if(len(name_piece) > 1):
		name = name_piece[0] + " " +name_piece[1]
	else:
		name = name_piece[0]
	score = line.split("  ")[1]
	data = name+","+score[1:-1]
	print data
	print>> fk, data
fk.close()
	#fk.write()