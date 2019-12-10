"""
Pattern name - Singleton
Pattern type - Creational Design Patterns
"""


class Singleton(object):
    """ Singleton class"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


def main():
    spacer = "=" * 20
    print(spacer)

    obj1 = Singleton()
    print("Object 1: ", obj1)
    obj1.data = 10
    obj2 = Singleton()
    print("Object 2: ", obj2)
    print(spacer)

    print("Object 2 data: ", obj2.data)
    obj2.data = 5
    print("Object 1 data: ", obj1.data)
    print(spacer)


if __name__ == "__main__":
    main()
