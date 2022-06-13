
from assets.database import *


#Инициализация приложения
db.connect()
db.create_tables([Catalog,Abonements])


commands={
    'clear':DB.clear_screen,
    'get_cat':DB.get_catalog,
    'get_abon':DB.get_abonements,
    'add_book':DB.add_book,
    'rem_book':DB.remove_book,
    'give_book':DB.give_book,
    'ret_book':DB.return_book,
    'exit':exit,
    'help':DB.help,
    'about':DB.about,
    'add_abon':DB.add_abon,
}


def loop():
    try:
        cmd=input('>')
    except:
        exit()
    if cmd not in commands.keys():
        print('Неизвестная команда, для помощи пропишите help')
    else:
        commands[cmd]()
    loop()
loop()