""" Dictionary Class Object

Creates a Dictionary Class that imports words from a given dictionary file. 
User can also add, delete and find words. Python script also contains a Statistics 
Class that measures the run-time and collisions of various hash_bases and table_sizes. 
"""
__author__ = 'Nicholas Chua'
__docformat__ = 'reStructuredText'
__modified__ = '05/06/2020'
__since__ = '25/05/2020'

from hash_table import LinearProbeHashTable, T
from timeit import default_timer as timer

class Dictionary(LinearProbeHashTable[T]):
    def __init__(self, hash_base:int, table_size:int) -> None:
        '''Initiates a hash_table instance based on given hash_base and table_size
        
        :complexity: O(N), where N is the table_size
        '''
        self.hash_table = LinearProbeHashTable(hash_base, table_size)

    def load_dictionary(self, filename:str, time_limit:int=None) -> int:
        '''Loads words from file name into hash_table. Each line is a word.
        
        :complexity: O(N), where N is the length of lines in a file
        '''
        word_count = 0 
        with open(filename, 'r', encoding = 'utf-8') as file:
            start_time = timer()    
            for word in file:
                if time_limit != None and timer() - start_time > time_limit:
                    raise TimeoutError("Time limit exceeded. Load dictionary failed.")
                self.add_word(word.strip("\n"))
                word_count += 1
        return word_count
    
    def add_word(self, word:str) -> None:
        '''Adds a given word and stores into hash_table. Word is paired with 1 as the value-pair.
        :complexity best: O(K) where the first searched position is empty, using linear probe,
                          where K is the size of the key
        :complexity worst: O(N^2) when we've searched the entire table, using linear probe, and 
                           the table is rehashed, where N is the table_size
        '''
        self.hash_table[word.lower()] = 1
    
    def find_word(self, word:str) -> bool:
        '''Returns true if given word exists in dictionary. Otherwise, returns false.
        :complexity best: O(K) where the given word is the first searched position, using linear
                        probe, where K is the size of the key
        :complexity worst: O(N) where the given word is the last searched position, using linear
                        probe, where N is the size of the hash_table
        :raises KeyError: When a position can't be found
        '''
        return self.hash_table[word.lower()] == 1

    def delete_word(self, word:str) -> None:
        '''Deletes the given word from the dictionary. Otherwise, raises KeyError.
        :complexity best: O(K) finds the position straight away and doesn't have to rehash
                          where K is the size of the key
        :complexity worst: O(K + N) when it has to rehash all items in the hash table
                          where N is the table size
        :raises KeyError: When a position can't be found
        '''
        self.hash_table.__delitem__(word.lower())
    
    def menu(self) -> None:
        '''Initiates a menu in terminal. Uses methods in Dictionary class. Runs for as long as 
        user uses the menu, in other words, while exit_boolean is false. Terminates when exit_boolean 
        is true.'''
        exit_boolean = False
        while not exit_boolean:
            print("Select option: ")
            print("1 - Read file")
            print("2 - Add a word")
            print("3 - Find a word")
            print("4 - Delete a word")
            print("5 - Exit")

            try:
                option = int(input())
                if option < 1 or option > 5:
                    raise ValueError
            except ValueError:
                print("Input given is invalid, try again!") 
            else:
                if option == 1:
                    # handles ValueError for time_limit. Sets strings and empty inputs to None
                    try:
                        filename = input("What file would you like to import? ")
                        time_limit = int(input("How long do you want to wait? (For no time limit, just press enter)"))
                    except ValueError:
                        time_limit = None

                    # handles FileNotFoundError. Returns to menu if not found. 
                    try:
                        total_words = self.load_dictionary(filename, time_limit)
                    except FileNotFoundError:
                        print("File not found. Input was not given the correct directory. Returning to menu.")
                    else:
                        print("File successfully imported "+str(total_words)+" words!")
                elif option == 2:
                    word = input("What word would you like to add? ")
                    self.add_word(word)
                elif option == 3:
                    try:
                        word = input("What word do you want to find? ")
                        self.find_word(word)
                    except KeyError as e:
                        print("Key doesn't exist: "+str(e))
                    else:
                        print("Key found!")
                elif option == 4:
                    try:
                        word = input("What word that exists in the dictionary would you like to delete? ")
                        self.delete_word(word)
                    except KeyError as e:
                        print("Key doesn't exist: "+str(e))
                    else:
                        print("Key successfully deleted!")
                elif option == 5:
                    print("Exiting program. ")
                    exit_boolean = True

class Statistics:
    def load_statistics(self, hash_base:int, table_size:int, filename:str, max_time:int) -> tuple:
        '''Imports a given dictionary and measures run-time based on hash_base & table_size. 
        If max_time has been exceeded, load_dictionary will abort. Returns dictionary and collision
        statistics. 

        :complexity: O(N), where N is the length of lines in a file
        '''
        dictionary = Dictionary(hash_base, table_size)
        try:
            start_time = timer()
            words = dictionary.load_dictionary(filename, max_time) # returns the word count of filename
            final_time = timer() - start_time
        except TimeoutError:
            words = "TIMEOUT"
            final_time = "TIMEOUT"
        
        return (words, final_time, dictionary.hash_table.collision_count, dictionary.hash_table.probe_total, dictionary.hash_table.probe_max, 
        dictionary.hash_table.rehash_count)

    def table_load_statistics(self, max_time) -> None:
        '''Outputs a CSV file named 'output_task2.csv' based from dictionary statistics given by 
        load_statistics. Each dictionary is tested for run-time based on differing hash_base & 
        table_size.

        Run-time WILL differ based on table_load_limit, which may cause table to rehash. See __setitem__ in 
        hash_table.py
        
        :complexity best: O(N*C) as it iterates through each hash combination and imports each line in a file,
                    where N is the length of lines in a file and C is the length of each combination.
        :complexity worst: O(N*C*H) when it needs to rehash the table, where H is the length of the already
                    existing hash table
        '''
        dictionaries_array = ["english_small.txt", "english_large.txt", "french.txt"]
        bases_array = [1, 27183, 250726]
        table_size_array = [250727, 402221, 1000081]
        statistics_array = []

        # setting up combinations for hashing to minimise O-complexity
        hash_combinations = []
        for base in bases_array:
            for table_size in table_size_array:
                hash_combinations.append((base, table_size))

        for dictionary in dictionaries_array:
            for combo in hash_combinations:
                words, time, collision_count, probe_total, probe_max, rehash_count = self.load_statistics(combo[0], combo[1], 
                dictionary, max_time)

                if time == "TIMEOUT":
                    # uses max_time when time has exceed max_time
                    data = [dictionary, combo[0], combo[1], words, collision_count, probe_total, probe_max, rehash_count, max_time]
                    statistics_array.append(data)
                else:
                    # otherwise uses actual time
                    data = [dictionary, combo[0], combo[1], words, collision_count, probe_total, probe_max, rehash_count, time]
                    statistics_array.append(data)

        with open("output_task2.csv", "w") as file:
            file.write("Dictionary, Hash Base, Table Size, Total Words, Collision Count, Probe Total, Probe Max, Rehash Count, Time \n")
            for data_line in statistics_array:
                file.write(str(data_line[0])+", "+str(data_line[1])+", "+str(data_line[2])+", "+str(data_line[3])+", "+str(data_line[4])
                +", "+str(data_line[5])+", "+str(data_line[6])+", "+str(data_line[7])+", "+str(data_line[8])+" \n")

if __name__ == '__main__':
    # dictionary = Dictionary(31, 17)
    # dictionary.menu()

    Statistics().table_load_statistics(10)