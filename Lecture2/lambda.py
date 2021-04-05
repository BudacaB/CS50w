people = [
    {"name": "Harry", "house": "Gryff"},
    {"name": "Cho", "house": "Raven"},
    {"name": "Draco", "house": "Slyther"},
]

# def f(person):
#     return person["name"]

people.sort(key=lambda person: person["name"])

print(people)