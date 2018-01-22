import time
import argparse
import numpy as np

from konlpy.tag import Komoran

def file_read_parallel(file_idx):
	komoran = Komoran()
	f = open("{}.txt".format(file_idx))
	ret = []
	while True:
		l = f.readline()
		if not l: break
		ret.append(" ".join(komoran.nouns(l)) + "\n")
	return ret

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="File read parallel")
	parser.add_argument(
		'nbr_workers', type=int, help="Number of workers e.g. 1,2,4,8")
	parser.add_argument(
		'--processes',
		action="store_true",
		default=False,
		help='True if using processes, absent (False) for Threads')
	
	args = parser.parse_args()
	if args.processes:
		print("Using Processes")
		from multiprocessing import Pool
	else:
		print ("Using Thread")
		from multiprocessing.dummy import Pool

	parallel_blocks = args.nbr_workers 

	pool = Pool(processes=parallel_blocks)

	map_inputs = range(parallel_blocks)
	t1 = time.time()
	results = pool.map(file_read_parallel, map_inputs)
	pool.close()


	print("Took {}s".format(time.time() - t1))

	print (results[0])

	'''
	f = open("output.txt", "w")
	for r in results:	
		for l in r:	
			f.write("{}\n".format(r))
	'''
