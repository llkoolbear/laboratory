



class Human():

    SENSES = ('taste', 'smell', 'sight', 'touch', 'audition')
    LIMBS = {'arms': 2, 'legs': 2}
    DIGITS = {'toes': 10, 'fingers': 10}

    def __init__(self, name, eye_color, thumb_shape):

        self.name = name
        self.eye_color = eye_color
        self.thumb_shape = thumb_shape

Matthew = Human('Matthew Bissen','hazel','chode')
Bear = Human('Bear Bissen','blue','chode')
Nick = Human('Nick Bissen','hazel','hitch-hiker')



