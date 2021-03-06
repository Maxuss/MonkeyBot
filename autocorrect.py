import json
from data import ExitForLoop
# ADDS WORDS FROM bz_ac.json
with open('bz_ac.json', 'r') as bac:
    ac = json.load(bac)
    print("AutoCorrect Database Connected!")
inp_words = list(ac.keys())

# FUNCTIONS TO CHECK WORDS
def correctWord(word: str):
    strr = word.lower()
    words = strr.split(" ")
    second_word = words[1]
    first_word = words[0]
    if first_word in "enchanted":
        first_word = 'enchanted'
    if strr.startswith("e") and not strr.startswith("en"):
        strrr = strr.replace("e", "enchanted", 1)
        words = list(strrr.split(" ", 1))
        print(words)
        second_word = words[1]
        if second_word.endswith("block"):
            swords = list(second_word.rsplit(" ", 1))
            print(swords)
            third_word = swords[0]
            block = swords[-1]
    try:
        try:
            period_word = ac[third_word]
        except UnboundLocalError:
            try:
                period_word = ac[second_word]
            except UnboundLocalError:
                pass
    except KeyError:
        pass
    try:
        new_word = first_word + "_" + period_word + "_" + block
        return new_word
    except UnboundLocalError:
        try:
            new_word = first_word + "_" + period_word
            return new_word
        except UnboundLocalError:
            try:
                new_word = first_word + "_" + second_word
                return new_word
            except UnboundLocalError:
                return word
print("AutoCorrect System Connected!")
print("Use correctWord(string) to correct!")
