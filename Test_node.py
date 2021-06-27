mot_vide = "ε"


class node:
    def __init__(self, n) -> None:
        self.info = n
        self.suivant = None
        self.parent = None

    def __str__(self) -> str:
        return f'{self.info} ----> '

    def add(self, x):
        a = self
        q = a
        while a.suivant != None:
            a = a.suivant
        a.suivant = node(x)
        a.suivant.parent = a

    def print(self):
        a = self
        while a != None:
            print(a)
            a = a.suivant

    def test(self):
        a = node(1)
        for i in range(3, 7):
            print(i)
            a.add(i)
        a.print()


if __name__ == '__main__':
    # from sys import getsizeof
    # a = node(1)
    # print(getsizeof(a))
    # for i in range(3,7):
    #     a.add(i)
    # print(getsizeof(a))
    # a.print()
    class Noeud():
        def __init__(self, t1=None, t2=None) -> None:
            self.trnasition1 = t1
            self.trnasition2 = t2
