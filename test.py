class Aboba:
    def __init__(self):
        pass


a = Aboba()
a = str(type(a))
print(a)
a = a[a.rfind('.')+1:a.rfind('\'')]
print(a)
print(f'\t{a}(x=0, y=13, angle=270)')
