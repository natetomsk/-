from datetime import date

from django.db import models


# Create your models here.
class Book(models.Model):#книга
    number_code=models.CharField(max_length=12)#код книги
    title=models.CharField(max_length=100)#название/загаловок
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)#автор книги, ссылка
    def is_upperclass(self):
        return '{0}'.format(self.language)
    Edition=models.IntegerField()
    def __str__(self):
        return self.title



class Author(models.Model):#автор книги
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    def __str__(self):
        return '{0} {1}'.format(self.first_name , self.last_name)
        
class A_Logger(models.Model):#запись о выдаче книги
    book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)#книга, ссылка
    borrower = models.ForeignKey('Log_user' , on_delete=models.SET_NULL, null=True, blank=True)#ссылка на пользователя
    
    LOAN_STATUS = (
        ('On loan', 'On loan'),#не в наличии
        ('Available', 'Available'),#имеется в наличии
        ('Reserved', 'Reserved'),#зарезервирована
    )#типы записи

    status = models.CharField(
        max_length=10,
        choices=LOAN_STATUS,
        blank=True,
        default='Available',
        help_text='Book availability')#тип записи
    
    def __str__(self):
        """String for representing the Model object."""
        return '({0}) and {1}'.format(self.borrower,self.status)       
		
class Log_user(models.Model):#пользователь
    first_name=models.CharField(max_length=100)#имя
    last_name=models.CharField(max_length=100)#фамилия
    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1}'.format(self.first_name,self.last_name) 


