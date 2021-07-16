from env import Env

def mergesort(env: Env):
	arr = env.arr
	n = len(arr)
	brr = env.malloc(n)

	for i in range(n):
		env.mov(brr + i, arr + i)

	splitmerge(env, brr, 0, n, arr)

def splitmerge(env: Env, brr, lo, hi, arr):
	if hi - lo < 2:
		return
	elif hi - lo == 2:
		if env.cmp(arr + lo, arr + (lo + 1)):
			env.swap(arr + lo, arr + (lo + 1))
		return

	mid = (lo + hi) // 2
	splitmerge(env, arr, lo, mid, brr)
	splitmerge(env, arr, mid, hi, brr)
	merge(env, brr, lo, mid, hi, arr)

def merge(env: Env, arr, lo, mid, hi, brr):
	i = lo
	j = mid
	k = lo

	while i < mid and j < hi:
		q = env.cmp(arr + i, arr + j)

		if q is False or q is None:
			env.mov(brr + k, arr + i)
			k += 1
			i += 1

		if q is True or q is None:
			env.mov(brr + k, arr + j)
			k += 1
			j += 1

	if i < mid:
		lo_extra = i
		hi_extra = mid
	elif j < hi:
		lo_extra = j
		hi_extra = hi
	else:
		return

	for l in range(lo_extra, hi_extra):
		env.mov(brr + k, arr + l)
		k += 1
