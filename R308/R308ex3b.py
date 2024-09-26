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

    def printListRecRev(self):
        if self.head is not None:
            self.head.printNode()
        print()

    def addInTail(self, data):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = newNode

    
    def addSorted(self, data):
        newNode = Node(data)
        if self.head is None or data < self.head.data:
            newNode.next = self.head
            self.head = newNode
        else:
            current = self.head
            while current.next is not None and data > current.next.data:
                current = current.next
            newNode.next = current.next
            current.next = newNode

    def remove(self, value):
        current = self.head
        previous = None

        while current is not None:
            if current.data == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next

    def merge(self, other_list):

        if self.head is None:
            self.head = other_list.head
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = other_list.head
            other_list.head = None

        current = self.head
        previous = None

        while current is not None:
            next_node = current.next
            while next_node is not None and next_node.data < current.data:
                temp = next_node.next
                next_node.next = current
                current.next = temp
                if previous is not None:
                    previous.next = next_node
                else:
                    self.head = next_node
                previous = next_node
            previous = current
            current = current.next



myLinkedList = LinkedList()
myNode1 = Node(10)
myNode2 = Node(20)
myNode3 = Node(30)
myNode4 = Node(40)
myLinkedList.head = myNode1
myNode1.next = myNode2
myNode2.next = myNode3
myNode3.next = myNode4

print("Les éléments dans la liste sont:")
myLinkedList.printListRecRev()

myLinkedList.addInTail(50)
print("Les éléments dans la liste apres avoir ajouté 50 sont:")
myLinkedList.printListRecRev()

myLinkedList.addSorted(25)
print("Les éléments dans la liste apres avoir ajouté 25 sont:")
myLinkedList.printListRecRev()

myLinkedList.remove(25)
print("Les éléments dans la liste apres avoir supprimé 25 sont:")
myLinkedList.printListRecRev()

list1 = LinkedList()
list1.addSorted(10)
list1.addSorted(20)
list1.addSorted(30)

list2 = LinkedList()
list2.addSorted(15)
list2.addSorted(25)
list2.addSorted(35)

list1.merge(list2)
print("Les éléments dans la liste après avoir fusionné sont:")
list1.printListRecRev()
