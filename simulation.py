# simulation.py
import random
from buddy_allocator import BuddyAllocator

class Simulation:
    """
    Simulates memory allocation and deallocation requests.

    Attributes:
        allocator (BuddyAllocator): The Buddy allocator instance.
        num_requests (int): Number of requests to simulate.
        max_request_size (int): Maximum size of memory request.
        allocated_addresses (dict): Keep track of allocated block start addresses and their sizes.
    """

    def __init__(self, total_memory_size, min_block_size, num_requests, max_request_size):
        self.allocator = BuddyAllocator(total_memory_size, min_block_size)
        self.num_requests = num_requests
        self.max_request_size = max_request_size
        self.allocated_addresses = {}  # To store {address: size}

    def run(self):
        """Runs the simulation."""
        print("Initial Allocator State:")
        print(self.allocator)

        for _ in range(self.num_requests):
            request_type = random.choice(["allocate", "deallocate"])
            if request_type == "allocate" or not self.allocated_addresses:  # Force allocate if no blocks are allocated
                size = random.randint(1, self.max_request_size)
                address = self.allocator.allocate(size)
                if address != -1:
                    self.allocated_addresses[address] = size
                    print(f"Allocated: Address={address}, Size={size}")
                else:
                    print(f"Allocation Failed: Size={size}")
            else:
                address_to_deallocate = random.choice(list(self.allocated_addresses.keys()))
                size = self.allocated_addresses.pop(address_to_deallocate)
                self.allocator.deallocate(address_to_deallocate)
                print(f"Deallocated: Address={address_to_deallocate}, Size={size}")

            print("\nAllocator State After Request:")
            print(self.allocator)
        
        print("\nFinal Allocator State:")
        print(self.allocator)