from django.test import TestCase
from datetime import datetime
from bookshelf.models import Author, Book, A_Logger, Log_user

class AuthorModelTest(TestCase):#тест таблицы Author из БД
    @classmethod
    def setUpTestData(cls):#создание строки в таблице Author БД
        Author.objects.create(first_name='Имя', last_name='Фамилия', middle_name='Отчество',
            pic='Ссылка на картинку', description='Описание')
    
    def test_read(self):#проверка корректности созаднной строки в таблице Author БД
        author=Author.objects.get(id=1)
        self.assertEquals(author.first_name, 'Имя')
        self.assertEquals(author.last_name, 'Фамилия')
        self.assertEquals(author.middle_name, 'Отчество')
        self.assertEquals(author.pic, 'Ссылка на картинку')
        self.assertEquals(author.description, 'Описание')
    
    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')
    
    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)
    
    def test_error(self):#Ошибка если превысить максимальную допустимую длину строкового поля (для лабораторной)
        try:
            first_name=str(list[range(150)])
            Author.objects.create(first_name=first_name)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

class LibraryDatabaseModelTest(TestCase):#тест на взятие и сдачу книги читателем
    @classmethod
    def setUpTestData(cls):#заполнение БД
        Author.objects.create(first_name='Имя', last_name='Фамилия', middle_name='Отчество',
            pic='Ссылка на картинку', description='Описание')
        Book.objects.create(number_code='Код 1', title='Название', author=Author.objects.get(id=1),
            pic='Ссылка на картинку', description='Описание')
        Log_user.objects.create(number_code = 'Код 2', first_name = 'Имя', last_name = 'Фамилия',
            middle_name = 'Отчество', number_phone = 'Номер телефона', pic = 'Ссылка на картинку',
            description = 'Описание')
        A_Logger.objects.create(book = Book.objects.get(id=1), borrower = Log_user.objects.get(id=1),
            status = 'Reserved', start_date = datetime.now())
    
    def test_1(self):#Сдача книги
        id1=Book.objects.get(number_code='Код 1')
        id2=Log_user.objects.get(number_code='Код 2')
        log=A_Logger.objects.get(book=id1, borrower=id2, status='Reserved')
        log.status='Available'
        log.finish_date=datetime.now()
        log.save()
        A_Logger.objects.get(book=id1, borrower=id2, status='Available')
    
    def test_2(self):#Выдача книги
        id1=Book.objects.get(number_code='Код 1')
        id2=Log_user.objects.get(number_code='Код 2')
        date=datetime.now()
        A_Logger.objects.create(book = Book.objects.get(id=1), borrower = Log_user.objects.get(id=1),
                status = 'Reserved')
        A_Logger.objects.get(id=2)
