import numpy as np
from numpy.random import Generator, PCG64
def generate_timestamp(size: int = 5, start_ms: int = 0, max_deviation: int = 1000) -> np.ndarray:
    from python.index import USE_DTYPE

    array = np.empty(size, dtype=USE_DTYPE)
    generator = Generator(PCG64())
    for i in range(size):
        start_ms += generator.integers(low=1, high=max_deviation)
        array[i] = start_ms

    return array