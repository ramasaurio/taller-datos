
class Player(object):

    def __init__(self, name=None, fullname=None, country=None, bday=None):

        # Para manejar nombre con comas
        if ',' in name:
            auxname = name.split(',')
            if len(auxname) == 2:
                name = auxname[1][1:] + ' ' + auxname[0]

        # Para manejar los casos en que no esté el nombre o el nombre completo
        if fullname == '-':
            fullname = name
        if name == '-':
            name = fullname

        self.name = name
        self.fullname = fullname
        self.country = country

        if len(bday) == 10:
            self.byear = bday[0:4]
            self.bmonth = bday[5:7]
            self.bday = bday[8:10]
        elif len(bday) == 7:
            self.byear = None
            self.bmonth = bday[2:4]
            self.bday = bday[5:7]
        elif len(bday) == 4:
            self.byear = bday
            self.bmonth = None
            self.bday = None


class FifaPlayer(object):

    def __init__(self, idapi=None, name=None, idapififa=None, bday=None):
        self.idapi = idapi
        self.idapififa = idapififa
        self.name = name.replace('"', '')
        if len(bday) != 21:
            print(bday)
