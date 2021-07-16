import inspect
import itertools as it
import math
import pytest
from random import randint

from env import Env
import sorts
from sorts.errors import ArrNotPow2


sortfs = inspect.getmembers(sorts, inspect.isfunction)


@pytest.fixture(params=[x[1] for x in sortfs], ids=[x[0] for x in sortfs])
def sortf(request):
	return request.param

def cmp_perfect(a, b):
	if a == b:
		return None
	return a > b

def run_sort(arr, sortf):
	env = Env(arr, cmp_perfect)
	env.run(sortf, trace=False)
	assert list(env.arr.block) == sorted(arr), f'Original: {arr}'




@pytest.mark.parametrize('repeat', list(range(5+1)))
def test_sort_short(sortf, repeat):
	for arr in it.product(range(repeat), repeat=repeat):
		try:
			run_sort(list(arr), sortf)
		except ArrNotPow2:
			break

def test_sort_stress_rand(sortf):
	for _ in range(100):
		l = randint(0, 52)
		arr = [randint(1,l) for _ in range(l)]

		try:
			run_sort(arr, sortf)
		except ArrNotPow2:
			l = 2 ** math.floor(math.log2(l))
			arr = arr[:l]

			run_sort(arr, sortf)
