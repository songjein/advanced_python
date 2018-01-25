import math
import time
import multiprocessing
from multiprocessing import Pool

FLAG_ALL_DONE = b"WORK_FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = b"WORKER_FINISHED_PROCESSING"

def check_prime(possible_primes_queue, definite_primes_queue):
	while True:	
		n = possible_primes_queue.get()
		if n == FLAG_ALL_DONE:
			# 모든 결과를 결과 대기열에 보냈음을 표시
			definite_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
			break
		else:
			if n % 2 == 0:
				continue
			for i in range(3, int(math.sqrt(n)) + 1, 2):
				if n % i == 0:
					break
			else:
				definite_primes_queue.put(n)

def feed_new_jobs(number_range, possible_primes_queue, nbr_poison_pills):
	print ("ADDING JOBS TO THE QUEUE")

	# fill the works into the shared queue
	for possible_prime in number_range:
		possible_primes_queue.put(possible_prime)
	print ("ALL JOBS ADDED TO THE QUEUE")

	# add poison pills to stop the remote workers
	for n in range(NBR_PROCESSES):	
		possible_primes_queue.put(FLAG_ALL_DONE)
	
				

if __name__ == "__main__":
	primes = []

	manager = multiprocessing.Manager()
	possible_primes_queue = manager.Queue()
	definite_primes_queue = manager.Queue()

	NBR_PROCESSES = 4
	pool = Pool(processes=NBR_PROCESSES)
	processes = []

	for _ in range(NBR_PROCESSES):
		p = multiprocessing.Process(
			target=check_prime,
			args=(
				possible_primes_queue,
				definite_primes_queue))
		processes.append(p)
		p.start()
	
	t1 = time.time()
	number_range = range(100000000, 101000000) # C

	import threading
	thrd = threading.Thread(target=feed_new_jobs, args=(
		number_range, possible_primes_queue, NBR_PROCESSES))
	thrd.start()

	print ("NOW WAITING FOR RESULTS")
	processors_indicating_they_have_finished = 0
	while True:
		# block whilst waiting for results
		new_result = definite_primes_queue.get()
		if new_result == FLAG_WORKER_FINISHED_PROCESSING:
			print ("WORKER {} HAS JUST FINISHED".format(processors_indicating_they_have_finished))
			processors_indicating_they_have_finished += 1
			if processors_indicating_they_have_finished == NBR_PROCESSES:
				break
		else:
			primes.append(new_result)
	assert processors_indicating_they_have_finished == NBR_PROCESSES


	print ("Took:", time.time() - t1)
	print (len(primes), primes[:10], primes[-10:])


