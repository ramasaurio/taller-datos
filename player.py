class FullPlayer():

    def __init__(self, idapi, name, country, age, league, season):
        self.idapi = idapi
        self.name = name
        self.country = country
        self.age = age
        self.league = league
        self.season = season


class Player(object):

    def __init__(self, name=None, fullname=None, country=None, bday=None):

        # Para manejar nombre con comas
        if ',' in name:
            name = name.lower()
            auxname = name.split(',')
            if len(auxname) == 2:
                name = auxname[1][1:] + ' ' + auxname[0]

        # Para manejar los casos en que no esté el nombre o el nombre completo
        if fullname == '-':
            fullname = name
        if name == '-':
            name = fullname

        self.name = cleanWeirdLetters(name)
        self.fullname = cleanWeirdLetters(fullname)
        self.country = country

        if len(bday) == 10:
            self.byear = int(bday[0:4])
            self.bmonth = int(bday[5:7])
            self.bday = int(bday[8:10])
        elif len(bday) == 7:
            self.byear = None
            self.bmonth = int(bday[2:4])
            self.bday = int(bday[5:7])
        elif len(bday) == 4:
            self.byear = int(bday)
            self.bmonth = None
            self.bday = None


class FifaPlayer(object):

    def __init__(self, idapi=None, name=None, idapififa=None, bday=None, country=None, premier=None,
                 bundes=None, seriea=None, spain=None, age=None):
        self.idapi = int(idapi)
        self.name = name.replace('"', '').lower()

        if idapififa is not None and bday is not None:
            self.idapififa = int(idapififa)
            self.byear = int(bday[0:4])
            self.bmonth = int(bday[5:7])
            self.bday = int(bday[8:10])

        if age is None:
            years = 2016 - self.byear - 1
            months = 9 - self.bmonth
            days = 29 - self.bday

            if months > 0:
                years += 1
            elif months == 0:
                if days > 0:
                    years += 1

            self.age = years
        else:
            self.age = int(age)

        if country is not None:
            self.country = country
            self.premier = premier
            self.bundes = bundes
            self.seriea = seriea
            self.spain = spain


def cleanWeirdLetters(name):

    name = name.lower()
    name.replace(', jr', ' jr')
    name = name.replace('á', 'a').replace('ā', 'a').replace('å', 'a').replace('ä', 'a').replace('â', 'a')
    name = name.replace('à', 'a').replace('ã', 'a').replace('ă', 'a').replace('ą', 'a')
    name = name.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ę', 'e')
    name = name.replace('ě', 'e').replace('ё', 'e').replace('ë', 'e').replace('ė', 'e')
    name = name.replace('í', 'i').replace('ì', 'i').replace('ï', 'i').replace('î', 'i').replace('õ', 'o')
    name = name.replace('ó', 'o').replace('ò', 'o').replace('ö', 'o').replace('ô', 'o').replace('ő', 'o')
    name = name.replace('ú', 'u').replace('ù', 'u').replace('ü', 'u').replace('û', 'u').replace('ū', 'u')
    name = name.replace('č', 'c').replace('ć', 'c').replace('ç', 'c')
    name = name.replace('š', 's').replace('ş', 's').replace('ś', 's').replace('ș', 's')
    name = name.replace('ž', 'z').replace('ż', 'z').replace('ź', 'z')
    name = name.replace('ń', 'n').replace('ņ', 'n').replace('ň', 'n')
    name = name.replace('ý', 'y')
    name = name.replace('ğ', 'g')
    name = name.replace('ř', 'r').replace('/', '')
    name = name.replace("'", "").replace('’', '').replace(',', '').replace('–', '-')
    return name
