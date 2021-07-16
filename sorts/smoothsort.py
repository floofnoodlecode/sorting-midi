"""
Implementation ported from C++
Source: https://www.keithschwarz.com/interesting/code/?dir=smoothsort
"""

from copy import copy
from dataclasses import dataclass

from env import Env, Addr


# Compute leonardo numbers
kLeonardoNumbers = [1, 1]
while kLeonardoNumbers[-1] <= 2**32 - 1:
	kLeonardoNumbers.append(kLeonardoNumbers[-2] + kLeonardoNumbers[-1] + 1)
kLeonardoNumbers.pop()


def smoothsort(env: Env):
	arr = env.arr
	n = len(arr)

	if n <= 1:
		return

	shape = HeapShape(trees=0, smallestTreeSize=0)

	end = arr + n
	for i in range(n):
		LeonardoHeapAdd(env, arr, arr + i, end, shape)

	for i in range(n, 0, -1):
		LeonardoHeapRemove(env, arr, arr + i, shape)

@dataclass
class HeapShape:
	trees: int
	smallestTreeSize: int

def SecondChild(root: Addr):
	return root - 1

def FirstChild(root: Addr, size: int):
	return SecondChild(root) - kLeonardoNumbers[size - 2]

def LargerChild(env: Env, root: Addr, size: int):
	first = FirstChild(root, size)
	second = SecondChild(root)

	return second if env.cmp(second, first) else first

def RebalanceSingleHeap(env: Env, root: Addr, size: int):
	while size > 1:
		first = FirstChild(root, size)
		second = SecondChild(root)

		if env.cmp(second, first):
			largerChild = second
			childSize = size - 2
		else:
			largerChild = first
			childSize = size - 1

		if not env.cmp(largerChild, root):
			return

		env.swap(root, largerChild)
		root = largerChild
		size = childSize

def LeonardoHeapRectify(env: Env, begin: Addr, end: Addr, shape: HeapShape):
	shape = copy(shape)
	itr = end - 1

	while True:
		lastHeapSize = shape.smallestTreeSize

		if (itr - begin) == (kLeonardoNumbers[lastHeapSize] - 1):
			break

		toCompare = itr

		if shape.smallestTreeSize > 1:
			largeChild = LargerChild(env, itr, shape.smallestTreeSize)

			if env.cmp(largeChild, toCompare):
				toCompare = largeChild

		priorHeap = itr - kLeonardoNumbers[lastHeapSize]

		if not env.cmp(priorHeap, toCompare):
			break

		env.swap(itr, priorHeap)
		itr = priorHeap

		while True:
			shape.trees >>= 1
			shape.smallestTreeSize += 1
			if shape.trees & 1:
				break

	RebalanceSingleHeap(env, itr, lastHeapSize)

def LeonardoHeapAdd(env: Env, begin: Addr, end: Addr, heapEnd: Addr, shape: HeapShape):
	if not shape.trees & 1:
		shape.trees |= 1
		shape.smallestTreeSize = 1
	elif shape.trees & 3 == 3:
		shape.trees >>= 2
		shape.trees |= 1
		shape.smallestTreeSize += 2
	elif shape.smallestTreeSize == 1:
		shape.trees <<= 1
		shape.smallestTreeSize = 0
		shape.trees |= 1
	else:
		shape.trees <<= shape.smallestTreeSize - 1
		shape.trees |= 1
		shape.smallestTreeSize = 1

	isLast = False
	if shape.smallestTreeSize == 0:
		if end + 1 == heapEnd:
			isLast = True
	elif shape.smallestTreeSize == 1:
		if (end + 1 == heapEnd) or (end + 2 == heapEnd and shape.trees & 2 != 2):
			isLast = True
	else:
		if (heapEnd - end - 1) < kLeonardoNumbers[shape.smallestTreeSize - 1] + 1:
			isLast = True

	if not isLast:
		RebalanceSingleHeap(env, end, shape.smallestTreeSize)
	else:
		LeonardoHeapRectify(env, begin, end + 1, shape)

def LeonardoHeapRemove(env: Env, begin: Addr, end: Addr, shape: HeapShape):
	if shape.smallestTreeSize <= 1:
		while True:
			shape.trees >>= 1
			shape.smallestTreeSize += 1
			if not (shape.trees != 0 and not shape.trees & 1):
				return

	heapOrder = shape.smallestTreeSize
	shape.trees &= ~1
	shape.trees <<= 2
	shape.trees |= 3
	shape.smallestTreeSize -= 2

	leftHeap = FirstChild(end - 1, heapOrder)
	rightHeap = SecondChild(end - 1)

	allButLast = copy(shape)
	allButLast.smallestTreeSize += 1
	allButLast.trees >>= 1

	LeonardoHeapRectify(env, begin, leftHeap + 1, allButLast)
	LeonardoHeapRectify(env, begin, rightHeap + 1, shape)
