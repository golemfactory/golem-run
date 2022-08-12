import argparse
from multiprocessing.pool import ThreadPool

parser = argparse.ArgumentParser()
parser.add_argument("range_start", type=int, help="Specify search range start (inclusive)")
parser.add_argument("range_end", type=int, help="Specify search range end, (non-inclusive")
args = parser.parse_args()

# Collatz Conjecture algorithm - https://pl.wikipedia.org/wiki/Problem_Collatza#Zwi%C4%85zek_z_problemem_stopu
#   procedure collatz(x);
#   begin
#     do
#       if x mod 2 = 0 then
#         x := x / 2
#       else
#         x := 3 * x + 1
#     while x <> 1
#   end


def collatz(initial):
    x = initial
    top_value = initial
    iters = 0
    while x != 1:
        x = int(x / 2) if x % 2 == 0 else int(3 * x + 1)
        iters += 1
        if x > top_value:
            top_value = x
    print(f"[{initial}]: Found; max={top_value},iters={iters}")


pool = ThreadPool()
pool.map(collatz, range(args.range_start, args.range_end))