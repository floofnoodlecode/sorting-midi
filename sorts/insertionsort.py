from env import Env

def insertionsort(env: Env):
	arr = env.arr
	for i in range(len(arr)):
		for j in range(i, 0, -1):
			if env.cmp(arr + (j - 1), arr + j):
				env.swap(arr + (j - 1), arr + j)
			else:
				break