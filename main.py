# main.py
from simulation import Simulation

if __name__ == "__main__":
    total_memory_size = 128  # Example: 128 units of memory
    min_block_size = 4       # Example: Minimum block size of 4
    num_requests = 20       # Number of requests to simulate
    max_request_size = 32     # Maximum request size

    sim = Simulation(total_memory_size, min_block_size, num_requests, max_request_size)
    sim.run()