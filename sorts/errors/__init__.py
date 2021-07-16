import math

class ArrNotPow2(Exception):
	pass

def raise_pow2(n):
	if n < 2:
		return

	if not math.log2(n).is_integer():
		raise ArrNotPow2(n)