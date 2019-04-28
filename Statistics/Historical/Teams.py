from enum import Enum

class Teams(Enum):
    Arsenal = 1
    Bournemouth = 2
    Brighton = 3
    Burnley = 4
    Cardiff = 5
    Chelsea = 6
    Crystal_Palace = 7
    Everton = 8
    Fulham = 9
    Huddersfield = 10
    Leicester_City = 11
    Liverpool = 12
    Manchester_City = 13
    Manchester_United = 14
    Newcastle = 15
    Southampton = 16
    Spurs = 17
    Watford = 18
    West_Ham = 19
    Wolves = 20

def FDR_Arsenal(isHome):
    if(isHome):
        return 4
    return 4

def FDR_Bournemouth(isHome):
    if(isHome):
        return 2
    return 3

def FDR_Brighton(isHome):
    if(isHome):
        return 1
    return 2

def FDR_Burnley(isHome):
    if(isHome):
        return 3
    return 3

def FDR_Cardiff(isHome):
    if(isHome):
        return 1
    return 2

def FDR_Chelsea(isHome):
    if(isHome):
        return 4
    return 4

def FDR_CrystalPalace(isHome):
    if(isHome):
        return 2
    return 2

def FDR_Everton(isHome):
    if(isHome):
        return 2
    return 3

def FDR_Fulham(isHome):
    if(isHome):
        return 1
    return 2

def FDR_Huddersfield(isHome):
    if(isHome):
        return 1
    return 2

def FDR_Leicester(isHome):
    if(isHome):
        return 3
    return 3

def FDR_Liverpool(isHome):
    if(isHome):
        return 4
    return 5

def FDR_ManCity(isHome):
    if(isHome):
        return 4
    return 5

def FDR_ManUtd(isHome):
    if(isHome):
        return 4
    return 4

def FDR_Newcastle(isHome):
    if(isHome):
        return 2
    return 3

def FDR_Southampton(isHome):
    if(isHome):
        return 2
    return 2

def FDR_Spurs(isHome):
    if(isHome):
        return 4
    return 5

def FDR_Watford(isHome):
    if(isHome):
        return 3
    return 3

def FDR_WestHam(isHome):
    if(isHome):
        return 3
    return 3

def FDR_Wolves(isHome):
    if(isHome):
        return 3
    return 3

