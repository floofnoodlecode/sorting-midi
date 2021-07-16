def cocktailshakersort(env):
	arr = env.arr

	start = 0
	end = len(arr) - 2
	while start <= end:
		start_, end_ = end, start
		for i in range(start, end + 1):
			if env.cmp(arr + i, arr + (i + 1)) is True:
				env.swap(arr + i, arr + (i + 1))
				end_ = i

		end = end_ - 1
		for i in range(end, start - 1, -1):
			if env.cmp(arr + i, arr + (i + 1)) is True:
				env.swap(arr + i, arr + (i + 1))
				start_ = i

		start = start_ + 1