from abc import ABC
from dataclasses import dataclass, field

from .memory import Addr


@dataclass
class Event(ABC):
	time: int = field(compare=False)

	def apply(self):
		pass

	def revert(self):
		pass

class EventEnd(Event):
	pass

@dataclass
class EventCmp(Event):
	addr1: Addr
	addr2: Addr

@dataclass
class EventSwap(Event):
	addr1: Addr
	addr2: Addr

	def apply(self):
		self._swap()

	def revert(self):
		self._swap()

	def _swap(self):
		tmp = self.addr1.get()
		self.addr1.set(self.addr2.get())
		self.addr2.set(tmp)

@dataclass
class EventMov(Event):
	dst: Addr
	src: Addr
	val1: int = field(init=False)

	def __post_init__(self):
		self.val1 = self.dst.get()

	def apply(self):
		self.dst.set(self.src.get())

	def revert(self):
		self.dst.set(self.val1)
