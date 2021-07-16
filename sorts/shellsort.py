from math import ceil

def shellsort(env):
	arr = env.arr
	n = len(arr)

	gaps = [1]
	while True:
		gap = gaps[-1] * 2.25 + 1
		if gap < n:
			gaps.append(gap)
		else:
			break
	gaps = [ceil(x) for x in gaps[::-1]]

	for gap in gaps:
		for i in range(gap, n):
			for j in range(i, gap - 1, -gap):
				if env.cmp(arr + j, arr + (j - gap)) is False:
					env.swap(arr + j, arr + (j - gap))
				else:
					break