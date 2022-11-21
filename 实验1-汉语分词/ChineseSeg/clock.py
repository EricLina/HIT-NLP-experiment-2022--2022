import time
import functools
def clock(func):

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        timecost = time.time() - start_time
        print(func.__name__ + " time_cost -> {}".format(timecost))
        return result
    
    return clocked

@clock  # --> 6
def fib(n):
    """this is fibonacci function"""
    return n if n < 2 else fib(n - 1) + fib(n - 2)

if __name__ == "__main__":
    fib(1)
    print(fib.__name__)  # 输出 clocked
    print(fib.__doc__)  # 输出 this is inner clocked function