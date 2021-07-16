def bitonicsort(env, lo=0, n=None, asc=True):
	if n is None:
		n = len(env.arr)

	if n > 1:
		m = n // 2
		bitonicsort(env, lo, m, not asc)
		bitonicsort(env, lo + m, n - m, asc)
		bitonicmerge(env, lo, n, asc)

def bitonicmerge(env, lo, n, asc):
	if n > 1:
		arr = env.arr

		m = ceilpow2(n)
		for i in range(lo, lo + n - m):
			if env.cmp(arr + i, arr + (i + m)) is asc:
				env.swap(arr + i, arr + (i + m))

		bitonicmerge(env, lo, m, asc)
		bitonicmerge(env, lo + m, n - m, asc)

def ceilpow2(n):
	k = 1
	while 0 < k < n:
		k <<= 1
	return k >> 1
