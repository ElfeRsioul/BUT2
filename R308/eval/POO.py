class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Figure: 
    def __init__(self, coin, longueur, largeur):
        self.coin = coin
        self.longueur = longueur
        self.largeur = largeur

    def surface(self, ratio): 
        raise NotImplementedError("Doit être mis par les sous-classes")

class Rectangle(Figure): 
    def __init__(self, coin, longueur, largeur):
        super().__init__(coin, longueur, largeur)

    def surface(self, ratio): 
        return self.longueur * self.largeur * ratio

class Cercle(Figure): 
    def __init__(self, centre, rayon):
        super().__init__(centre, rayon, rayon) 

    def surface(self, ratio): 
        return 2 * 3.14 * self.longueur * ratio

class Dessin:
    def __init__(self):
        self.refFigure = []

    def ajouter(self, refFigure, ratio):
        self.refFigure.append({"figure": refFigure, "ratio": ratio})

    def surfaceTotale(self):
        total_surface = 0
        for figure in self.refFigure:
            fig = figure["figure"]
            ratio = figure["ratio"]
            total_surface += fig.surface(ratio)
        return total_surface

# Programme principal #

coin = Point(1, 2)
rectangle = Rectangle(coin, 5, 3)
print("La surface du rectangle choisi est de: ", rectangle.surface(1)) # Print classe rectangle

dessin = Dessin()
dessin.ajouter(Rectangle(Point(0, 0), 10, 5), 1.5) # Création d'un rectangle de 10*5 et d'un ratio de 1.5
dessin.ajouter(Rectangle(Point(20,0), 5, 11), 2.0) # Création d'un rectangle de 5*11 et d'un ratio de 2
dessin.ajouter(Cercle(Point(10, 0), 3), 2.0)  # Création d'un cercle de rayon 3 et d'un ratio de 2
dessin.ajouter(Cercle(Point(15,0), 2), 1.5) # Création d'un cercle de rayon 2 et d'un ratio de 1.5
print("La surface totale des figures dans le dessins est de: ", dessin.surfaceTotale()) #Print classe figure avec 2 cercles et 2 rectangles
