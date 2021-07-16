from env import Env

def heapsort(env: Env):
	arr = env.arr
	heapify(env)

	for end in range(len(arr) - 1, 0, -1):
		env.swap(arr + end, arr)
		siftDown(env, 0, end)

def heapify(env: Env):
	end = len(env.arr)
	for start in range(iParent(end - 1), -1, -1):
		siftDown(env, start, end)

def siftDown(env: Env, start, end):
	arr = env.arr
	root = start

	while iLeftChild(root) < end:
		child = iLeftChild(root)
		swap = root

		if env.cmp(arr + swap, arr + child) is False:
			swap = child

		if child + 1 < end:
			if env.cmp(arr + swap, arr + (child + 1)) is False:
				swap = child + 1

		if swap == root:
			return

		env.swap(arr + root, arr + swap)
		root = swap

def iParent(i):
	return (i - 1) // 2

def iLeftChild(i):
	return 2 * i + 1