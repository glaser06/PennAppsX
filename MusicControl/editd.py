def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def sM0(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()
    return float(max(len(s1), len(s2)) - levenshtein(s1, s2)) / float(max(len(s1), len(s2)))


def sM1(s1, s2):
    if(s2 == ""):
        return (s1 == s2) + 0
    s1 = s1.lower()
    s2 = s2.lower()
    c = 0
    t = 0
    m = min(len(s1), len(s2))
    for i in range(0, len(s1)):
        for j in range(i, len(s1)):
            if j - i + 1 <= m:
                c += (s1[i:(j+1)] in s2)
                t += 1
    for i in range(0, len(s2)):
        for j in range(i, len(s2)):
            if j - i + 1 <= m:
                c += (s2[i:(j+1)] in s1)
                t += 1
    return float(c)/float(t)


def sM2(a, b):
    import difflib
    seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
    return seq.ratio()

if __name__ == "__main__":
    print(sM2("hi", "hi"))
    print(sM2("hiiii", "jiiii"))
    print(sM2("abcde", "jiiii"))
    print(sM1("hi", "hi"))
    print(sM1("hiiii", "jiiii"))
    print(sM1("abcde", "jiiii"))
    print(sM0("hi", "hi"))
    print(sM0("hiiii", "jiiii"))
    print(sM0("abcde", "jiiii"))
