# test_buddy_allocator.py

import unittest
from buddy_allocator import BuddyAllocator
from utils import is_power_of_two


class TestBuddyAllocator(unittest.TestCase):

    def test_basic_allocation(self):
      """Test basic allocation and deallocation."""
      print("\nStarting test_basic_allocation")
      allocator = BuddyAllocator(total_memory_size=128, min_block_size=4)

      # Test 1: Allocate a small block
      print("  Test 1: Allocating block of size 8")
      addr1 = allocator.allocate(8)
      self.assertNotEqual(addr1, -1, "Failed to allocate block of size 8")
      self.assertTrue(0 <= addr1 < 128, "Address out of range")
      print(f"    Allocated block of size 8 at address {addr1}")
      allocator.deallocate(addr1)
      print(f"    Deallocated block at address {addr1}")
      
      # Test 2: Allocate a large block
      print("  Test 2: Allocating block of size 64")
      addr2 = allocator.allocate(64)
      self.assertNotEqual(addr2, -1, "Failed to allocate block of size 64")
      self.assertTrue(0 <= addr2 < 128, "Address out of range")
      print(f"    Allocated block of size 64 at address {addr2}")
      allocator.deallocate(addr2)
      print(f"    Deallocated block at address {addr2}")

      # Test 3: Allocate and deallocate multiple blocks
      print("  Test 3: Allocating and deallocating multiple blocks")
      addr3 = allocator.allocate(16)
      addr4 = allocator.allocate(32)
      self.assertNotEqual(addr3, -1, "Failed to allocate block of size 16")
      self.assertNotEqual(addr4, -1, "Failed to allocate block of size 32")
      print(f"    Allocated block of size 16 at address {addr3}")
      print(f"    Allocated block of size 32 at address {addr4}")
      allocator.deallocate(addr3)
      print(f"    Deallocated block at address {addr3}")
      addr5 = allocator.allocate(8)
      self.assertNotEqual(addr5, -1, "Failed to allocate block of size 8 after deallocation")
      print(f"    Allocated block of size 8 at address {addr5}")
      allocator.deallocate(addr4)
      print(f"    Deallocated block at address {addr4}")
      allocator.deallocate(addr5)
      print(f"    Deallocated block at address {addr5}")
      print("  Basic allocation and deallocation tests passed.")
    
    def test_boundary_conditions(self):
        """Test boundary conditions and edge cases."""
        print("\nStarting test_boundary_conditions")
        allocator = BuddyAllocator(total_memory_size=128, min_block_size=4)

        # Test 1: Allocate min block size
        print("  Test 1: Allocating block of min size (4)")
        addr1 = allocator.allocate(4)
        self.assertNotEqual(addr1, -1, "Failed to allocate block of min size")
        print(f"    Allocated block of size 4 at address {addr1}")
        allocator.deallocate(addr1)
        print(f"    Deallocated block at address {addr1}")

        # Test 2: Allocate max block size
        print("  Test 2: Allocating block of max size (128)")
        addr2 = allocator.allocate(128)
        self.assertNotEqual(addr2, -1, "Failed to allocate block of max size")
        print(f"    Allocated block of size 128 at address {addr2}")
        allocator.deallocate(addr2)
        print(f"    Deallocated block at address {addr2}")

        # Test 3: Allocate slightly less than a power of 2
        print("  Test 3: Allocating block slightly less than a power of 2 (size 7)")
        addr3 = allocator.allocate(7)
        self.assertNotEqual(addr3, -1, "Failed to allocate block of size 7")
        block = allocator.allocated_blocks[addr3]
        self.assertEqual(block.size, 8, "Allocated block size is incorrect")
        print(f"    Allocated block of size 7 (actual size 8) at address {addr3}")
        allocator.deallocate(addr3)
        print(f"    Deallocated block at address {addr3}")

        # Test 4: Attempt to allocate more than total memory
        print("  Test 4: Attempting to allocate more than total memory (size 200)")
        addr4 = allocator.allocate(200)
        self.assertEqual(addr4, -1, "Should not be able to allocate more than total memory")
        print("    Failed to allocate block of size 200, as expected.")

        print("  Boundary conditions tests passed.")

    def test_error_handling(self):
        """Test error handling conditions."""
        print("\nStarting test_error_handling")

        # Test 1: Invalid total memory size (not power of 2)
        print("  Test 1: Invalid total memory size (130)")
        with self.assertRaises(ValueError) as context:
           BuddyAllocator(total_memory_size=130, min_block_size=4)
        self.assertIn("must be powers of 2", str(context.exception))
        print("    ValueError raised for invalid total memory size, as expected.")

        # Test 2: Invalid min block size (not power of 2)
        print("  Test 2: Invalid min block size (3)")
        with self.assertRaises(ValueError) as context:
          BuddyAllocator(total_memory_size=128, min_block_size=3)
        self.assertIn("must be powers of 2", str(context.exception))
        print("    ValueError raised for invalid min block size, as expected.")

        # Test 3: Min block size > total memory
        print("  Test 3: Min block size greater than total memory size")
        with self.assertRaises(ValueError) as context:
           BuddyAllocator(total_memory_size=64, min_block_size=128)
        self.assertIn("cannot be greater than total memory size", str(context.exception))
        print("    ValueError raised for min block size > total memory, as expected.")

        # Test 4: Deallocate invalid address
        print("  Test 4: Deallocating an invalid address")
        allocator = BuddyAllocator(total_memory_size=128, min_block_size=4)
        allocator.deallocate(200)  # 200 is not a valid allocated address
        print("    Attempt to deallocate invalid address (200), no action should be taken, as expected.")

        print("  Error handling tests passed.")

    def test_invalid_input(self):
      with self.assertRaises(ValueError):
         BuddyAllocator(127, 4)
      with self.assertRaises(ValueError):
        BuddyAllocator(128, 3)
      with self.assertRaises(ValueError):
        BuddyAllocator(128, 256)
      
if __name__ == '__main__':
    unittest.main()