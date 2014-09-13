import editd

# s is input string
def checkArray(s, target, threshold):
    t = s.split(" ")
    for j in range(0, len(t)):
        if editd.sM1(t[j], target) >= threshold:
            return True
    return False
