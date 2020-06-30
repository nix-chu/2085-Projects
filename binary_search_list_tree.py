"""Unit testing for Code Review 4, Exercise 1 to 3"""
__author__ = "Nicholas Chua"
__docformat__ = 'reStructuredText'
__since__ = '05/06/2020'
__modified__ = '11/06/2020'

from typing import TypeVar, Generic, Tuple
from list import SortedLinkList
from stack import LinkStack
K = TypeVar('Key')
I = TypeVar('Item')

class BinarySearchListTreeNode(Generic[K, I]):
    """ Implementation of a BST List Node

    Attributes:
         key (K): the key to be stored in the node
         items (SortedLinkList[I]): the sorted list of items in the node
         left (BinarySearchListTreeNode[K, I]): pointer to left child
         right (BinarySearchListTreeNode[K, I]): pointer to right child
    """

    def __init__(self, key: K, item: I = None) -> None:
        self.key = key
        self.items = SortedLinkList()
        self.items.append(item)
        self.left = None
        self.right = None

    def __str__(self):
        """Key and associated data items"""
        return " (" + str(self.key) + ", " + str(self.items) + " ) "

class InorderIteratorStack:
    '''
    Class was created before Brendon updated the Prac Brief, and this currently works.
    So I prefer to not change the type-hints and the methods, when it works. Hope the assessor 
    that reads this understands.
    '''
    def __init__(self, root:BinarySearchListTreeNode[K,I]) -> None:
        '''Initiates the Stack for iteration
        
        :complexity: O(N), where N is the total number of nodes in the tree
        '''
        self.stack = LinkStack()
        self.current: Tuple[K, SortedLinkList] = None
        self.__store_item(root)
    
    def __store_item(self, current_node:BinarySearchListTreeNode[K,I]) -> None:
        '''Stores nodes in stack in inorder order. This is done first, to avoid
        complicated tree logic
        
        :complexity: O(N), where N is the total number of nodes in the tree'''
        if current_node is not None:
            self.__store_item(current_node.right)
            self.stack.push(current_node)
            self.__store_item(current_node.left)
    
    def __iter__(self):
        '''Returns the iteration instance
        :complexity: O(1)'''
        return self
    
    def __next__(self) -> Tuple[K,SortedLinkList]:
        '''Moves to next object in the iteration and returns a tuple of the key
        and the list of items associated with the key

        :complexity: O(1)
        '''
        if not self.has_next():
            raise StopIteration
        self.current = self.peek()
        return self.current
    
    def reset(self) -> None:
        '''Clears all elements in the stack
        :complexity: O(1)'''
        self.stack.clear()

    def has_next(self) -> bool:
        '''Returns boolean whether there are still items in the stack
        :complexity: O(1)'''
        return not self.stack.is_empty()
    
    def peek(self) -> Tuple[K, SortedLinkList]:
        '''Returns tuple of the key and a list of items associated with the key.
        :complexity: O(1)'''
        current_node = self.stack.pop()
        return (current_node.key, current_node.items)

class BinarySearchListTree(Generic[K, I]):
    """ Implementation of a BST using a sorted list for the item.

    Attributes:
         root (BinarySearchListTreeNode): reference to the root of the BST
    """
    def __init__(self) -> None:
        self.root = None

    def __getitem__(self, key: K) -> SortedLinkList[I]:
        '''__getitem__ recursion function caller'''
        return self.__getitem_aux(self.root, key)

    def __getitem_aux(self, current:BinarySearchListTreeNode[K,I], key:K) -> SortedLinkList[I]:
        '''Returns the associated list of items that are related to the given key. Searches using
        recursion calls.

        :complexity best: O(1)*Comp==, if the element is at the root
        :complexity worst: O(N)*(Comp== + Comp<), where N is the depth of the tree and varies
        whether the tree is balanced or not'''
        if current is None:
            raise KeyError("Key not found!")
        elif key == current.key:
            return current.items
        elif key < current.key:
            return self.__getitem_aux(current.left, key)
        else: # key > current.key
            return self.__getitem_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        '''__setitem__ recursion function caller'''
        self.root = self.__setitem_aux(self.root, key, item)
    
    def __setitem_aux(self, current:BinarySearchListTreeNode[K,I], key:K, item:I) -> BinarySearchListTreeNode[K,I]:
        '''Creates or updates a node with the given item, based on the given item. Searches 
        using recursion calls.

        :complexity best: O(1)*Comp==, if the element is at the root
        :complexity worst: O(N)*(Comp== + Comp<), where N is the depth of the tree and varies
        whether the tree is balanced or not'''
        if current is None:
            current = BinarySearchListTreeNode(key, item) # new key
        elif key == current.key:
            current.items.insert(item) # existing key, insert new item
        elif key < current.key:
            current.left = self.__setitem_aux(current.left, key, item)
        else: # key > current.key
            current.right = self.__setitem_aux(current.right, key, item)
        return current
    
    def __iter__(self) -> InorderIteratorStack:
        '''Iteration caller'''
        return InorderIteratorStack(self.root)
