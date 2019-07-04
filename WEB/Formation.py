class Formation:
    gameweek = 0
    goalkeepers = []
    defenders = []
    midfielders = []
    forwards = []

    def __init__(self, gw, gk, df, md, fw):
        self.gameweek = gw
        self.goalkeepers = gk
        self.defenders = df
        self.midfielders = md
        self.forwards = fw


class Player:
    name = ""
    points = 0

    def __init__(self, name, points):
        self.name = name
        self.points = points