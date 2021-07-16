from dataclasses import dataclass
import logging
import sys
from typing import Callable, Optional, List

from .events import Event, EventEnd, EventCmp, EventSwap, EventMov
import env.memory
from .memory import Memory, Addr


logger = logging.getLogger(__name__)


@dataclass
class Stats:
	cmps: int = 0
	swaps: int = 0
	movs: int = 0
	writes: int = 0

	@property
	def total(self) -> int:
		return self.cmps + self.swaps + self.movs + self.writes

class Env:
	def __init__(self, arr: List[int], cmp: Callable[[int, int], Optional[bool]]):
		self.mem = Memory()
		self._arr = self.mem.alloc(arr).addr
		self._cmp = cmp
		self.events: List[Event] = []
		self.stats = Stats()
		self.time = 0

	def _local_trace(self, frame, event, args):
		if event == 'line':
			frame.f_trace_lines = False
			frame.f_trace_opcodes = True
		elif event == 'opcode':
			self.time += 1
		elif event == 'return':
			return
		else:
			raise Exception(frame, event, args)

		return self._local_trace

	def _global_trace(self, frame, event, args):
		if event == 'call':
			# Flag indicating if the called function is from Addr
			top_memory_call = True if frame.f_code.co_filename == env.memory.__file__ else False

			f = frame
			while f:
				code = f.f_code

				# Non top level Addr functions don't count
				if f is not frame and code.co_filename == env.memory.__file__:
					return

				if code.co_filename == __file__:
					# If stack reaches back to self.run than this is a function called by the sort
					if self.run.__func__.__code__ == code:
						break

					# Otherwise, we reached another function from Env that must have been called by the sort
					# Add constant time and don't enter its implementation
					self.time += 8
					return
				f = f.f_back

			# Add constant time for top level Addr functions. Don't enter their implementation
			if top_memory_call:
				self.time += 3
				return

			return self._local_trace
		else:
			raise Exception(frame, event, args)

	def run(self, sortf: Callable[['Env'], None], trace: bool = True) -> None:
		if trace:
			old_trace = sys.gettrace()
			sys.settrace(self._global_trace)

		sortf(self)
		self._add_event(EventEnd(self.time))

		if trace:
			sys.settrace(old_trace)

	@property
	def arr(self):
		return self._arr

	def malloc(self, size: int) -> Addr:
		return self.mem.alloc(size).addr

	def cmp(self, addr1: Addr, addr2: Addr) -> Optional[bool]:
		if addr1 == addr2:
			logger.warning('[cmp] addr1 == addr2')

		ev = EventCmp(self.time, addr1, addr2)
		self._add_event(ev)

		self.stats.cmps += 1

		return self._cmp(addr1.get(), addr2.get())

	def swap(self, addr1: Addr, addr2: Addr) -> None:
		if addr1 == addr2:
			logger.warning('[swap] addr1 == addr2', exc_info=True)

		ev = EventSwap(self.time, addr1, addr2)
		self._add_event(ev)

		self.stats.swaps += 1

		ev.apply()

	def mov(self, dst: Addr, src: Addr) -> None:
		if dst == src:
			logger.warning('[mov] addr1 == addr2', exc_info=True)

		ev = EventMov(self.time, dst, src)
		self._add_event(ev)

		self.stats.movs += 1

		ev.apply()

	def _add_event(self, event: Event) -> None:
		if len(self.events) > 0 and self.events[-1] == event:
			logger.warning(f'Duplicate event {event}')

		self.events.append(event)
