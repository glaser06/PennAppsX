import editd


def checkArray(s, target, threshold):
    for i in range(0, len(s)):
        t = s[i].split(" ")
        for j in range(0, len(t)):
            if editd.sM1(t[j], target) >= threshold:
                return True
    return False
