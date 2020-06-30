""" Frequency Class 

Creates a Frequency Class that measures the rarity and frequency of words in a given
file. Rarity is sorted by COMMON, UNCOMMON, RARE, and MISPELT. Frequency is ranked 
using QuickSort algorithm. 
"""
__author__ = 'Nicholas Chua'
__docformat__ = 'reStructuredText'
__modified__ = '05/06/2020'
__since__ = '25/05/2020'

from hash_table import LinearProbeHashTable
from dictionary import Dictionary
from list import ArrayList
from enum import Enum

class Rarity(Enum):
    '''Returns rarity based on given number from Frequency.rarity() method
    :complexity: O(1)
    '''
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    MISPELT = 4

class Frequency():
    def __init__(self) -> None:
        '''Initiates a hash_table instance based on given hash_base & table_size, and max_word
        for the word with the highest frequency.
        
        :complexity: O(N), where N is the table_size
        '''
        self.hash_table = LinearProbeHashTable(27183, 1000081)
        self.dictionary = Dictionary(27183, 1000081)
        self.dictionary.load_dictionary("english_large.txt")
        self.max_word = ("",0) 

    def add_file(self, filename:str) -> None:
        '''Loads words from file name into hash_table. Each line has multiple words and each  
        word is required to be stored separately.
        
        :complexity: O(L*W) as it iterates through each word in each line of the file, 
                    where L is the length of lines in a file and W is the length of words in each line.
        '''
        with open(filename, 'r', encoding = 'utf-8') as file:
            for line in file:
                for word in line.split():
                    word = word.lower() # sets to lowercase in the code block
                    if word in self.hash_table:
                        # increments occurrence of word
                        self.hash_table[word] += 1 
                    else:
                        # stores word and sets occurence of word to one
                        self.hash_table[word] = 1
                    
                    # checks if current word has the most occurrence compared to max_word
                    if self.hash_table[word] > self.max_word[1]:
                        self.max_word = (word, self.hash_table[word])
    
    def rarity(self, word: str) -> Rarity:
        '''Returns a string describing a given word's rarity. 
        If a word appears at least max_word/100 times, then the word is COMMON. 
        If a word appears less than max_word/1000 times, then the word is RARE. 
        If a word appears less than max_word/100 times and greater or equal to max_word/1000 times, then the word 
        is UNCOMMON. 
        If word doesn't exist, then the word is MISPELT.
        
        :complexity best: O(K) where the given word is the first searched position in the hash table, using linear
                        probe, where K is the size of the key
        :complexity worst: O(K+N) where the given word is the last searched position in the hash table or not found, 
                        using linear probe, where N is the size of the hash_table
        '''
        try:
            word_frequency = self.hash_table[word.lower()] # loads the frequency of given word
            if word_frequency >= self.max_word[1]/100:
                return Rarity(1) # should return COMMON
            elif word_frequency < self.max_word[1]/1000:
                return Rarity(3) # should return RARE
            elif word_frequency < self.max_word/100 and word_frequency >= self.max_word[1]/1000:
                return Rarity(2) # should return UNCOMMON
        except KeyError:
            return Rarity(4) # should return MISPELT
    
    def quick_sort(self, array:ArrayList) -> None:
        '''Initialises QuickSort algorithm to sort frequency of words in descending order.

        :complexity best: O(N*logN) when the pivot is the median, where N represents the size of the list.
        :complexity worst: O(N^2) when the pivot is min/max, where N represents the size of the list.
        '''
        start = 0 
        end = array.length - 1
        self.__quick_sort_aux(array, start, end)
    
    def __quick_sort_aux(self, array:ArrayList, start:int, end:int) -> None:
        '''Applies the QuickSort algorithm using recursion to sort frequency of words in descending order.

        :complexity best: O(N*logN) when the pivot is the median, where N represents the size of the list.
        :complexity worst: O(N^2) when the pivot is min/max, where N represents the size of the list.
        '''
        if start < end:
            boundary = self.__partition(array, start, end)
            self.__quick_sort_aux(array, start, boundary-1)
            self.__quick_sort_aux(array, boundary+1, end)
            
    def __partition(self, array:ArrayList, start:int, end:int) -> int:
        '''Part of the QuickSort algorithm. Allocates the pivot and sorts items before or after the pivot.

        :complexity: O(N) as it iterates through the entire array, where N represents the size of the list.
        '''
        mid = (start + end) // 2
        pivot = array[mid][1] # accesses only the number
        self.__swap(array, start, mid)
        boundary = start
        for k in range(start+1, end+1):
            if array[k][1] > pivot: # sorts in descending order
                boundary += 1
                self.__swap(array, k, boundary)
        self.__swap(array, start, boundary)
        return boundary

    def __swap(self, array:ArrayList, index1:int, index2:int) -> None:
        '''Swaps the two items from the given indexes. 
        :complexity: O(1) 
        '''
        temp = array[index1]
        array[index1] = array[index2]
        array[index2] = temp

    def ranking(self) -> ArrayList[tuple]:
        '''Returns a List of the words from hash_table, ranked from most frequent word to least frequent word. Sorts using 
        QuickSort algorithm.
        
        :complexity best: O(N*logN) when QuickSort picks the median as the pivot, where N represents the size of the list.
        :complexity worst: O(N^2) when QuickSort picks the min/max as the pivot, where N represents the size of the list.
        '''
        known_words = ArrayList(self.hash_table.count)
        count = 0
        hashkeys = self.hash_table.table.array._objects # directory of all the hashkeys in the hash_table, stored as a dictionary
        for key in hashkeys: 
            item = hashkeys[key] # gets the item from the dictionary using the hashkey
            known_words.insert(count, item) # stores item into ArrayList
            count += 1
        self.quick_sort(known_words)
        return known_words

def frequency_analysis() -> None:
    '''Performs analysis on frequency of words from "84-0.txt" file. Shows the top ranking words, based on
    user's input
    '''
    frequency = Frequency()
    frequency.add_file("84-0.txt")
    frequency_rankings = frequency.ranking()

    correct_input = False
    while not correct_input:
        user_input = int(input("Number of rankings to show: "))
        try:
            if user_input < 0 and user_input > frequency.hash_table.count:
                # executes when input is outside the range of hash_table.count
                raise Exception
        except ValueError as error:
            # for strings, symbols, or for inputs with other data types
            print(error+" Try again")
        except Exception:
            # for inputs outside the range of rankings
            print("Input was outside the range of the rankings. Try again.\n")
        else:
            correct_input = True
    
    # displays statistics of the number of rankings suggested by user
    for rank in range(user_input):
        word = frequency_rankings[rank][0]
        word_frequency = frequency_rankings[rank][1]
        word_rarity = frequency.rarity(str(word))
        print(str(word)+", "+str(word_frequency)+", "+str(word_rarity))

if __name__ == '__main__':
    test_1342 = Frequency()
    test_1342.add_file('1342-0.txt')
    test_2600 = Frequency()
    test_2600.add_file('2600-0.txt')
    test_98 = Frequency()
    test_98.add_file('98-0.txt')
    test_all = Frequency()
    test_all.add_file('1342-0.txt')
    test_all.add_file('2600-0.txt')
    test_all.add_file('98-0.txt')
    
    # import sys
    # sys.setrecursionlimit(10000)
    # frequency_analysis()
