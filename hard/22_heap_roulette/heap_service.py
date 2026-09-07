#!/usr/bin/env python3

import sys
import os

MAX_NOTES = 8
MAX_SIZE = 0x80

notes = [{'content': None, 'size': 0, 'in_use': False} for _ in range(MAX_NOTES)]

def read_str():
    try:
        return input().strip()[:MAX_SIZE]
    except:
        return ''

def read_int():
    try:
        return int(input().strip())
    except:
        return 0

def find_free_slot():
    for i in range(MAX_NOTES):
        if not notes[i]['in_use']:
            return i
    return -1

def create_note():
    idx = find_free_slot()
    if idx == -1:
        print("No free slots!")
        return
    
    print("Size: ", end='', flush=True)
    size = read_int()
    
    if size > MAX_SIZE or size == 0:
        print("Invalid size!")
        return
    
    print("Content: ", end='', flush=True)
    content = read_str()
    
    notes[idx]['content'] = content
    notes[idx]['size'] = size
    notes[idx]['in_use'] = True
    
    print(f"Created note {idx}")

def edit_note():
    print("Index: ", end='', flush=True)
    idx = read_int()
    
    if idx < 0 or idx >= MAX_NOTES or not notes[idx]['in_use']:
        print("Invalid index!")
        return
    
    print("New content: ", end='', flush=True)
    content = read_str()
    
    # BUG: Can write more than allocated size
    notes[idx]['content'] = content[:notes[idx]['size'] + 1]
    
    print("Updated!")

def delete_note():
    print("Index: ", end='', flush=True)
    idx = read_int()
    
    if idx < 0 or idx >= MAX_NOTES or not notes[idx]['in_use']:
        print("Invalid index!")
        return
    
    # BUG: Don't clear content, just mark as not in use
    notes[idx]['in_use'] = False
    # Content still accessible!
    
    print("Deleted!")

def view_note():
    print("Index: ", end='', flush=True)
    idx = read_int()
    
    if idx < 0 or idx >= MAX_NOTES:
        print("Invalid index!")
        return
    
    if notes[idx]['content'] is not None:
        print(f"Content: {notes[idx]['content']}")
        print(f"Size: {notes[idx]['size']}")
    else:
        print("Empty note")

def main():
    print("=============================")
    print("  Heap Roulette v2.0")
    print("  College CTF 2026")
    print("=============================")
    print()
    print("Can you corrupt the heap and get a shell?")
    print()
    
    while True:
        print("\n=== Heap Roulette ===")
        print("1. Create note")
        print("2. Edit note")
        print("3. Delete note")
        print("4. View note")
        print("5. Exit")
        print("> ", end='', flush=True)
        
        choice = read_int()
        
        if choice == 1:
            create_note()
        elif choice == 2:
            edit_note()
        elif choice == 3:
            delete_note()
        elif choice == 4:
            view_note()
        elif choice == 5:
            print("Bye!")
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()
