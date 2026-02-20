class Mother:
    def speak(self):
        return "Hello from Mom!"

class Father:
    def work(self):
        return "Dad is working hard!"

class Child(Mother, Father):
    pass

my_child = Child()

print(my_child.speak())
print(my_child.work())