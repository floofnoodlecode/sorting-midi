def oddevensort(env):
	arr = env.arr
	n = len(arr)

	done = False
	while not done:
		done = True

		for i in range(1, n-1, 2):
			if env.cmp(arr + i, arr + (i + 1)):
				env.swap(arr + i, arr + (i + 1))
				done = False

		for i in range(0, n-1, 2):
			if env.cmp(arr + i, arr + (i + 1)):
				env.swap(arr + i, arr + (i + 1))
				done = False