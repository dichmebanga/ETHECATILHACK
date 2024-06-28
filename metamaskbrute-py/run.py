import argparse
import random

def generate_seed_phrase(lang):
    # Initial wordlists
    fours = []
    fives = []
    sixes = []
    sevens = []

    wordlist_files = {
        "eng" : "eng.txt",
        "fren" : 'fre.txt',
        "czech" : 'cze.txt',
        "itali" : 'itali.txt',
        "jp" : 'jp.txt',
        "kor" : 'kor.txt',
        "por" : 'por.txt',
        "span" : 'span.txt',
        "cn1" : 'cn_simple.txt',
        "cn2" : 'cn_tradition.txt'
    }

    if lang not in wordlist_files:
        raise ValueError("Unsupported language specified")

    wordlist_file = wordlist_files[lang]

    # Fill above lists with corresponding word lengths from wordlist
    with open(f"./WordListKeyMetaMask/{wordlist_file}") as wordlist:
        for line in wordlist:
            if len(line) == 4:
                fours.append(line.strip())
            elif len(line) == 5:
                fives.append(line.strip())
            elif len(line) == 6:
                sixes.append(line.strip())
            elif len(line) == 7:
                sevens.append(line.strip())

    # Create new lists and fill with number of items in fours
    fivesLess = []
    sixesLess = []
    sevensLess = []

    fivesCounter = 0
    while fivesCounter < len(fours):
        randFive = random.choice(fives)
        if randFive not in fivesLess:
            fivesLess.append(randFive)
            fivesCounter += 1

    sixesCounter = 0
    while sixesCounter < len(fours):
        randSix = random.choice(sixes)
        if randSix not in sixesLess:
            sixesLess.append(randSix)
            sixesCounter += 1

    sevensCounter = 0
    while sevensCounter < len(fours):
        randSeven = random.choice(sevens)
        if randSeven not in sevensLess:
            sevensLess.append(randSeven)
            sevensCounter += 1

    choices = [fours, fivesLess, sixesLess, sevensLess]

    # Generate seed phrase
    seed = []
    while len(seed) < 12:
        wordLengthChoice = random.choice(choices)
        wordChoice = random.choice(wordLengthChoice)
        seed.append(wordChoice)

    # Convert seed phrase to string
    seed_phrase = ' '.join(seed)

    # Save seed phrase to file (append mode)
    with open('seed_phrase.txt', 'a') as file:
        file.write(seed_phrase + '\n')

def main():
    parser = argparse.ArgumentParser(description='Generate seed phrases')
    parser.add_argument('numbergenerator', metavar='N', type=int, help='Number of iterations to generate seed phrases')
    parser.add_argument('language', metavar='L', type=str, help='Language key for the wordlist to use')
    args = parser.parse_args()

    for _ in range(args.numbergenerator):
        generate_seed_phrase(args.language)
    print("New seed phrase appended to seed_phrase.txt")

if __name__ == "__main__":
    main()
