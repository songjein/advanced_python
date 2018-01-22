import time
import argparse
import numpy as np

from konlpy.tag import Komoran
komoran = Komoran()
fw = open("output.txt", "w")

def file_read_single():
	f = open("wise.txt")
	ret = []
	while True:
		l = f.readline()
		if not l: break
		ret.append(" ".join(komoran.nouns(l)) + "\n")
	return ret

if __name__ == "__main__":

	t1 = time.time()
	results = file_read_single()

	print("Took {}s".format(time.time() - t1))
