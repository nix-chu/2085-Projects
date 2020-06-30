"""
Anagram Searcher

Finds anagrams of given input, based on given strings and files. 
"""

__author__ = "Nicholas Chua"
__docformat__ = 'reStructuredText'
__since__ = '28/06/2013'
__modified__ = '11/06/2020'

from binary_search_list_tree import BinarySearchListTree
import sys

def read_from_file(filename: str, my_tree: BinarySearchListTree[str, str]) -> None:
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.isalpha():
                sorted_string = "".join(sorted(line.lower()))
                print("Inserting:", line, "->", sorted_string)
                # TODO: Add word to my_tree
                my_tree[sorted_string] = line
            else:
                print("Error: Input string %s from file %s" % (line, filename))

def menu() -> None:
    my_tree = BinarySearchListTree()
    quit_program = False
    options = ["Prac7 Anagram Tree Menu Options:",
               "Read String",
               "Read File",
               "List",
               "Search",
               "Anagram",
               "Quit"]

    while not quit_program:
        print()
        for i, option in enumerate(options):
            optnum = "%d. " % i if i > 0 else ""
            print(optnum, option, sep="")

        command = input("Please press a number, then <enter>: ").strip()

        if command == "1":                                   # Read string
            input_string = input("Please enter a string: ").strip()
            if input_string.isalpha():
                sorted_string = "".join(sorted(input_string.lower()))
                print("Inserting:", input_string, "->", sorted_string)
                # TODO: Add string to my_tree
                my_tree[sorted_string] = input_string
            else:
                print("ERROR: String not alphanumerical or zero length")

        elif command == "2":                                  # Read file
            filename = input("Filename: ")
            try:
                read_from_file(filename, my_tree)
            except IOError:
                print("Error reading from file:", filename)

        elif command == "3":                                  # List words in BST
            for anagram in my_tree:
                string = ""
                for words in anagram[1]:
                    string += str(words)+", "
                print(anagram[0]+" = "+string)
            print("Done!")

        elif command == "4":                                  # Search
            input_string = input("Search string: ").strip()
            if input_string.isalpha():
                sorted_string = "".join(sorted(input_string.lower()))
                print("Searching:", input_string)
                # TODO: Add search code
                try: 
                    items = my_tree[sorted_string]
                except KeyError:
                    print("Item could not be found. Returning to menu")
                else:
                    print("Item found!")
            else:
                print("Error: please enter a good string")

        elif command == "5":                                   # Anagram
            input_string = input("Find anagrams of word: ").strip()
            if input_string.isalpha():
                sorted_string = "".join(sorted(input_string.lower()))
                print("Searching for anagrams of: "+input_string)
                try:
                    anagram_list = my_tree[sorted_string]
                    if len(anagram_list) == 1: 
                        # if list found has only one element, then there must be no other anagrams
                        raise KeyError
                except KeyError:
                    print("No anagram found")
                else:
                    for word in anagram_list:
                        if word is not input_string:
                            print(word)
                    print("Done!")
            else:
                print("Error: please enter a good string")

        elif command == "6":                                   # Quit
            quit_program = True

        else:
            print("Human Error: unrecognised command number!")

if __name__ == '__main__':
    menu()
