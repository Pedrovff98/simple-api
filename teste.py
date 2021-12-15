class Animal:

    def comer(self):
        print('comeu')

    def descomer(self):
        print("PUMM")

    def viver(self):
        print("viver")


class Dog(Animal):

    def latir(self):
        print("auauau")


animal = Animal()
print(type(animal))
animal.comer()
animal.descomer()
animal.viver()

dog = Dog()
print(type(dog))
dog.comer()
dog.viver()
dog.descomer()
dog.latir()
