# ПР 8

"""
x = input('Имя: ')
y = input('Сколько лет: ')
z = input('Год рождения: ')

print(f'Здравствуйте {x} {y} - вам {z} лет')
"""

# ПР 9

"""
x = int(input('Введите четырехзначный год: '))
if x % 4 == 0 and x % 100 != 0:
    print('Год високосный')
elif x % 400 == 0:
    print('Год високосный')
else:
    print('Год не високосный(')
"""

# ПР 10

a = []

for i in range(1, 11):
    k = []
    for j in range(1, 11):
        k.append(i * j)
    a.append(k)

for k in a:
    for num in k:
        print(f"{num:3}", end=" ")
    print()