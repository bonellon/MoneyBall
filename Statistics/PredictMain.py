from collections import OrderedDict

required = 5

def getTransferCounts(player):
    transfers_in = int(player['transfers_in_event'])
    transfers_out = int(player['transfers_out_event'])
    return transfers_in

def getHighestTransfersIn(players):
    print("Getting Highest Transfers in...")

def getHighestTransfersOut(players):
    print("Getting Highest Transfers out...")

def sortList(list):
    isSorted = False
    while not isSorted:
        changesMade = False
        for i in range(1, len(list)):
            current = list[i]
            prev = list[i-1]

            if(int(current[1]['transfers_in_event']) > int(prev[1]['transfers_in_event'])):
                list[i] = prev
                list[i - 1] = current
                changesMade = True
        if not changesMade:
            isSorted = True
    return list

def getTopTransfers(players):
    playersList = []
    for key, value in players.items():
        playersList.append([key, value])

    top = sortList(playersList[0:required])

    for playerTup in playersList[required:]:
        player = playerTup[1]

        # Update rest
        insertAtPosition = required
        updated = False

        for i in range(0, len(top)):
            current = top[i]
            if getTransferCounts(current[1]) < getTransferCounts(player):
                insertAtPosition = i
                updated = True
                break

        if updated:
            top[insertAtPosition] = playerTup
            top = sortList(top)

    return OrderedDict(top)

# getPlayerScore finds top 5 players and 1 random -> sorts and removes last element
# hack -> temp solution
def sortAndRemove(top):
    currentTop = {}
    for i in range(0, len(top)):
        currentTop[i] = top[i][1]

    sortedTop = sorted(currentTop.items(), key=lambda v: v[1]['ep_next'])
    return sortedTop