from argparse import ArgumentParser
import logging
import os
from random import randint
import subprocess

from env import Env
from render import generate_audio, generate_animation
from sorts import *

SORT2TITLE = {
	bitonicsort: 'Bitonic sort',
	bubblesort: 'Bubble sort',
	cocktailshakersort: 'Cocktail Shaker sort',
	combsort: 'Comb sort',
	gnomesort: 'Gnome sort',
	heapsort: 'Heapsort',
	heapsort_bottomup: 'Heapsort (Bottom-Up)',
	insertionsort: 'Insertion sort',
	insertionsort_binary: 'Insertion sort (Binary)',
	introsort: 'Introsort',
	mergesort: 'Merge sort',
	mergesort_half: 'Merge sort (Half Buffer)',
	oddevensort: 'Odd-even Sort',
	quicksort_hoare: 'Quicksort (Hoare)',
	quicksort_lomuto: 'Quicksort (Lomuto)',
	selectionsort: 'Selection sort',
	selectionsort_bi: 'Selection sort (Bidirectional)',
	shellsort: 'Shellsort',
	slowsort: 'Slowsort',
	smoothsort: 'Smoothsort',
	stoogesort: 'Stooge sort',
}

def cmp_perfect(a, b):
	if a == b:
		return None
	return a > b

def main():
	argparse = ArgumentParser()
	argparse.add_argument('-s', '--sort', type=str, help='Sorting algorithm function name (e.g. bubblesort, quicksort_lomuto, etc.')
	argparse.add_argument('-n', '--size', type=int, help='Array size')
	args = argparse.parse_args()

	arr = [randint(1, args.size) for _ in range(args.size)]
	print(arr)
	cmp = cmp_perfect

	SORT = globals()[args.sort]
	env = Env(arr, cmp)
	env.run(SORT)
	if sorted(arr) != list(env.arr.block):
		logging.critical('Array is not sorted\n%s\n%s', sorted(arr), list(env.arr.block))

	print(env.stats)

	OUTDIR = 'out/'
	if not os.path.exists(OUTDIR):
		os.makedirs(OUTDIR)
	audio_filename = OUTDIR + SORT.__name__ + '_audio.wav'
	anim_filename = OUTDIR + SORT.__name__ + '_anim.mp4'

	generate_audio(env, filename=audio_filename)
	generate_animation(env, start_delay=2, title=SORT2TITLE[SORT], filename=anim_filename)

	subprocess.run([
		'ffmpeg',
		'-y',
		'-i', anim_filename,
		'-i', audio_filename,
		'-c:v', 'copy',
		'-c:a', 'aac',
		'-af', 'adelay=delays=2s:all=1',
		OUTDIR + SORT.__name__ + '.mp4'
	])

if __name__ == '__main__':
	main()