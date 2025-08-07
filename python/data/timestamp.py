import numpy as np
from numpy.random import Generator, PCG64
def generate_timestamp(size: int = 5, seed: int = None, start_ms: int = 0, max_deviation: int = 1000, interval: int = 3, dtype: np.dtype = np.float64) -> np.ndarray:

    array = np.empty(size, dtype=dtype)
    generator = Generator(PCG64(seed=seed))
    sum = start_ms
    for i in range(size):
        sum += generator.integers(low=1, high=max_deviation)
        array[i] = sum
        if (i+1) % interval == 0:
            sum = start_ms
    return array