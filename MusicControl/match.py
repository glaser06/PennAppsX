import editd

# s is input string
def checkArray(s, targets, threshold):
    t = s.split(" ")
    t2 = targets.split(" ")
    for j in range(0, len(t)):
        for k in range(0, len(t2)):
            if editd.sM1(t[j], t2[k]) >= threshold:
                return True
    return False
