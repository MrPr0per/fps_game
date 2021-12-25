from geometric_classes import Column


class Enemy(Column):
    def __init__(self, x, y, h, h_down):
        super().__init__(x=x, y=y, h=h, h_down=h_down)
