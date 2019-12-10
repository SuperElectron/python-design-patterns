"""
recommended solution to using the prototype pattern
source: https://python-patterns.guide/gang-of-four/iterator/#implementing-an-iterable-and-iterator

*What is this pattern about?
Traverses a container and accesses the container's elements.

*Implementing an iterable and interator

How can a class implement the Iterator Pattern and plug in to Python’s native iteration mechanisms for, iter(), and next()?
1. make iterable: The container must offer an __iter__() method that returns an iterator object.
2. Each iterator must offer a __next__() method that returns the next item from the container each time it is called.
- It should raise StopIterator when there are no further items.
3.each iterator must have __iter__() that returns itself.
- some users pass iterators to a for loop instead of passing the underlying container.
"""


class OddNumbers(object):
    "An iterable object."

    def __init__(self, maximum):
        self.maximum = maximum

    def __iter__(self):
        """ 1. make iterable"""
        return OddIterator(self)


class EvenNumbers(object):
    "An iterable object."

    def __init__(self, maximum):
        self.maximum = maximum

    def __iter__(self):
        """ 1. make iterable"""
        return EvenIterator(self)


class OddIterator(object):
    "An iterator."

    def __init__(self, container):
        self.container = container
        self.n = -1

    def __next__(self):
        """ 2. use __next__() to return next item in container"""
        self.n += 2
        if self.n > self.container.maximum:
            raise StopIteration
        return self.n

    def __iter__(self):
        """ 3. __iter__() that returns itself """
        return self


class EvenIterator(object):
    "An iterator."

    def __init__(self, container):
        self.container = container
        self.n = 0

    def __next__(self):
        """ 2. use __next__() to return next item in container"""
        self.n += 2
        if self.n > self.container.maximum:
            raise StopIteration
        return self.n

    def __iter__(self):
        """ 3. __iter__() that returns itself """
        return self


def main():
    spacer = "=" * 20
    print(spacer)

    print("Odd iterator in action")
    numbers = OddNumbers(7)
    for n in numbers:
        print(n)
    print(spacer)

    print("Even iterator in action")
    numbers = EvenNumbers(8)
    for n in numbers:
        print(n)
    print(spacer)


if __name__ == "__main__":
    main()
