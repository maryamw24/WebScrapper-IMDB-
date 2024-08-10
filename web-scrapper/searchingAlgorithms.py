
def linearSearch(arr: list,attribute: str, mode: str, toCheck: str)->list:
    result = []
    mode = mode.lower()
    i = 0
    for i in arr:
        word = str(getattr(i,attribute))
        if mode == "exact" and str(word.lower()) == toCheck.lower():
            result.append(i)
        if mode == "starts with" and startWith(word.lower(), toCheck.lower()):
            result.append(i)
        if mode == "ends with" and endWith(word.lower(), toCheck.lower()):
            result.append(i)
        if mode == "contains" and contains(word.lower(), toCheck.lower()):
            result.append(i)
    return result


def startWith(word: str, toCheck: str)->bool:
    n = len(toCheck)
    if (n>len(word)):
        return False
    flag = False
    for i in range(n):
        if word[i] != toCheck[i]:
            return False
    return True
        

def endWith(word: str, toCheck: str)->bool:
    n = len(toCheck)
    if (n>len(word)):
        return False
    flag = False
    i = 0
    for j in range(len(word)-n, len(word)):
        if word[j] != toCheck[i]:
            return False
        else: i+=1
    return True

def contains(word: str, toCheck: str)->bool:
    n = len(toCheck)
    if (n>len(word)):
        return False
    i = 0
    while(i < len(word) - len(toCheck)+1):
        idx = i
        for j in range(n):
            if word[idx] != toCheck[j]:
                break
            idx+=1
        else:
            return True
        i+=1
    return False



if __name__ == "__main__":
    print(contains("Maryaiom", "aiol"))
