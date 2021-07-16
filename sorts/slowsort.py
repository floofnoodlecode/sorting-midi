def slowsort(env, i=0, j=None):
	arr = env.arr

	if j is None:
		j = len(arr) - 1

	if i >= j:
		return

	m = (i + j) // 2
	slowsort(env, i, m)
	slowsort(env, m+1, j)

	if env.cmp(arr + j, arr + m) is False:
		env.swap(arr + j, arr + m)
	slowsort(env, i, j-1)
