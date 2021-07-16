from env import Env

def selectionsort_bi(env: Env):
	arr = env.arr
	n = len(arr)

	for i in range(n // 2):
		end = n - 1 - i
		if env.cmp(arr + i, arr + end) is False:
			jmin = i
			jmax = end
		else:
			jmin = end
			jmax = i


		for j in range(i + 1, n // 2):
			j2 = n - 1 - j
			if env.cmp(arr + j, arr + j2) is False:
				if env.cmp(arr + j, arr + jmin) is False:
					jmin = j
				if env.cmp(arr + j2, arr + jmax) is True:
					jmax = j2
			else:
				if env.cmp(arr + j2, arr + jmin) is False:
					jmin = j2
				if env.cmp(arr + j, arr + jmax) is True:
					jmax = j

		if n % 2 == 1:
			n2 = n // 2
			if jmin != n2 and not env.cmp(arr + n2, arr + jmin):
				jmin = n2
			elif jmax != n2 and env.cmp(arr + n2, arr + jmax) is True:
				jmax = n2

		if jmin != i:
			env.swap(arr + i, arr + jmin)
		if jmax != end:
			if jmax != i:
				env.swap(arr + end, arr + jmax)
			elif jmin != end:
				env.swap(arr + end, arr + jmin)