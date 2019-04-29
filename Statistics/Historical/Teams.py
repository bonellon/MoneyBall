from Statistics.Historical.TeamsEnum import TeamsEnum

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

def FDR_Crystal_Palace(isHome):
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

def FDR_Leicester_City(isHome):
    if(isHome):
        return 3
    return 3

def FDR_Liverpool(isHome):
    if(isHome):
        return 4
    return 5

def FDR_Manchester_City(isHome):
    if(isHome):
        return 4
    return 5

def FDR_Manchester_United(isHome):
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

def FDR_West_Ham(isHome):
    if(isHome):
        return 3
    return 3

def FDR_Wolves(isHome):
    if(isHome):
        return 3
    return 3

def GetFDR(team, isHome):
    import sys
    current_module = sys.modules[__name__]

    methodName = 'FDR_'+str(TeamsEnum(team).name)
    method = getattr(current_module, methodName)(isHome)
    return method