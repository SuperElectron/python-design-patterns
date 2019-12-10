"""
Pattern name - SingleTon
Pattern type - Creational Design Pattern
"""


# Solution - 1
class SingleTon(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


def main():
    spacer = "=" * 20
    print(spacer)

    o1 = SingleTon()
    print("Object - 1 ==>", o1)
    o1.data = 10
    print(spacer)

    o2 = SingleTon()
    print("Object - 2 ==>", o2)
    print("Object - 2 data ==>", o2.data)
    o2.data = 5
    print("Object - 1 data ==>", o1.data)
    print(spacer)


if __name__ == "__main__":
    main()
