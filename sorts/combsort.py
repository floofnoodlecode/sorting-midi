def combsort(env):
	arr = env.arr
	n = len(arr)

	gap = n
	shrink = 1.3
	done = False

	while not done:
		gap = int(gap / shrink)
		if gap <= 1:
			gap = 1
			done = True

		for i in range(n - gap):
			if env.cmp(arr + i, arr + (i + gap)) is True:
				env.swap(arr + i, arr + (i + gap))
				done = False