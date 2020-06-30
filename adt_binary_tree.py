from typing import TypeVar, Generic, Callable
from stack import ArrayStack

K = TypeVar('Key')
I = TypeVar('Item')
T = TypeVar('T') # for the iterator

class BinaryTreeNode(Generic[K,I]):
    def __init__(self, key:K, item:I) -> None:
        self.key = key
        self.item = item
        self.left = None
        self.right = None
    
    def __str__(self):
        return "("+str(self.key)+", "+str(self.item)+")"

class BinaryTree(Generic[K,I]):
    def __init__(self) -> None:
        self.root = None
    
    def is_empty(self) -> bool:
        return self.root is None

    def __len__(self) -> int:
        return self.len_aux(self.root)
    
    def len_aux(self, current:BinaryTreeNode[K,I]) -> int:
        if current is None:
            return 0
        else:
            return 1 + self.len_aux(current.left) + self.len_aux(current.right)

    def __contains__(self, key:K) -> bool:
        return self.contains_aux(self.root, key)
    
    def contains_aux(self, current:BinaryTreeNode[K,I], key:K) -> bool:
        if current is None:
            return False
        elif key < current.key:
            return self.contains_aux(current.left, key)
        elif key > current.key:
            return self.contains_aux(current.right, key)
        else:
            return True # key found
    
    def __getitem__(self, key:K) -> BinaryTreeNode:
        return self.getitem_aux(self.root, key)

    def getitem_aux(self, current:BinaryTreeNode[K,I], key:K) -> I:
        if current is None:
            raise KeyError(key)
        elif key < current.key:
            return self.contains_aux(current.left, key)
        elif key > current.key:
            return self.contains_aux(current.right, key)
        else:
            return current.item
    
    def __setitem__(self, key:K, item:I) -> None:
        self.root = self.insert_aux(self.root, key, item)
    
    def setitem_aux(self, current:BinaryTreeNode[K,I], key:K, item:I) -> BinaryTreeNode:
        if current is None:
            current = BinarySearchNode(key, item) # creates the new node
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else: # key == current.key
            current.item = item
        return current
        
    def insert(self, key:K, item:I=None) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current:BinaryTreeNode[K,I], key:K, item:I) -> BinaryTreeNode:
        if current is None:
            current = BinaryTreeNode(key, item) # creates the new node
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else: # key == current.key
            raise ValueError("Inserting duplicate item")
        return current

    def delete(self, key:K) -> None:
        self.root = self.delete_aux(self, key)
    
    def delete_aux(self, current:BinaryTreeNode[K,I], key:K, item:I) -> BinaryTreeNode:
        if current is None:
            raise ValueError("Key doesn't exist")
        elif key < current.key:
            current.left = self.delete_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key, item)
        else: # key == current.key
            return None # delete node
        return current
    
    def __iter__(self):
        return PreorderIteratorStack(self.root)

class PreorderIteratorStack(Generic[T]):
    def __init__(self, root:BinaryTreeNode[K,I]) -> None:
        self.stack = ArrayStack()
        self.stack.push(root)
    
    def __iter__(self):
        return self
    
    def __next__(self) -> T:
        if self.stack.is_empty():
            raise StopIteration
        current = self.stack.pop()
        if current.right is not None:
            self.stack.push(current.right)
        if current.left is not None:
            self.stack.push(current.left)
        return current.item
    
mytree = BinaryTree()
mytree.insert(4, "+")
mytree.insert(2, "/")
mytree.insert(1, "1")
mytree.insert(3, "3")
mytree.insert(8, "/")
mytree.insert(6, "*")
mytree.insert(5, "6")
mytree.insert(7, "7")
mytree.insert(9, "4")

for item in mytree:
    print(item)