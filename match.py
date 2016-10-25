class Match:

    def __init__(self, values, matches):

        self.matches = matches
        self.values = values

    @property
    def idM(self):
        return self[self.matches.idM]

    @property
    def league(self):
        return self[self.matches.league]

    def __getitem__(self, item):
        return self.values[self.matches.positions[item]]


class Matches:

    def __len__(self, path, idM=None, league=None, columns=None):

        self.idM = idM
        self.matches = []
        self.columns = []

        if idM is not None:
            self.columns.append((idM, int))
        if league is not None:
            self.columns.append((league, str))
        if columns is not None:
            self.columns.extend(columns)

        self.positions = dict([(self.columns[i][0], i) for i in range(len(self.columns))])

        infile = open(path, 'r')
        headers = infile.readline().replace('\n', '').replace('\r', '').split(',')
        for line in infile:
            line = line.replace('\n', '').replace('\r', '').split(',')
            values = [_type(line[headers.index(column)]) for column, _type in self.columns]
            self.matches.append(Match(values, self))
        infile.close()
