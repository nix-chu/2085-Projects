from abc import ABC, abstractmethod 
from typing import Generic
from referential_array import ArrayR, T

class Stack(ABC, Generic[T]):
    def __init__(self) -> None:
        self.length = 0

    @abstractmethod
    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack."""
        pass

    @abstractmethod
    def pop(self) -> T:
        """ Pops an element from the top of the stack."""
        pass

    @abstractmethod
    def peek(self) -> T:
        """ Pops the element at the top of the stack."""
        pass

    def __len__(self) -> int:
        """ Returns the number of elements in the stack."""
        return self.length

    def is_empty(self) -> bool:
        """ True if the stack is empty. """
        return len(self) == 0

    @abstractmethod
    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed. """
        pass

    def clear(self):
        """ Clears all elements from the stack. """
        self.length = 0

class ArrayStack(Stack[T]):
    """ Implementation of a stack with arrays.
    
    Attributes:
         length (int): number of elements in the stack (inherited)
         array (ArrayR[T]): array storing the elements of the queue

    ArrayR cannot create empty arrays. So MIN_CAPCITY used to avoid this.
    """
    MIN_CAPACITY = 1 

    def __init__(self, max_capacity: int) -> None:
        """ Initialises the length and the array with the given capacity.
            If max_capacity is 0, the array is created with MIN_CAPACITY.
        """
        Stack.__init__(self)
        self.array = ArrayR(max(self.MIN_CAPACITY, max_capacity))
        
    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed.
        :complexity: O(1)
        """
        return len(self) == len(self.array)

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :pre: stack is not full
        :complexity: O(1)
        :raises Exception: if the stack is full
        """
        if self.is_full():
            raise Exception("Stack is full")
        self.array[len(self)] = item
        self.length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :pre: stack is not empty
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        self.length -= 1
        return self.array[self.length]

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :pre: stack is not empty
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.array[self.length-1]
 
    def __str__(self) -> str:
        """Computes a string from the stack items - top to bottom.
        :complexity: O(N) where N is the size of the stack
        """
        length = len(self)
        if length > 0:
            output = str(self.array[length-1])
            for i in range(length-2, -1, -1):
                output += "," + str(self.array[i])
        else:
            output = ""
        return output

class Node(Generic[T]):
    """ Implementation of a generic Node class

    Attributes:
         item (T): the data to be stored by the node
         link (Node[T]): pointer to the next node

    ArrayR cannot create empty arrays. So MIN_CAPCITY used to avoid this.
    """

    def __init__(self, item: T = None) -> None:
        self.item = item
        self.link = None

class LinkStack(Stack[T]):
    """ Implementation of a stack with linked nodes.

    Attributes:
         length (int): number of elements in the stack (inherited)
    """

    def __init__(self, _=None) -> None:
        Stack.__init__(self)
        self.top = None

    def clear(self) -> None:
        """" Resets the stack
        :complexity: O(1)
        """
        super().clear()
        self.top = None

    def is_empty(self) -> bool:
        """ Returns whether the stack is empty
        :complexity: O(1)
        """
        return self.top is None

    def is_full(self) -> bool:
        """ Returns whether the stack is full
        :complexity: O(1)
        """
        return False

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :complexity: O(1)
        """
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :pre: stack is not empty
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")

        item = self.top.item
        self.top = self.top.next
        self.length -= 1
        return item

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :pre: stack is not empty
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty(self):
            raise Exception("Stack is empty")
        return self.top.item
