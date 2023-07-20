enter = input('введите символы: ')

def palendrom(enter):
    if enter == enter[::-1]:
        return True
    return False

print(palendrom(enter))
#теперь надо написать как я это сделал в коммите