# FIT2085 Code Review 2
import timeit
import random
import csv_plotting
import os
from typing import List

def shaker_sortII(a_list):
    '''Sorts a list using Shaker Sort algorithm

    a_list: usually an unsorted list

    :complexity: Best O(N), when all elements in the list has been sorted. Worst O(N^2), when the list is 
                 in reverse order. 
    '''
    left = 0
    right = len(a_list) - 1
    mark = 0 # initialising mark 
    swapped = True # to initiate while loop

    while swapped:
        swapped = False # the start of a new iteration

        # left to right passes 
        for i in range(left, right):
            item = a_list[i]
            item_to_right = a_list[i+1]

            if item > item_to_right:
                # swaps when item is larger to item to right
                a_list[i] = item_to_right
                a_list[i+1] = item
                mark = i+1 # final value for this should be the index of the last swapped element
                swapped = True
        
        if not swapped:
            break # executes when no swap occurred in left-to-right passing
       
        right = mark # assigns the index of the last swapped element, every element to the right must be sorted
        swapped = False # resets swapped value for next passing

        # right to left passes
        for i in range(right, left, -1):
            item = a_list[i]
            item_to_left = a_list[i-1]

            if item < item_to_left:
                a_list[i] = item_to_left
                a_list[i-1] = item
                mark = i-1 # final value for this should be the index of the last swapped element
                swapped = True

        left = mark # assigns the index of the last swapped element, every element to the left must be sorted
    
    return a_list

def __create_list(length:int, lower:int, upper:int) -> List[int]:
    """ Creates a list of given length where elements are random 
    integers within interval [upper,lower]. 

    :pre: lower<=upper
    :post: returned list has length elements within [upper,lower]
    """

    # precondition
    assert lower <= upper, ValueError("The value of lower must be LOWER than the value of upper")

    # actual code
    a_list = [0]*length
    for i in range(length):
        a_list[i] = random.randint(lower, upper)

    # postcondition 
    for i in range(length):
        assert a_list[i] >= lower, "The element "+str(i)+" has a value lower than the user's lower limit. The value is "+str(a_list[i])
        assert a_list[i] <= upper, "The element "+str(i)+" has a value higher than the user's upper limit. The value is "+str(a_list[i])

    return a_list

def table_time_shaker_sortII(filename:str, threshold:int, lower:int, upper:int) -> None:
    """ Creates lists of increasing power-of-2 length, until threshold,
    where elements are random integers within [lower,upper] interval. 
    For each list, it calls sum_of_digits_of_non_negatives and writes
    a line in the comma separated filename, with the length of the list,
    and the times needed to create and process it. If threshold <= 2, it
    does nothing.

    :pre: lower<=upper 
    :raises ValueError: if lower>upper
    """

    assert lower <= upper, ValueError("Value of Lower must be LOWER than value of upper")

    length = 2
    if length < threshold: # file will not be empty
        file = open(filename, "w")

        while length < threshold:
            # creates and sorts the lists like normal
            time_at_start = timeit.default_timer() 
            a_list = __create_list(length,lower, upper)
            time_after_create = timeit.default_timer() 
            time_to_create = time_after_create - time_at_start # total create time 
            shaker_sortII(a_list)
            time_after_sort = timeit.default_timer() 
            time_to_sort = time_after_sort - time_after_create # total sort time

            # sorts the sorted lists
            time_at_sort_again = timeit.default_timer()
            shaker_sortII(a_list)
            time_after_sort_again = timeit.default_timer() 
            time_to_sort_again = time_after_sort_again - time_at_sort_again # total sort again time

            # sorts reverse list
            a_list.reverse()
            time_at_sort_reverse = timeit.default_timer()
            shaker_sortII(a_list)
            time_after_sort_reverse = timeit.default_timer()
            time_to_sort_reverse = time_after_sort_reverse - time_at_sort_reverse # total sort reverse time

            file.write(str(length)+","+str(time_to_create)+","+str(time_to_sort)+","+str(time_to_sort_again)
            +","+str(time_to_sort_reverse)+"\n")
            length = length << 1 # bitwise operation to multiply by 2

        file.close()
        csv_plotting.plot_csv(filename,5)

def table_avg_shaker_sortII(filename:str, threshold:int, lower:int, upper:int) -> None:
    '''Creates 100 list of elements of random integers [lower, upper] in the interval. Then sorts 
    these 100 lists. The times it takes to create and sort these 100 lists is recorded. The lengths 
    of these lists start from 2 and increases by power-of-two until threshold. 

    :pre: lower<=upper 
    :raises ValueError: if lower>upper
    '''

    assert lower <= upper, ValueError("Value of Lower must be LOWER than value of upper")

    length = 2
    a_list = [0]*100 # initialising a_list for 100 lists 

    if length < threshold:
        file = open(filename, "w")

        while length < threshold:
            # creates 100 arrays
            time_at_start = timeit.default_timer()
            for i in range(100):
                a_list[i] = __create_list(length, lower, upper) # 100 arrays in one array
            time_after_create = timeit.default_timer()
            time_to_create = (time_after_create - time_at_start)/100 # averaging creating an array

            # sorts the 100 arrays
            for j in range(100):
                shaker_sortII(a_list[j])
            time_after_sum = timeit.default_timer()
            time_to_sum = (time_after_sum - time_after_create)/100 # averaging sorting an array

            file.write(str(length)+","+str(time_to_create)+","+str(time_to_sum)+"\n")
            length = length << 1 # bitwise operation to multiply by 2

        file.close()
        csv_plotting.plot_csv(filename,3)

            
if __name__ == '__main__':
    table_time_shaker_sortII("output_shaker_sortII.csv", 4200, 0, 10000)
    table_avg_shaker_sortII("output_avg_shaker_sortII.csv", 1200, 0, 10000)