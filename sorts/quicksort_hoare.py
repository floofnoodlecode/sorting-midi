from env import Env


def quicksort_hoare(env: Env, lo=0, hi=None):
	if hi is None:
		hi = len(env.arr) - 1

	if lo < hi:
		p = partition(env, lo, hi)
		quicksort_hoare(env, lo, p - 1)
		quicksort_hoare(env, p + 1, hi)

def partition(env: Env, lo, hi):
	arr = env.arr

	pivot = (hi + lo) // 2
	i = lo
	j = hi

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