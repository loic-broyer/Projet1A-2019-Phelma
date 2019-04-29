#coding: utf-8

import multiprocessing

def runMultiCore(core, functionPointer, arguments):
	manager = multiprocessing.Manager()
	return_dict = manager.dict()
	jobs = []
	for i in range(core):
		p = multiprocessing.Process(target = functionPointer, args = (return_dict)
		jobs.append(p)
		p.start()
	for proc in jobs:
		proc.join()
	return return_dict
	
