from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class SortedList(ABC, Generic[T]):
    """ Abstract class for a generic List. """

    def __init__(self) -> None:
        """ Initialises the length of an exmpty list to be 0. """
        self.length = 0

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        """ Returns the value of the element at position index
        :pre: index is 0 <= index < len(self)
        """
        pass

    def __len__(self) -> int:
        """ Returns the length of the list
        :complexity: O(1) 
        """
        return self.length

    def append(self, item: T) -> None:
        """Adds the item to the end of the list"""
        self.insert(item)

    @abstractmethod
    def is_full(self) -> bool:
        """ Returns True iff the list is full
        """
        pass

    def is_empty(self) -> bool:
        """ Returns True iff the list is empty
        :complexity: O(1) 
        """
        return len(self) == 0

    def clear(self):
        """ Sets the list back to empty
        :complexity: O(1) 
        """
        self.length = 0

    @abstractmethod
    def insert(self, item: T) -> None:
        """ Inserts item into the list at the correct position"""
        pass

    @abstractmethod
    def delete_at_index(self, index: int) -> T:
        """Moved self[j+1] to self[j] if j>index & returns old self[index]
        :pre: index is 0 <= index < len(self)
        """
        pass

    @abstractmethod
    def index(self, item: T) -> int:
        """ Returns the position of the first occurrence of item
        :raises ValueError: if item not in the list
        """
        pass

    def remove(self, item: T) -> None:
        """ Removes the first occurrence of the item from the list
        :raises ValueError: if item not in the list
        :see: #index(item: T) and #delete_at_index(index: int)
        """
        index = self.index(item)
        self.delete_at_index(index)

    def __str__(self) -> str:
        """ Converts the list into a string, first to last
        :complexity: O(len(self) * M), M is the size of biggest item
        """
        result = "["
        for i in range(len(self)):
            if i > 0:
                result += ', '
            result += str(self[i])
        result += ']'
        return result

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

class LinkListIterator(Generic[T]):
    """Implementation of a linked list iterator"""
    def __init__(self, node: Node[T]) -> None:
        """Starts the iterator at node (normally root)"""
        self.current = node

    def __iter__(self) -> 'LinkListIterator':
        return self

    def __next__(self) -> T:
        """ Gets the next node in the linked list"""
        if self.current is not None:
            item = self.current.item
            self.current = self.current.link
            return item
        else:
            raise StopIteration

class SortedLinkList(SortedList[T]):
    """ Implementation of a generic sorted list with linked nodes.
    
    Attributes:
         length (int): number of elements in the list (inherited)
         head (Node[T]): node at the head of the list
    """
    def __init__(self) -> None:
        """ Initialises self.length by calling its parent and 
        self.head as None, since the list is initially empty
        :complexity: O(1)
        """        
        SortedList.__init__(self)
        self.head = None

    def __getitem__(self, index: int) -> T:
        """ Returns the value of the element at position index
        :see: #__get_node_at_index(index)
        """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index.item

    def __iter__(self) -> LinkListIterator[T]:
        """ Computes and returns an iterator for the current list
        :complexity: O(1)
        """
        return LinkListIterator(self.head)

    def __contains__(self, item: T) -> bool:
        """ Checks whether the item is in the linked list
        :see: #__get_node_at_index(index)
        """
        for list_item in self:
            if list_item == item:
                return True

        return False

    def is_full(self):
        """ Returns true if the list is full
        :complexity: O(1)
        """
        return False

    def __get_node_at_index(self, index: int) -> Node[T]:
        """ Returns the node in the list at position index
        :complexity: O(index)
        :pre: index is 0 <= index < len(self)
        """
        if 0 <= index and index < len(self):
            current = self.head
            for i in range(index):
                current = current.link
            return current
        else:
            raise ValueError("Index out of bounds")
            
    def insert(self, item: T) -> None:
        """
        :complexity best: O(1) inserting at the beginning of the list
        :complexity worst: O(N) where N is the length of the list (adding at the end)
        """
        if item in self:
            return # prevents duplicates

        new_node = Node(item)

        previous = None
        current = self.head
        index = 0
        # Find the correct position to insert
        while current is not None and current.item < item:
            previous = current
            current = current.link
            index += 1

        # Insert at the start
        if previous is None:
            new_node.link = self.head
            self.head = new_node
        # Insert in the middle
        else:
            new_node.link = previous.link
            previous.link = new_node
        self.length += 1

    def index(self, item: T) -> int:
        """ Returns the position of the first occurrence of item
        :raises ValueError: if item not in the list
        :complexity: O(Comp==) if item is first; Comp== is the BigO of ==
                     O(len(self)*Comp==) if item is last
        """
        current = self.head
        index = 0
        while current is not None and current.item != item:
            current = current.link
            index += 1
        if current is None:
            raise ValueError("Item is not in list")
        else:
            return index

    def delete_at_index(self, index: int) -> T:
        """ Moves self[j+1] to self[j] if j>index & returns old self[index]
        :pre: index is 0 <= index < len(self), checked by __get_node_at_index
        :complexity: O(index)
        """
        try:
            previous_node = self.__get_node_at_index(index-1)
        except ValueError as e:
            if self.is_empty(): 
                raise ValueError("List is empty")
            elif index == 0:
                item = self.head.items
                self.head = self.head.link
            else:
                raise e
        else:
            item = previous_node.link.items
            previous_node.link = previous_node.link.link
        self.length -= 1
        return item

    def clear(self):
        """ Overrides the parent to set the head to None 
        :complexity: O(1) 
        """
        SortedList.clear(self)
        self.head = None
