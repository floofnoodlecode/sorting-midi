def gnomesort(env):
	arr = env.arr
	n = len(arr)

	pos = 0
	while pos < n:
		if pos == 0 or env.cmp(arr + pos, arr + (pos - 1)) is not False:
			pos += 1
		else:
			env.swap(arr + pos, arr + (pos - 1))
			pos -= 1