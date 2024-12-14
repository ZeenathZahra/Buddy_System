# memory_block.py

class MemoryBlock:
    """
    Represents a block of memory in the Buddy system.

    Attributes:
        start_address (int): The starting address of the block.
        size (int): The size of the block.
        is_free (bool): True if the block is free, False if allocated.
        order (int): The order of the block (size = 2^order).
    """

    def __init__(self, start_address, size, order):
        self.start_address = start_address
        self.size = size
        self.is_free = True
        self.order = order

    def __str__(self):
        return f"Block(start={self.start_address}, size={self.size}, order={self.order}, free={self.is_free})"