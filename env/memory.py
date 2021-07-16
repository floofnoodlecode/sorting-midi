from typing import List, overload

class Memory:
	def __init__(self):
		self.blocks: List['Block'] = []

	@overload
	def alloc(self, size: int) -> 'Block':
		pass
	@overload
	def alloc(self, arr: List[int]) -> 'Block':
		pass
	def alloc(self, init) -> 'Block':
		if isinstance(init, int):
			block = Block(init, len(self.blocks))
		elif isinstance(init, list):
			block = Block(len(init), len(self.blocks))
			block[:] = init
		else:
			raise ValueError

		self.blocks.append(block)
		return block

class Block(list):
	def __init__(self, size: int, block_idx: int):
		super().__init__([0 for _ in range(size)])
		self.block_idx = block_idx

	@property
	def addr(self) -> 'Addr':
		return Addr(self, 0)

	def __hash__(self):
		return hash(id(self))

	def __eq__(self, other):
		return id(self) == id(other)

class Addr:
	def __init__(self, block: Block, offset: int):
		self.block = block
		self.offset = offset

	def get(self) -> int:
		assert 0 <= self.offset < len(self.block)
		return self.block[self.offset]

	def set(self, val: int):
		assert 0 <= self.offset < len(self.block)
		self.block[self.offset] = val

	def __add__(self, other: int) -> 'Addr':
		assert isinstance(other, int)
		return Addr(self.block, self.offset + other)

	@overload
	def __sub__(self, other: int) -> 'Addr':
		pass
	@overload
	def __sub__(self, other: 'Addr') -> int:
		pass
	def __sub__(self, other):
		if isinstance(other, int):
			return Addr(self.block, self.offset - other)
		elif isinstance(other, Addr):
			assert self.block == other.block
			return self.offset - other.offset
		else:
			raise ValueError

	def __len__(self):
		return len(self.block)

	def __eq__(self, other):
		return (self.block, self.offset) == (other.block, other.offset)

	def __repr__(self):
		return f'*({self.block.block_idx}+{self.offset})'