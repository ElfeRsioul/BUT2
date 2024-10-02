class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

    def printNode(self):
        print(self.data, end= " ")
        if self.next is not None:
            self.next.printNode()

class LinkedList:

    def __init__(self):
        self.head = None

    def printListRecRev(self): # Fonction print
        if self.head is not None:
            self.head.printNode()
        print()

    def unePasse(self):
        if self.head is None or self.head.next is None:
            return
        current = self.head
        while current.next is not None:
            if current.data > current.next.data:
                # Permutation des données
                current.data, current.next.data = current.next.data, current.data
            current = current.next

    # def tri(self): #Foonction tri

myLinkedList = LinkedList()
myNode1 = Node(3)
myNode2 = Node(1)
myNode3 = Node(7)
myNode4 = Node(8)
myNode5 = Node(6)
myNode6 = Node(9)
myLinkedList.head = myNode1
myNode1.next = myNode2
myNode2.next = myNode3
myNode3.next = myNode4
myNode4.next = myNode5
myNode5.next = myNode6

print("Les éléments de la liste sont: ")
myLinkedList.printListRecRev()

myLinkedList.unePasse()
print("Les éléments de la liste après la fontion unePasse: ")
myLinkedList.printListRecRev()
