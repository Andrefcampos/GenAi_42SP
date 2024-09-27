import time
import sys

def ft_progress(valor):
    start_time = time.time()

    for index in valor:
        elapsed_time = time.time() - start_time
        eta = (elapsed_time / (index + 1)) * (len(valor) - (index + 1))
        bar_progress = (index + 1) / len(valor)

        filled_length = int(bar_progress * 20)
        bar = '=' * filled_length + '>' + ' ' * (20 - filled_length)
        sys.stdout.write(
            f"\rETA: {eta:.2f}s [{int(bar_progress * 100)}%][{bar}] "
            f"{(index + 1)}/{len(valor)} | elapsed time {elapsed_time:.2f}s"
        )
        sys.stdout.flush()
        yield index
    print()

# if __name__ == "__main__":
a_list = range(1000)
ret = 0
for elem in ft_progress(a_list):
    ret += (elem + 3) % 5
    time.sleep(0.01)
print()
print(ret)
