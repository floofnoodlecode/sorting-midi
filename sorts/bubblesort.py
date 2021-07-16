from env import Env

def bubblesort(env: Env):
	arr = env.arr

	n = len(arr)
	while n > 1:
		newn = 0
		for i in range(1, n):
			if env.cmp(arr + (i - 1), arr + i) is True:
				env.swap(arr + (i - 1), arr + i)
				newn = i
		n = newn