#!/usr/bin/env python3
"""Wordle solver — information-theoretic word guesser."""
import sys, math, random
from collections import Counter

COMMON_WORDS = ["crane","slate","trace","audio","raise","stare","arise","irate",
    "snare","crate","plane","steal","great","train","learn","heart","clean","dream",
    "steam","trail","grain","claim","brain","chair","paint","flash","blank","charm",
    "draft","flame","frame","grant","grape","graph","guard","harsh","kneel","lance",
    "manor","marsh","nerve","ocean","panel","patch","pause","pearl","phase","plant",
    "plate","plead","pouch","pound","prove","queen","quest","quote","range","rapid",
    "realm","reign","relax","ridge","rival","rouge","route","sauce","scale","scare",
    "scene","scope","shade","shame","shape","share","sharp","shear","shelf","shell",
    "shift","shine","shirt","shock","shore","short","shout","shown","siege","sight"]

def score_guess(guess, answer):
    result = ['⬛'] * 5
    answer_chars = list(answer)
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = '🟩'; answer_chars[i] = None
    for i in range(5):
        if result[i] == '🟩': continue
        if guess[i] in answer_chars:
            result[i] = '🟨'; answer_chars[answer_chars.index(guess[i])] = None
    return ''.join(result)

def filter_words(words, guess, pattern):
    result = []
    for w in words:
        if score_guess(guess, w) == pattern:
            result.append(w)
    return result

def entropy(guess, words):
    patterns = Counter(score_guess(guess, w) for w in words)
    total = len(words)
    return -sum(c/total * math.log2(c/total) for c in patterns.values())

if __name__ == "__main__":
    words = COMMON_WORDS
    if sys.argv[1:] == ["play"]:
        answer = random.choice(words)
        for turn in range(6):
            guess = input(f"Guess {turn+1}/6: ").lower().strip()
            pattern = score_guess(guess, answer)
            print(f"  {pattern}")
            if pattern == "🟩🟩🟩🟩🟩": print("🎉 You got it!"); break
        else:
            print(f"Answer was: {answer}")
    else:
        # Show best openers by entropy
        print("Top openers by information entropy:")
        scored = [(w, entropy(w, words)) for w in words[:20]]
        scored.sort(key=lambda x: -x[1])
        for w, e in scored[:10]:
            print(f"  {w}: {e:.3f} bits")
