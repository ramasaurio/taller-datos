

class Player(object):

    def __init__(self, name=None, fullname=None, country=None, bday=None):
        self.name = name
        self.fullname = fullname
        self.country = country
        if len(bday) != 10:
            print(bday)

        # if bday[0] == '-':
        #     self.byear = None
        #     bday = bday[2:]
        # else:
        #     self.byear = bday[0:4]
        #     bday = bday[]





