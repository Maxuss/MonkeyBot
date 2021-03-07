import json
from data import ExitForLoop
import logging

console = logging.StreamHandler()  
console.setLevel(logging.ERROR)  
logging.getLogger("").addHandler(console)

# ADDS WORDS FROM bz_ac.json
with open('bz_ac.json', 'r') as bac:
    ac = json.load(bac)
    print("AutoCorrect Database Connected!")
inp_words = list(ac.keys())

# FUNCTIONS TO CHECK WORDS
def correctWord(word: str):
    try:
        strr = word.lower()
        try:
            first_word = ac[strr]
        except KeyError:
            try:    
                words = strr.split(" ")
                second_word = words[1]
                first_word = words[0]
            except IndexError:
                raise ExitForLoop
        if first_word in "enchanted":
            first_word = 'enchanted'
        if strr.startswith("e") and not strr.startswith("en"):
            try:
                strrr = strr.replace("e", "enchanted", 1)
                words = list(strrr.split(" ", 1))
                second_word = words[1]
            except IndexError:
                print("COULDN'T FIND THIS ITEM!")
            if second_word.endswith("block"):
                swords = list(second_word.rsplit(" ", 1))
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
            print('block')
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
                    try:
                        new_word = first_word
                        return new_word
                    except UnboundLocalError:
                        new_word = word
                        return new_word
    except ExitForLoop:
        new_word = word
        return new_word
    print("Successfully corrected " + word + " to " + new_word + "!")
    logging.info("BAZAAR_AUTOCORRECT: CHANGED '" + word.upper() + "' TO '" + new_word.upper() + "'")
    words.clear()

print("AutoCorrect System Connected!")
print("Use correctWord(string) to correct!")
