x=list(range(0,100))
import random
print(x)
def trnSelect(tournamentMembers):
    best = None
    for i in tournamentMembers:
        if best==None:
            best = 1
        if i>best:
            best=i
    return best

def tournament (x,tournamentsize=1,numberToSelect=6,selected=[]):
    #global selected
    random.shuffle(x)
    tournamentMembers = []
    if numberToSelect==0:
        return selected
    for i in range(0,tournamentsize):
        tournamentMembers.append(x[random.randint(0,len(x)-1)])
    print (tournamentMembers)
    #for i in range(0,numberToSelect):
   # best = trnSelect(tournamentMembers)
    selected.append(trnSelect(tournamentMembers))
    tournament(x,tournamentsize=tournamentsize, numberToSelect=numberToSelect-1,selected=selected)

    print (selected)



tournament(x,4)