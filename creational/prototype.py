"""
recommended solution to using the prototype pattern
source: https://python-patterns.guide/gang-of-four/prototype/

*What is this pattern about?
This patterns aims to reduce the number of classes required by an
application. Instead of relying on subclasses it creates objects by
copying a prototypical instance at run-time.

Avoiding a factory.
- classes and functions in Python are first-class, thus can be passed as arguments like any other objects.
- first-class objects are stored in data structures can be passed as objects!
- we want to solve our problem without having to mirror each class with a factory.

- we can use the original objects to store the arguments
- this gives those objects the ability to provide new instances.

The result is the Prototype pattern!
- All of the factory classes disappear.
"""

# The Prototype pattern: teach each object
# instance how to build copies of itself.


class Note(object):
    "Musical note 1 ÷ `fraction` measures long."
    def __init__(self, fraction):
        self.fraction = fraction

    def clone(self):
        return Note(self.fraction)


class Sharp(object):
    "The symbol ♯."
    def clone(self):
        return Sharp()


class Flat(object):
    "The symbol ♭."
    def clone(self):
        return Flat()


def main():
    spacer = "=" * 20
    print(spacer)
    sharp = Note(fraction=2)
    print(sharp, sharp.fraction)
    print(spacer)

    sharp2 = sharp.clone()
    print(sharp2, sharp2.fraction)
    print(spacer)

    flat = Note(fraction=3)
    flat2 = flat.clone()
    print(flat, flat.fraction)
    print(spacer)
    print(flat2, flat.fraction)
    print(spacer)


if __name__ == '__main__':
    main()
