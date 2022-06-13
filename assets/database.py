
import os
import requests
from tabulate import tabulate
from peewee import *
os.system('color')

__all__ = ["db",'Catalog','Abonements','DB']

db = SqliteDatabase('data.db')
class Mdl(Model):
    class Meta:
        database = db

class Catalog(Mdl):
    ISBN = TextField()
    Using_by = TextField()


class Abonements(Mdl):
    owner = TextField()
    
class DB():
    def clear_screen():
        os.system('cls')
    def help():
        print("""
Список доступных команд:
    help - возвращает этот список.
    clear - очистка экрана.
    get_cat - Возвращает таблицу, содержащую все книги в каталоге.
    get_abon - Возвращает таблицу зарегестрированых абонементов.
    add_book - Команда добавляет в каталог новую книгу.
    rem_book - Команда удаляет книгу из каталога.
    give_book - Команда связывает книгу с абонементом.
    ret_book - Развязывает книгу с абонементом (если была ранее привязана).
    add_abon - добавляет новый абонемент.
    exit - выход из приложения.
    about - об авторе приложения.
        """)
    def get_catalog():
        table = [['id','ISBN','Авторы','Дата публикации','Название','Текущий владелец']]
        for book in Catalog.select():
            try:
                data=requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{book.ISBN}").json()['items'][0]['volumeInfo']
            except KeyError:
                continue
            table.append([book.id,book.ISBN,", ".join(data['authors']),data['publishedDate'],data['title'],book.Using_by])
        print(tabulate(table,tablefmt="rst"))
    
    def get_abonements():
        table=[['Номер абонемента','Имя Фамилия владельца']]
        for abon in Abonements.select():
            table.append([abon.id,abon.owner])
        print(tabulate(table,tablefmt="rst"))
    def add_book():
        ISBN=input('Введите ISBN книги>')
        return Catalog.create(ISBN=ISBN,Using_by=0).id

    def remove_book():
        id=int(input('Введите id книги в каталоге>'))
        if Catalog.select().where(Catalog.id == id).get_or_none() is None:
            print('Книги с этим id не существует')
        Catalog.delete_by_id(int(id))
        return 0
    def add_abon():
            owner=input('Введите Имя и Фамилию владельца>')
            return Abonements.create(owner=owner).id
    def give_book():
        id=int(input('Введите id книги в каталоге>'))
        ab=int(input('Введите id абонемента>'))
        if Abonements.select().where(Abonements.id == ab).get_or_none() is None:
            print('Данного абонемента не существует')
            return 1
        elif Catalog.select().where(Catalog.id == id).get_or_none() is None:
            print('Книги с таким id не существует')
            return 2
        elif Catalog.select().where((Catalog.id == id) & (Catalog.Using_by == ab)).get_or_none() is not None:
            print("Эта книга уже выдана на этот абонемент")
        elif Catalog.select().where((Catalog.id == id) & (Catalog.Using_by == 0)).get_or_none() is not None:
            d=Catalog.select().where(Catalog.id == id).get()
            d.Using_by = ab
            d.save()
            return 0
        else:
            print('Книга занята')
        
    def return_book():
        id=input('Введите id книги>')
        ab=input('Введите id абонемента>')
        if Catalog.select().where(Catalog.id == id).get_or_none() is None:
            print('Книги с этим id не существует')
            return 1
        elif Catalog.select().where(Catalog.id == id).get_or_none() is None:
            print('Книги с таким id не существует')
            return 2
        elif Catalog.select().where((Catalog.id == id) & (Catalog.Using_by == ab)).get_or_none() is None:
            print("Эта книга не была выдана на этот абонемент")
            return 3
        else:
            d=Catalog.select().where((Catalog.id == id) & (Catalog.Using_by == ab)).get()
            d.Using_by = '0'
            
            d.save()
            return 0
    def about():
        print("""
Made with \x1b[31;1m♥\x1b[0m by Tau
\x1b[38;2;0;204;193m ██    ██    ██
████ ██████ ████
███ ████████ ███
██  ████████  ██
██ ████\x1b[38;2;254;123;219m██\x1b[38;2;0;204;193m████ ██
 █ ███\x1b[38;2;254;123;219m████\x1b[38;2;0;204;193m███ █
 █ █\x1b[38;2;254;123;219m█\x1b[38;2;0;204;193m█\x1b[38;2;254;123;219m████\x1b[38;2;0;204;193m█\x1b[38;2;254;123;219m█\x1b[38;2;0;204;193m█ █
 █ █\x1b[38;2;254;123;219m████████\x1b[38;2;0;204;193m█ █
 █  █\x1b[38;2;254;123;219m██████\x1b[38;2;0;204;193m█  █
     ██████\x1b[0m
Github: https://github.com/Taukurade
VK: https://vk.com/taukurade
Discord: 4R14 M41D3N#2478
eSUSU: https://edu.susu.ru/user/profile.php?id=124674
""")