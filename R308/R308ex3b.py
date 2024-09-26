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
            return
        
        if other_list.head is None:
            return

        # Pointeur pour la liste fusionnée
        dummy = Node(0)
        tail = dummy

        current1 = self.head
        current2 = other_list.head

        while current1 is not None and current2 is not None:
            if current1.data < current2.data:
                tail.next = current1
                current1 = current1.next
            else:
                tail.next = current2
                current2 = current2.next
            tail = tail.next

        # Ajouter les éléments restants
        if current1 is not None:
            tail.next = current1
        else:
            tail.next = current2

        # Mettre à jour la tête de la liste actuelle
        self.head = dummy.next

    
    def get_head(self, n):
        result = []
        current = self.head
        count = 0
        while current is not None and count < n:
            result.append(current.data)
            current = current.next
            count += 1
        return result
    
    def get_tail(self, n):
        result = []
        current = self.head
        length = 0
        # Calculer la longueur de la liste
        while current is not None:
            length += 1
            current = current.next
        # Trouver le début des n derniers éléments
        if n > length:
            n = length  # On ne peut pas demander plus que la taille de la liste
        start_index = length - n
        current = self.head
        for _ in range(start_index):
            current = current.next
        # Récupérer les n derniers éléments
        while current is not None:
            result.append(current.data)
            current = current.next
        return result


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

print("Les N premières valeurs de la liste sont:", myLinkedList.get_head(3))
print("Les N dernières valeurs de la liste sont:", myLinkedList.get_tail(3))

myLinkedList1 = LinkedList()
myLinkedList2 = LinkedList()

myLinkedList1.addInTail(10)
myLinkedList1.addInTail(20)
myLinkedList1.addInTail(30)

myLinkedList2.addInTail(15)
myLinkedList2.addInTail(25)
myLinkedList2.addInTail(35)

print("Liste 1:")
myLinkedList1.printListRecRev()
print("Liste 2:")
myLinkedList2.printListRecRev()

myLinkedList1.merge(myLinkedList2)
print("Liste fusionnée:")
myLinkedList1.printListRecRev()
