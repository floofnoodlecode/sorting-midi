def stoogesort(env, i=0, j=None):
	arr = env.arr

	if j is None:
		j = len(arr) - 1
		if j < 1:
			return

	if env.cmp(arr + i, arr + j):
		env.swap(arr + i, arr + j)

	if j - i + 1 > 2:
		t = (j - i + 1) // 3
		stoogesort(env, i, j - t)
		stoogesort(env, i + t, j)
		stoogesort(env, i, j - t)
