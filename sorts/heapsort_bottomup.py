from env import Env

def heapsort_bottomup(env):
	arr = env.arr
	heapify(env)

	for end in range(len(arr) - 1, 0, -1):
		env.swap(arr + end, arr)
		siftDown(env, 0, end)

def heapify(env: Env):
	end = len(env.arr)
	for start in range(iParent(end - 1), -1, -1):
		siftDown(env, start, end)

def siftDown(env, start, end):
	arr = env.arr
	j = leafSearch(env, start, end)

	while start != j:
		if env.cmp(arr + start, arr + j) is True:
			j = iParent(j)
		else:
			break

	while j > start:
		env.swap(arr + j, arr + start)
		j = iParent(j)


def leafSearch(env, start, end):
	arr = env.arr
	j = start
	while iRightChild(j) < end:
		lc, rc = iLeftChild(j), iRightChild(j)
		if env.cmp(arr + rc, arr + lc) is True:
			j = rc
		else:
			j = lc

	lc = iLeftChild(j)
	if lc < end:
		j = lc
	return j

def iParent(i):
	return (i - 1) // 2

def iLeftChild(i):
	return 2 * i + 1

def iRightChild(i):
	return 2 * i + 2