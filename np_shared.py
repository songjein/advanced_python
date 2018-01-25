import os
import multiprocessing
from collections import Counter
import ctypes
import numpy as np
from prettytable import PrettyTable

SIZE_A, SIZE_B = 10000, 80000

def worker_fn(idx):
	"""Do some work on the shared np array on row idx"""
	# confirm that no other process has modified this value already
	assert main_nparray[idx, 0] == DEFAULT_VALUE
	if idx % 1000 == 0:
		print (" {}: with idx {} \n id of local_nparray_in_process is {} in PID {}"\
					.format(worker_fn.__name__, idx, id(main_nparray), os.getpid()))
	main_nparray[idx, :] = os.getpid()

if __name__ == '__main__':
	DEFAULT_VALUE = 42
	NBR_OF_PROCESSES = 4

	# create a block of bytes, reshaepd into a local numpy array
	NBR_ITEMS_IN_ARRAY = SIZE_A * SIZE_B
	shared_array_base = multiprocessing.Array(
		ctypes.c_double, NBR_ITEMS_IN_ARRAY, lock=False)
	main_nparray = np.frombuffer(shared_array_base, dtype=ctypes.c_double)
	main_nparray = main_nparray.reshape(SIZE_A, SIZE_B)

	assert main_nparray.base.base is shared_array_base
	print ("Created shared array with {} nbytes".format(main_nparray.nbytes))
	print ("Shared array id is {} in PID {}".format(id(main_nparray), os.getpid()))
	print ("Starting with an array of 0 values")
	print (main_nparray)
	print ()

	# Modify the data via our local numpy array
	main_nparray.fill(DEFAULT_VALUE)
	print ("Original array filled with value {}:".format(DEFAULT_VALUE))
	print (main_nparray)

	input("Press a key to start workers using multiprocessing...")
	print ()

	# create a pool of processes that whill share the memory block
	# of the global numpy array, share the ref to the underlying
	# block of data so we can build a numpy array wrapper in the new processes
	pool = multiprocessing.Pool(processes=NBR_OF_PROCESSES)
	# perform a map where each row index is passed as a parameter to the worker_fn
	pool.map(worker_fn, range(SIZE_A))

	print ()
	print ("The default value has been over-written with worker_fn's result:")
	print (main_nparray)
	print ()
	print ("Verification - extracting unique values from {:,} items\n in the numpy array(this might be slow)...".format(NBR_ITEMS_IN_ARRAY))
	# main_nparray.flat iterates over the contents of the array, it doesn't
	# make a copy
	counter = Counter(main_nparray.flat)
	print ("Unique values in main_nparray:")
	tbl = PrettyTable(["PID", "Counter"])
	for pid, count in counter.items():
		tbl.add_row([pid, count])
	print (tbl)

	total_items_set_in_array = sum(counter.values())
	
	# check that we have set every item in the array away from DEFAULT_VALUE
	assert DEFAULT_VALUE not in counter.keys()
	# check that we have accounted for every item in the array
	assert total_items_set_in_array == NBR_ITEMS_IN_ARRAY
	# check that we have NBR_OF_PROCESSES of unique keys to confirm that every
	# process did some of the work
	assert len(counter) == NBR_OF_PROCESSES

	input("Press a key to exit...")


