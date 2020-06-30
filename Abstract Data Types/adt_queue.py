from abc import ABC, abstractmethod 
from typing import TypeVar, Generic
from referential_array import ArrayR, T

class Queue(ABC, Generic[T]):
    """ Abstract class for a generic Queue. """
   
    def __init__(self) -> None:
        self.length = 0

    @abstractmethod
    def append(self,item:T) -> None:
        """ Adds an element to the rear of the queue."""
        pass

    @abstractmethod
    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front."""
        pass

    def __len__(self) -> int:
        """ Returns the number of elements in the queue."""
        return self.length

    def is_empty(self) -> bool:
        """ True if the queue is empty. """
        return len(self) == 0

    @abstractmethod
    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed. """
        pass

    def clear(self):
        """ Clears all elements from the queue. """
        self.length = 0

class CircularQueue(Queue[T]):
    """ Circular implementation of a queue with arrays.
    
    Attributes:
         length (int): number of elements in the stack (inherited)
         front (int): index of the element at the front of the queue
         rear (int): index of the first empty space at the oback of the queue
         array (ArrayR[T]): array storing the elements of the queue

    ArrayR cannot create empty arrays. So MIN_CAPCITY used to avoid this.
    """
    MIN_CAPACITY = 1 

    def __init__(self,max_capacity:int) -> None:
        Queue.__init__(self)
        self.front = 0
        self.rear = 0
        self.array = ArrayR(max(self.MIN_CAPACITY,max_capacity))


    def append(self, item: T) -> None:
        """ Adds an element to the rear of the queue.
        :pre: queue is not full
        :raises Exception: if the queueu is full
        """
        if self.is_full():
            raise Exception("Queue is full")

        self.array[self.rear] = item
        self.length += 1
        self.rear = (self.rear + 1) % len(self.array)

    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front.
        :pre: queue is not empty
        :raises Exception: if the queue is empty
        """
        if self.is_empty(): 
            raise Exception("Queue is empty")

        self.length -= 1
        item = self.array[self.front] 
        self.front = (self.front+1) % len(self.array)
        return item 

    def is_full(self) -> T:
        """ True if the queue is full and no element can be appended. """
        return len(self) == len(self.array)
 
    def clear(self) -> None:
        """ Clears all elements from the queue. """
        Queue.__init__(self)
        self.front = 0
        self.rear = 0
    
    def __str__(self) -> str:
        '''Prints a string from the queue items, from top to bottom'''
        index = self.front
        output = ""
        for _ in range(len(self)):
            output += str(self.array[index])
            index = (index + 1) % len(self.array)
        return output
        
