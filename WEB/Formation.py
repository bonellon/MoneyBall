class Formation:
    gameweek = 0
    svm = {}
    rf = {}
    gbm = {}

    def __init__(self, gw, svm, rf, gbm):
        self.gameweek = gw
        self.svm = svm
        self.rf = rf
        self.gbm = gbm


class Model:
    name = ""
    goalkeepers = []
    defenders = []
    midfielders = []
    forwards = []

    def __init__(self, name, goalkeepers, defenders, midfielders, forwards):
        self.name = name
        self.goalkeepers = goalkeepers
        self.defenders = defenders
        self.midfielders = midfielders
        self.forwards = forwards


class Player:
    name = ""
    points = 0

    def __init__(self, name, points):
        self.name = name
        self.points = points