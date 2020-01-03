# Fluent Python by Luciano Ramalho
# When python executes decorators
# Import time versus run time

registry = []


def register(func):
    print('import time: running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('runtime: running main()')
    print('registry.append(func) was imported twice: registry ->', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()
