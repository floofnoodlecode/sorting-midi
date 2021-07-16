from copy import deepcopy
import itertools as it
import math
from random import randint
import subprocess
from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mido
import numpy as np
from tqdm import tqdm

from env import Env
from env.events import *

DEFAULT_TEMPO = 500_000
DEFAULT_TICKS_PER_BEAT = 480


def generate_audio(env: Env, tempo=DEFAULT_TEMPO, ticks_per_beat=DEFAULT_TICKS_PER_BEAT, filename='audio.wav'):
	env = deepcopy(env)

	blocks = env.mem.blocks
	events = env.events
	[e.revert() for e in events[::-1]]

	mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
	track = mid.add_track()

	track.append(mido.MetaMessage('set_tempo', tempo=tempo))

	INSTRUMENTS = [randint(0, 127) for _ in range(len(blocks))]
	print('INSTRUMENTS:', INSTRUMENTS)
	block2ch = {b: 2*i for i, b in enumerate(blocks)}
	for ch, ins in zip(block2ch.values(), INSTRUMENTS):
		track.append(mido.Message('program_change', channel=ch, program=ins))
		track.append(mido.Message('control_change', channel=ch, control=10, value=0))
		track.append(mido.Message('program_change', channel=ch+1, program=ins))
		track.append(mido.Message('control_change', channel=ch+1, control=10, value=127))
	track.append(mido.Message('sysex', data=[], time=events[0].time))

	OCTAVE_NOTES = [1,0,1,0,1,1,0,1,0,1,0,1]  # major scale 'ttsttts'
	note_map = [i for i, x in enumerate(it.islice(it.cycle(OCTAVE_NOTES), 128)) if x and 20 < i < 109]

	def to_note(addr: Addr, mode: str) -> Tuple[int, int]:
		ch = block2ch[addr.block]
		if mode == 'w':
			ch += 1
		elif mode != 'r':
			raise Exception

		return ch, note_map[addr.offset + (len(note_map) - len(addr)) // 2]

	for i, ev in enumerate(events):
		if isinstance(ev, EventCmp):
			ops = [(ev.addr1, 'r'), (ev.addr2, 'r')]
		elif isinstance(ev, EventSwap):
			ops = [(ev.addr1, 'w'), (ev.addr2, 'w')]
		elif isinstance(ev, EventMov):
			ops = [(ev.dst, 'w'), (ev.src, 'r')]
		elif isinstance(ev, EventEnd):
			break
		else:
			raise Exception

		for addr, mode in ops:
			ch, note = to_note(addr, mode)
			track.append(mido.Message('note_on', channel=ch, note=note))
		track.append(mido.Message('sysex', data=[], time=events[i+1].time - ev.time))
		for addr, mode in ops:
			ch, note = to_note(addr, mode)
			track.append(mido.Message('note_off', channel=ch, note=note))

	midi_outfile = filename.rsplit('.', maxsplit=1)[0] + '.mid'
	mid.save(midi_outfile)

	subprocess.run([
		'timidity.exe',
		'--preserve-silence',
		'-c', 'timidity_config.cfg',
		'--voice-lpf=d',
		midi_outfile,
		'-OwS',
		'-o', filename
	])

def generate_animation(env: Env, start_delay, title='', tempo=DEFAULT_TEMPO, ticks_per_beat=DEFAULT_TICKS_PER_BEAT, filename='anim.mp4', figsize=(12.80,7.20)):
	COLOR_IDLE = 'white'
	COLORS_CMP = ['limegreen'] * 2
	COLORS_SWAP = ['red'] * 2
	COLORS_MOV = ['red', 'limegreen']
	FPS = 30
	TIMEWINDOW = 2

	env = deepcopy(env)

	blocks = env.mem.blocks
	events = env.events
	[e.revert() for e in events[::-1]]

	plt.style.use('dark_background')
	fig, (arr_axs, midi_axs) = plt.subplots(2, len(blocks), sharey='row', sharex='col', squeeze=False,
	                           gridspec_kw={
		                           'width_ratios': [len(b) for b in blocks],
		                           'wspace': 0,
		                           'height_ratios': [1, 2],
		                           'hspace': 0
	                           }, figsize=figsize)
	for ax in it.chain(arr_axs, midi_axs):
		ax.tick_params(which='both',
		               bottom=False, top=False, left=False, right=False,
		               labelbottom=False, labeltop=False, labelleft=False, labelright=False)
	fig.tight_layout(rect=[0,0,1,0.95])
	bars = {block: ax.bar(range(len(block)), block, width=1, color=COLOR_IDLE, edgecolor='black')
	        for ax, block in zip(arr_axs, blocks)}

	# Generate note bars
	for ax, block in zip(midi_axs, blocks):
		ax.set_ylim(-start_delay + TIMEWINDOW, start_delay)

		xs = []
		heights = []
		bottoms = []
		colors = []

		for i, ev in enumerate(events):
			if isinstance(ev, EventEnd):
				continue

			ev2 = events[i+1]
			height = mido.tick2second(ev2.time - ev.time, ticks_per_beat, tempo)
			bottom = mido.tick2second(ev.time, ticks_per_beat, tempo)
			if isinstance(ev, EventCmp):
				addr = [ev.addr1, ev.addr2]
				color = COLORS_CMP
			elif isinstance(ev, EventSwap):
				addr = [ev.addr1, ev.addr2]
				color = COLORS_SWAP
			elif isinstance(ev, EventMov):
				addr = [ev.dst, ev.src]
				color = COLORS_MOV
			else:
				raise ValueError

			for j in range(len(addr)):
				a = addr[j]
				if a.block is block:
					xs.append(a.offset)
					heights.append(height)
					bottoms.append(bottom)
					colors.append(color[j])

		ax.bar(xs, heights, width=1, bottom=bottoms, color=colors, edgecolor='black')


	cmps = swaps = movs = total = 0
	def title_fmt():
		return f'{title}\nSize:{len(env.arr)} -- Cmps:{cmps} -- Swaps:{swaps} -- Movs:{movs} -- Total:{total}'

	end_time_s = mido.tick2second(events[-1].time, ticks_per_beat, tempo)
	total_frames = math.ceil((end_time_s + start_delay) * 30)
	frame_times = np.linspace(-start_delay, end_time_s, total_frames)
	pbar = tqdm(total=total_frames)

	prev_bars = []
	revents = events[::-1]

	def init():
		fig.suptitle(title_fmt())
		return []

	def update(t):
		nonlocal prev_bars, cmps, swaps, movs, total

		pbar.update()

		fig.suptitle(title_fmt())

		for ax in midi_axs:
			ax.set_ylim(t + TIMEWINDOW, t)

		ret = []
		if t >= mido.tick2second(revents[-1].time, ticks_per_beat, tempo):
			event = revents.pop()

			for bar in prev_bars:
				bar.set_facecolor(COLOR_IDLE)
				ret.append(bar)
			prev_bars = []

			event.apply()

			if isinstance(event, EventCmp):
				cmps += 1
				colors = COLORS_CMP
				addrs = [event.addr1, event.addr2]
			elif isinstance(event, EventSwap):
				swaps += 1
				colors = COLORS_SWAP
				addrs = [event.addr1, event.addr2]
			elif isinstance(event, EventMov):
				movs += 1
				colors = COLORS_MOV
				addrs = [event.dst, event.src]
			elif isinstance(event, EventEnd):
				return []
			else:
				raise Exception
			total += 1

			for addr, color in zip(addrs, colors):
				bar = bars[addr.block][addr.offset]
				bar.set_height(addr.get())
				bar.set_facecolor(color)
				prev_bars.append(bar)
				ret.append(bar)

		return ret

	ani = FuncAnimation(fig, update, frames=frame_times, init_func=init,
	                    interval=1000/FPS, repeat=False)
	ani.save(filename)
	pbar.close()


def animate_bars(env: Env):
	COLOR_IDLE = 'white'
	COLORS_CMP = ['limegreen'] * 2
	COLORS_SWAP = ['red'] * 2
	COLORS_MOV = ['red', 'limegreen']

	env = deepcopy(env)

	blocks = env.mem.blocks
	events = env.events
	[e.revert() for e in events[::-1]]

	plt.style.use('dark_background')
	fig, (axs,) = plt.subplots(1, len(blocks), sharey=True, squeeze=False,
	                        gridspec_kw={
		                        'width_ratios': [len(b) for b in blocks],
		                        'wspace': 0,
	                        })
	for ax in axs:
		ax.spines['top'].set_visible(False)
		ax.tick_params(which='both',
		               bottom=False, top=False, left=False, right=False,
		               labelbottom=False, labeltop=False, labelleft=False, labelright=False)
	fig.tight_layout(pad=0, rect=[0, 0, 1, 0.95])
	bars = {block: ax.bar(range(len(block)), block, width=1, color=COLOR_IDLE, edgecolor='black', linewidth=0.5)
	        for ax, block in zip(axs, blocks)}

	cmps = swaps = movs = total = 0
	def title_fmt():
		return f'Cmps:{cmps} -- Swaps:{swaps} -- Movs:{movs} -- Total:{total}'

	prev_bars = []

	def init():
		fig.suptitle(title_fmt())
		return []

	def update(event: Event):
		nonlocal prev_bars, cmps, swaps, movs, total

		fig.suptitle(title_fmt())

		ret = []

		for bar in prev_bars:
			bar.set_facecolor(COLOR_IDLE)
			ret.append(bar)
		prev_bars = []

		event.apply()

		if isinstance(event, EventCmp):
			cmps += 1
			colors = COLORS_CMP
			addrs = [event.addr1, event.addr2]
		elif isinstance(event, EventSwap):
			swaps += 1
			colors = COLORS_SWAP
			addrs = [event.addr1, event.addr2]
		elif isinstance(event, EventMov):
			movs += 1
			colors = COLORS_MOV
			addrs = [event.dst, event.src]
		elif isinstance(event, EventEnd):
			return []
		else:
			raise Exception
		total += 1

		for addr, color in zip(addrs, colors):
			bar = bars[addr.block][addr.offset]
			bar.set_height(addr.get())
			bar.set_facecolor(color)
			prev_bars.append(bar)
			ret.append(bar)

		return ret

	ani = FuncAnimation(fig, update, frames=events, init_func=init, interval=1000/10, repeat=False)
	plt.show()
