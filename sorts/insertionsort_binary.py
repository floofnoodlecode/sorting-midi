from env import Env

def insertionsort_binary(env: Env):
	arr = env.arr

	for i in range(len(arr)):
		l, r = 0, i
		while l < r:
			m = (l + r) // 2
			q = env.cmp(arr + i, arr + m)

			if q is None:
				l = r = m
			elif q is False:
				r = m
			else:
				l = m + 1

		for j in range(i, r, -1):
			env.swap(arr + (j - 1), arr + j)