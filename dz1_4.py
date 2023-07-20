enter = input('введите символы: ')

def palendrom(enter):
    if enter == enter[::-1]:
        return True
    return False

print(palendrom(enter))