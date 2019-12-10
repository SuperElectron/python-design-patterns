"""
Pattern name - SingleTon
Pattern type - Creational Design Pattern
"""


# Solution - 4
class SingletonMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        print(cls.__instances)
        return cls.__instances[cls]


class DBConnector(metaclass=SingletonMeta):
    def __init__(self):
        self.status = "Not Connected"

    def disconnect(self):
        self.status = "Disconnected"

    def connect(self):
        self.status = "Connected"


if __name__ == "__main__":
    spacer = "=" * 20
    print(spacer)

    client1 = DBConnector()
    print("Client 1 ", client1)
    print(client1.status)
    print(spacer)

    client2 = DBConnector()
    print("Client 2 ", client2)
    print(spacer)
