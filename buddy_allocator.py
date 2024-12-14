# buddy_allocator.py
from memory_block import MemoryBlock
from utils import next_power_of_two, calculate_order, is_power_of_two

class BuddyAllocator:
    """
    Implements the Buddy memory allocation algorithm.

    Attributes:
        total_memory_size (int): Total size of memory managed by the allocator.
        min_block_size (int): Minimum size of allocatable blocks.
        free_lists (dict): Dictionary of free lists, indexed by order.
        allocated_blocks (dict): Dictionary of allocated blocks, indexed by start address.
    """

    def __init__(self, total_memory_size, min_block_size=1):
        if not is_power_of_two(total_memory_size) or not is_power_of_two(min_block_size):
            raise ValueError("Total memory size and minimum block size must be powers of 2")
        if min_block_size > total_memory_size:
            raise ValueError("Minimum block size cannot be greater than total memory size")

        self.total_memory_size = next_power_of_two(total_memory_size)
        self.min_block_size = min_block_size
        self.max_order = calculate_order(self.total_memory_size)
        self.min_order = calculate_order(self.min_block_size)
        self.free_lists = {i: [] for i in range(self.min_order, self.max_order + 1)}
        self.allocated_blocks = {}

        # Initialize with one large free block
        initial_block = MemoryBlock(0, self.total_memory_size, self.max_order)
        self.free_lists[self.max_order].append(initial_block)

    def allocate(self, size):
        """
        Allocates a block of memory of the given size.

        Args:
            size (int): The requested size of the memory block.

        Returns:
            int: The starting address of the allocated block, or -1 if allocation fails.
        """
        requested_size = next_power_of_two(size)
        if requested_size > self.total_memory_size:
            return -1  # Request too large
        
        order = calculate_order(requested_size)
        if order < self.min_order:
            order = self.min_order

        # Find a suitable free block
        for i in range(order, self.max_order + 1):
            if self.free_lists[i]:
                block = self.free_lists[i].pop(0)
                # Split block if necessary
                while i > order:
                    new_size = 2**(i - 1)
                    buddy1 = MemoryBlock(block.start_address, new_size, i -1 )
                    buddy2 = MemoryBlock(block.start_address + new_size, new_size, i -1 )
                    self.free_lists[i - 1].append(buddy2)
                    block = buddy1
                    i -=1

                block.is_free = False
                self.allocated_blocks[block.start_address] = block
                return block.start_address

        return -1  # No suitable block found

    def deallocate(self, start_address):
        """
        Deallocates a block of memory.

        Args:
            start_address (int): The starting address of the block to deallocate.
        """
        if start_address not in self.allocated_blocks:
            return  # Invalid address

        block = self.allocated_blocks.pop(start_address)
        block.is_free = True
        order = block.order

        # Coalesce with buddies
        while order < self.max_order:
            buddy_address = block.start_address ^ (2 ** order)
            buddy = self._find_free_buddy(buddy_address, order)

            if buddy:
                # Remove buddy from free list
                self.free_lists[order].remove(buddy)
                # Determine the start address of the merged block
                start_address = min(block.start_address, buddy.start_address)
                # Create the merged block with larger order
                block = MemoryBlock(start_address, 2**(order + 1), order + 1)
                block.is_free = True
                order += 1
            else:
                break
        self.free_lists[order].append(block)

    def _find_free_buddy(self, address, order):
        """Helper function to find a free buddy block."""
        for block in self.free_lists[order]:
            if block.start_address == address:
                return block
        return None

    def __str__(self):
        """String representation of the Buddy Allocator for debugging."""
        s = "Buddy Allocator State:\n"
        s += f"  Total Memory: {self.total_memory_size}\n"
        s += f"  Min Block Size: {self.min_block_size}\n"
        s += "  Free Lists:\n"
        for order in sorted(self.free_lists.keys()):
            s += f"    Order {order}: "
            if self.free_lists[order]:
              s += ", ".join(str(block) for block in self.free_lists[order])
            else:
                s+= "Empty"
            s += "\n"

        s += "  Allocated Blocks:\n"

        if self.allocated_blocks:
            for start_address, block in self.allocated_blocks.items():
                s += f"    {block}\n"
        else:
            s += "    No allocated Blocks\n"

        return s