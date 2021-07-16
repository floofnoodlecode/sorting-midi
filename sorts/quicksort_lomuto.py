"""
https://en.wikipedia.org/wiki/Quicksort
"""

from env import Env


def quicksort_lomuto(env: Env, lo=0, hi=None):
	if hi is None:
		hi = len(env.arr) - 1

	if lo < hi:
		p = partition(env, lo, hi)
		quicksort_lomuto(env, lo, p - 1)
		quicksort_lomuto(env, p + 1, hi)

def partition(env: Env, lo, hi):
	arr = env.arr

	i = lo
	for j in range(lo, hi):
		if env.cmp(arr + j, arr + hi) is False:
			if i != j:
				env.swap(arr + i, arr + j)
			i += 1
	if i != hi:
		env.swap(arr + i, arr + hi)
	return i