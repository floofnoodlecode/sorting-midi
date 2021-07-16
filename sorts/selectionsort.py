from env import Env

def selectionsort(env: Env):
	arr = env.arr
	n = len(arr)

	for i in range(n - 1):
		jmin = i
		for j in range(i + 1, n):
			if env.cmp(arr + j, arr + jmin) is False:
				jmin = j

		if jmin != i:
			env.swap(arr + i, arr + jmin)