import sqlite3
import sys

class InputError(Exception):
    pass

def has_same_alphabet(word: str) -> bool:
    for i in range(len(word)):
        if word.count(word[i]) > 1:
            return True
    return False

def popular(word: str) -> int:
    popular_1_alphabets = ['e', 't', 'a', 'o', 'n', 'i', 'r', 's', 'h', 'd', 'l', 'u', 'c', 'm', 'p', 'f', 'y', 'w', 'g', 'b', 'v', 'k', 'x', 'j', 'q', 'z']
    popular_2_alphabets = ['th', 'he', 'in', 'er', 'an', 're', 'ed', 'on', 'es', 'st', 'en', 'at', 'to', 'nt', 'ha', 'nd', 'ou', 'ea', 'ng', 'as', 'or', 'ti', 'is', 'et', 'it', 'ar', 'te', 'se', 'hi', 'of']
    popular_3_alphabets = ['the', 'ing', 'and', 'her', 'ere', 'ent', 'tha', 'nth', 'was', 'eth', 'for', 'dth']
    popular_point = 0
    for i, a in enumerate(popular_1_alphabets):
        if a in word:
            popular_point += len(popular_1_alphabets) - i
    for i, a in enumerate(popular_2_alphabets):
        if a in word:
            popular_point += len(popular_2_alphabets) - i
    for i, a in enumerate(popular_3_alphabets):
        if a in word:
            popular_point += len(popular_3_alphabets) - i
    if has_same_alphabet(word):
        popular_point -= 20
    return popular_point

def is_candidate(word: str, green, yellow, black) -> bool:
    #green_check
    for i, a in enumerate(word):
        if green[i] != None and a != green[i]:
            return False
    #yellow check
    if len(yellow) != 0:
        for a in yellow:
            if not a in word:
                return False
    #black check
    for i, a in enumerate(word):
        if a in black[i]:
            return False
    return True

def make_query(green, yellow, black, word5list: list) -> str:
    for word in word5list:
        if is_candidate(word, green, yellow, black):
            return word
    return None

def stote_result(result: str, green, yellow, black):
    if len(result) != 5:
        print("Error: invalid number of character")
        raise InputError
    if len(result.rstrip("byg")) != 0:
        print("Error: invalid character")
        raise InputError
    for j, a in enumerate(result):
        if a == 'g':
            green[j] = query[j]
        elif a == 'y':
            yellow.append(query[j])
            black[j].append(query[j])
        elif a == 'b':
            for k in range(5):
                black[k].append(query[j])

def join_green(green) -> str:
    s = ""
    for g in green:
        if g == None:
            s += "?"
        else:
            s += g
    return s

if __name__ == "__main__":
    print("Wordle solver v0.1")
    con = sqlite3.connect("wn.db")
    cur = con.execute("select lemma from word where lang='eng'")
    word_5 = []
    for row in cur:
        if len(row[0]) == 5:
            word_5.append(row[0])
    word_5 = list(set(word_5))
    word_5.sort(key=popular, reverse=True)
    green = [None, None, None, None, None]
    yellow = []
    black = [[], [], [], [], []]
    i = 0
    while i < 6:
        i += 1
        query = make_query(green, yellow, black, word_5)
        if query == None:
            print("Cannot find anser word from DB!!")
            break
        print(i, "query:", f'"{query}"', "?", end=" ")
        while True:
            result = input()
            if result == "e":
                word_5.remove(query)
                i -= 1
                break
            try:
                stote_result(result, green, yellow, black)
            except InputError:
                continue
            break
        if green.count(None) == 0:
            print(f"success {query} {i}/6")
            sys.exit(0)
    print(f"failure {join_green(green)} X/6")
