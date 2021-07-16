"""
http://kicia.ift.uni.wroc.pl/algorytmy/mergesortpaper.pdf
"""


from env import Env, Addr


def mergesort_half(env):
	al = env.arr
	ah = al + len(al)

	if ah - al < 2:
		return

	m = al + (ah - al) // 2
	buff = env.malloc(ah - m)
	copying_mergesort(env, m, ah, buff)
	copying_mergesort(env, al, m, ah - (m - al))
	merge(env, buff, buff + (ah - m), ah - (m - al), ah)

def copying_mergesort(env, al, ah, bl):
	if ah - al == 0:
		return
	elif ah - al == 1:
		env.mov(bl, al)
		return

	m = al + (ah - al) // 2
	copying_mergesort(env, m, ah, bl + (m - al))
	copying_mergesort(env, al, m, m)
	merge(env, m, m + (m - al), bl + (m - al), bl + (ah - al))

def merge(env: Env, p1: Addr, k1: Addr, p2: Addr, k2: Addr):
	p = p2 - (k1 - p1)
	while True:
		q = env.cmp(p1, p2)

		if q is True or q is None:
			env.mov(p, p2)
			p += 1
			p2 += 1
			if p2 == k2:
				break

		if q is False or q is None:
			env.mov(p, p1)
			p += 1
			p1 += 1
			if p1 == k1:
				return

	while p1 != k1:
		env.mov(p, p1)
		p += 1
		p1 += 1
