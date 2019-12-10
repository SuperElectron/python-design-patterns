"""
* Composite Pattern
source: https://python-patterns.guide/gang-of-four/composite/
"""


class Widget(object):

    def __init__(self, name):
        self.name = name

    def children(self):
        return []


class Frame(Widget):
    def __init__(self, child_widgets):
        self.child_widgets = child_widgets

    def children(self):
        return self.child_widgets


class Label(Widget):
    def __init__(self, text):
        self.text = text


def main():
    spacer = "=" * 20
    print(spacer)

    watch = Widget(name="watch")
    frame = Frame(watch)

    print(watch.name)
    print(spacer)
    print(frame.children())


if __name__ == "__main__":
    main()
