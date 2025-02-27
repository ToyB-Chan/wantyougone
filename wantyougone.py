# this script preserves extra spaces
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import time
import pygame

def type_with_wpm(text, wpm):
    words = text.split(" ")  # Split by space to preserve extra spaces
    skip_next = False
    for word in words:
        if skip_next:
            skip_next = False
            continue
        if '/f' in word:
            wpm *= 2
            word = word.replace('/f', '')
        elif '/s' in word:
            wpm /= 1.5
            word = word.replace('/s', '')
        elif '/rs' in word:
            wpm /= 2
            word = word.replace('/rs', '')
        elif '/ns' in word:
            wpm = original_wpm
            word = word.replace('/ns', '')
        elif '/i' in word:
            wpm *= 9999999999
            word = word.replace('/i', '')
        elif '/nl' in word:
            print()
            continue
        elif word.startswith('/d'):
            split_word = word.split("/d")
            if len(split_word) > 1 and split_word[1].strip():
                delay = float(split_word[1])
            else:
                delay = 0
            time.sleep(delay)
            skip_next = True
            continue
        
        delay = 60 / wpm
        
        for i, char in enumerate(word):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        
        if word != words[-1]:
            sys.stdout.write(' ')
            sys.stdout.flush()
            time.sleep(delay)
    sys.stdout.flush()


lyrics_file = './lyrics.txt'
if not os.path.exists(lyrics_file):
    print("Unable to find the file 'lyrics.txt'.")
    sys.exit()

with open(lyrics_file, 'r') as file:
    lyrics = file.read()

bg_music_file = "wyg.mp3"
if not os.path.exists(bg_music_file):
    print("Unable to find the file 'wyg.mp3'. Background music will not play.")

pygame.init()
if os.path.exists(bg_music_file):
    pygame.mixer.music.load(bg_music_file)
    pygame.mixer.music.play()

original_wpm = 800 
wpm = original_wpm

print("\033[38;2;255;212;87m") # set foreground color
print("\033[48;2;78;44;11m") # set background color
print("\033[2J") # clear screen
print("\033[H") # set cursor to top left position

for line in lyrics.split("\n"):
    if '/c' in line:
        print("\033[2J") # clear screen
        print("\033[H") # set cursor to top left position
    elif line.strip() and '/nl' not in line:
        type_with_wpm(line, wpm)
        print()
    elif line.strip():
        type_with_wpm(line, wpm)

print("\033[0;0m") # reset all formatting
pygame.mixer.music.stop()
