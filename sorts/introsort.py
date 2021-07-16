import math

from env import Env

def introsort(env, begin=0, end=None, maxdepth=3):
	if end is None:
		end = len(env.arr)
	n = end - begin

	if n <= 1:
		return

	if n <= 10:
		insertionsort(env, begin, end)
		print('insert', n)
	elif maxdepth == 0:
		heapsort_bottomup(env, begin, end)
		print('heap', n)
	else:
		p = partition(env, begin, end)
		introsort(env, begin, p, maxdepth - 1)
		introsort(env, p + 1, end, maxdepth - 1)


# INSERTIONSORT ------------------------------------
def insertionsort(env, lo, hi):
	arr = env.arr
	for i in range(lo, hi):
		for j in range(i, lo, -1):
			if env.cmp(arr + (j - 1), arr + j):
				env.swap(arr + (j - 1), arr + j)
			else:
				break

# HEAPSORT -----------------------------------------
from env import Env

def heapsort_bottomup(env, begin, end):
	arr = env.arr
	heapify(env, begin, end)

	for end in range(end - 1, begin, -1):
		env.swap(arr + end, arr + begin)
		siftDown(env, begin, begin, end)

def heapify(env: Env, begin, end):
	for start in range(iParent(begin, end - 1), begin - 1, -1):
		siftDown(env, begin, start, end)

def siftDown(env, begin, start, end):
	arr = env.arr
	j = leafSearch(env, begin, start, end)

	while start != j:
		if env.cmp(arr + start, arr + j) is True:
			j = iParent(begin, j)
		else:
			break

	while j > start:
		env.swap(arr + j, arr + start)
		j = iParent(begin, j)


def leafSearch(env, begin, start, end):
	arr = env.arr
	j = start
	while iRightChild(begin, j) < end:
		lc, rc = iLeftChild(begin, j), iRightChild(begin, j)
		if env.cmp(arr + rc, arr + lc) is True:
			j = rc
		else:
			j = lc

	lc = iLeftChild(begin, j)
	if lc < end:
		j = lc
	return j

def iParent(begin, i):
	return (i - begin - 1) // 2 + begin

def iLeftChild(begin, i):
	return 2 * (i - begin) + 1 + begin

def iRightChild(begin, i):
	return 2 * (i - begin) + 2 + begin


# QUICKSORT ------------------------------------------
def quicksort_hoare(env: Env, lo=0, hi=None):
	if hi is None:
		hi = len(env.arr)

	if lo < hi - 1:
		p = partition(env, lo, hi)
		quicksort_hoare(env, lo, p - 1)
		quicksort_hoare(env, p + 1, hi)

def partition(env: Env, lo, hi):
	arr = env.arr

	pivot = (hi - 1 + lo) // 2
	i = lo
	j = hi - 1

	while True:
		while i < pivot:
			if env.cmp(arr + i, arr + pivot) is True:
				break
			i += 1

		while j > pivot:
			if env.cmp(arr + j, arr + pivot) is False:
				break
			j -= 1

		if i == j:
			return pivot

		env.swap(arr + i, arr + j)

		if pivot == i:
			pivot = j
			i += 1
		elif pivot == j:
			pivot = i
			j -= 1
		else:
			i += 1
			j -= 1