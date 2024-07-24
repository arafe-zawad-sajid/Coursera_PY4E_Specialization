# 14.1
class PartyAnimal:
    x = 0
    name = ''

    def __init__(self, n):
        self.name = n
        print(self.name, 'constructed', self.x)

    def __del__(self):
        print(self.name, 'destroyed', self.x)

    def party(self):
        self.x += 1
        print(self.name, 'party()', self.x)

an = PartyAnimal('Sami')
an.party()
an.party()
an.party()
PartyAnimal.party(an)
# print(type(an))
# print(dir(an))
print()

# 14.3
print(an)  # prints: memory address
an = 42  # prints: Sami destructed 4
print(an)  # prints: 42
a = PartyAnimal('Rabid')
a.party()
b = PartyAnimal('Sajid')
b.party()
b.party()
a = b  # prints: Rabid destructed 1 and replaced with 'b'
a.party()
b.party()
print()

# 14.4
class FootballFan(PartyAnimal):  # FootballFan extends (PartyAnimal)
    points = 0

    def touchdown(self):
        self.points += 7
        self.party()
        print(self.name, "touchdown()", self.points)

s = PartyAnimal('Sally')
s.party()

j = FootballFan('Jim')
j.party()
j.touchdown()
print()

k = FootballFan(s)
k.party()
k.touchdown()
print()
m = FootballFan(j)
m.party()
m.touchdown()
print()
