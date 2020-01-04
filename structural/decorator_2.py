# #1 goodClock() uses the functools.wraps decorator to copy the relevant attributes from func to clocked
# #2 @clock() has a parametized registration decorator
import time
import functools


def okClock(func):
    """ this CANNOT accept keyword arguments  """
    """ this DOES mask __doc__ and __name__ of decorated function  """
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked


def goodClock(func):
    """ this CAN accept keyword arguments  """
    """ this DOES NOT mask __doc__ and __name__ of decorated function  """
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))

        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked


@okClock
def fake():
    return 10


@okClock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@goodClock
def goodFactorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@goodClock
def goodFake():
    return 10


# @clock() is a parametized registration decorator
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate


@clock()
def snooze1(seconds):
    """ IS NOT making use of parameterization """
    time.sleep(seconds)


@clock('{name}: {elapsed}s')
def snooze2(seconds):
    """ IS making use of parameterization """
    time.sleep(seconds)


if __name__ == '__main__':
    print('*' * 10)
    print('okClock usage: basic setup')
    fake()
    print('*' * 10)
    factorial(6)
    print('*' * 10)
    print('goodClock usage: @functools.wraps(func) used around inner function')
    print('*' * 10)
    goodFake()
    print('*' * 10)
    goodFactorial(6)
    print('*' * 10)
    print('clock usage: no parameterization')
    print('*' * 10)
    for i in range(3):
        snooze1(.123)
    print('*' * 10)
    print('clock usage: with parameterization')
    for i in range(3):
        snooze2(.123)
