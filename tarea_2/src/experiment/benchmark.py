import time
import concurrent
import tracemalloc
import multiprocessing

from typing import Any
from collections.abc import Callable

if multiprocessing.get_start_method(allow_none=True) != "fork":
    multiprocessing.set_start_method("fork", force=True)


def benchmark(kernel: Callable, input: Any, timeout: int) -> dict:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.submit(kernel, input)
        output = {}
        try:
            tracemalloc.start()
            start_time = time.perf_counter()
            result = future.result(timeout=timeout)
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            elapsed_time = end_time - start_time
            output = {
                "result": result,
                "time": elapsed_time,
                "peak_memory": peak
            }
        except concurrent.futures.TimeoutError as e:
            future.cancel()
        except Exception as e:
            print(f"Unexpected exception: {e}")
        finally:
            executor.shutdown(wait=False)
            tracemalloc.stop()

        return output


def run_benchmarks(kernels: list[Callable], inputs: list[Any], timeout: int, num_samples: int = 1) -> list[dict]:
    benchmark_results = []

    for i in range(len(inputs)):
        for sample in range(num_samples):
            for kernel in kernels:
                results = benchmark(kernel, inputs[i], timeout)
                benchmark_results.append({
                    "kernel": kernel.__name__,
                    "input": i,
                    **results
                })

    return benchmark_results
