import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
project_src = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_src)

import timeit
import asyncio

from fetch.fetch_coroutine import main as fetch_coroutine_main
from fetch.fetch_parallel import main as fetch_parallel_main

async def run_fetch_coroutine_main():
    await fetch_coroutine_main()

result_coroutine = timeit.timeit('asyncio.run(run_fetch_coroutine_main())', globals=globals(), number=1)
print(f'Coroutine took {result_coroutine:.3f} seconds')

result_threads = timeit.timeit('fetch_parallel_main()', globals=globals(), number=1)
print(f'Threads took {result_threads:.3f} seconds')

sys.argv.append('-p')
result_parrallel = timeit.timeit('fetch_parallel_main()', globals=globals(), number=1)
print(f'Parallel took {result_parrallel:.3f} seconds')