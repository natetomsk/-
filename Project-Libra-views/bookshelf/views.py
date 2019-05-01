from django.shortcuts import render
from django.views import generic
from .models import Book,Log_user,A_Logger,Author
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

import pickle

fil=''
queryset=Book.objects.order_by("title")
queryset=Book.objects.filter(title__icontains=fil)

# Create your views here.
def main_page(request):

	print("\n\n")
	book=Book.objects.all()
	a_logger=A_Logger.objects.all()
	#print(book, a_logger)
	for i in range(len(book)):
		for j in range(len(a_logger)):
			#print(book[i].title, "|", a_logger[j].book, str(book[i].title)==str(a_logger[j].book))
			if(book[i].title==a_logger[j].book):
				print(book[i])
	print("\n\n")


	num_books = Book.objects.all().count()
	user_num= Log_user.objects.all().count()
	num_authors= Author.objects.all().count()
	ln_books= A_Logger.objects.filter(status__exact='Reserved').count()
	#avail_books=A_Logger.objects.filter(status__exact ='On loan').count()
	av_book = num_books-ln_books
	context = {
		'book': num_books,
		'num_users': user_num,
		'book_onloan': ln_books,
		'book_av':av_book,
		'num_authors': num_authors
	}
	return render(request, 'bookshelf/index.html', context=context)


def book_list(request):
    print("ZZZ")
    if request.POST:
        #считывание размеров таблицы
        N = request.POST.get('N', None)
        fil = N
        print("NNN")
    return HttpResponseRedirect('./books/')

def user_profile(request):

	 return render(request, 'bookshelf/user_profile.html', context={})

class Books(generic.ListView):
    queryset = Book.objects.order_by('title')
    def get_context_data(self, **kwargs):
        logger=A_Logger.objects.filter(status='Reserved')
        context = {}
        book_list=list(self.queryset.values())
        
        logger=list(logger.values())
        logger_id_book=[log['book_id'] for log in logger]
        logger_id_borrower=[log['borrower_id'] for log in logger]
        for i in range(len(book_list)):
            author_ = model_to_dict(Author.objects.get(id=book_list[i]['author_id']))
            book_list[i].pop('author_id')
            book_list[i]['author_first_name']=author_['first_name']
            book_list[i]['author_last_name']=author_['last_name']
            if(book_list[i]['id'] in logger_id_book):
                book_list[i]['status']='Reserved'
                id_=logger_id_borrower[logger_id_book.index(book_list[i]['id'])]
                print("---", id_, book_list[i]['id'])
                reader_=model_to_dict(Log_user.objects.get(id=id_))
                print(reader_)
                book_list[i]['reader_first_name']=reader_['first_name']
                book_list[i]['reader_last_name']=reader_['last_name']
            else:
                book_list[i]['status']='Available'
                book_list[i]['reader_first_name']=''
                book_list[i]['reader_last_name']=''
        self.book_list=book_list
        context['book_list'] = book_list
        return context
	
    def post(self, request, *args, **kwargs):
        book_list=self.get_context_data(**kwargs)['book_list']
        fil=''
        if request.POST:
            #считывание размеров таблицы
            #фильтр
            fil = str(request.POST.get('N', None))
            S = str(request.POST.get('S', None))
            Obr=str(request.POST.get('Obr', None))
            Search=str(request.POST.get('Search', None))
            if(Obr==""):
                Obr="0"
            self.queryset=Book.objects.all()
            if(str(request.POST.get('name', None))!='Поиск'):
                fil=Search
            else:
                Search=fil
            i=0
            while i<len(book_list):
                if(all(fil.lower() not in str(title).lower() for title in book_list[i].values())):
                    del(book_list[i])
                else:
                    i+=1
            
            def sort_col(i):
                return i[pol]
            #сортировка
            if(S=='0'):
                pol='title'
                book_list.sort(key=sort_col)
            elif(S=='1'):
                pol='author_first_name'
                book_list.sort(key=sort_col)
                pol='author_last_name'
                book_list.sort(key=sort_col)
            elif(S=='2'):
                pol='status'
                book_list.sort(key=sort_col)
            elif(S=='3'):
                pol='reader_first_name'
                book_list.sort(key=sort_col)
                pol='reader_last_name'
                book_list.sort(key=sort_col)
            
            if(Obr==S):
                Obr='None'
                book_list=reversed(book_list)
            else:
                Obr=S
        
        context={
                'Search' : Search,
                'Obr' : Obr,
                'N' : fil,
                'book_list' : book_list
                }
        return render(request, 'bookshelf/book_list.html', context=context)
        #context_object_name = 'my_book_list'   # your own name for the list as a template variable
        #queryset = Book.objects.filter(title='вге') # Get 5 books containing the title war
        '''template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location '''

class Authors(generic.ListView):
    model = Author

class Users(generic.ListView):
    model = Log_user

class A_Loggers(generic.ListView):
    model = A_Logger

class Books_Reserved(generic.ListView):
    queryset = Book.objects.order_by('title')
    def get_context_data(self, **kwargs):
        logger=A_Logger.objects.filter(status='Reserved')
        context = {}
        book_list=list(self.queryset.values())
        
        logger=list(logger.values())
        logger_id_book=[log['book_id'] for log in logger]
        logger_id_borrower=[log['borrower_id'] for log in logger]
        i=0
        while i<len(book_list):
            author_ = model_to_dict(Author.objects.get(id=book_list[i]['author_id']))
            book_list[i].pop('author_id')
            book_list[i]['author_first_name']=author_['first_name']
            book_list[i]['author_last_name']=author_['last_name']
            if(book_list[i]['id'] in logger_id_book):
                book_list[i]['status']='Reserved'
                id_=logger_id_borrower[logger_id_book.index(book_list[i]['id'])]
                print("---", id_, book_list[i]['id'])
                reader_=model_to_dict(Log_user.objects.get(id=id_))
                print(reader_)
                book_list[i]['reader_first_name']=reader_['first_name']
                book_list[i]['reader_last_name']=reader_['last_name']
            else:
                del(book_list[i])
                continue
            i+=1
        self.book_list=book_list
        context['book_list'] = book_list
        return context
        
    def post(self, request, *args, **kwargs):
        book_list=self.get_context_data(**kwargs)['book_list']
        fil=''
        if request.POST:
            #считывание размеров таблицы
            #фильтр
            fil = str(request.POST.get('N', None))
            S = str(request.POST.get('S', None))
            Obr=str(request.POST.get('Obr', None))
            Search=str(request.POST.get('Search', None))
            if(Obr==""):
                Obr="0"
            self.queryset=Book.objects.all()
            if(str(request.POST.get('name', None))!='Поиск'):
                fil=Search
            else:
                Search=fil
            i=0
            while i<len(book_list):
                if(all(fil.lower() not in str(title).lower() for title in book_list[i].values())):
                    del(book_list[i])
                else:
                    i+=1
            
            def sort_col(i):
                return i[pol]
            #сортировка
            if(S=='0'):
                pol='title'
                book_list.sort(key=sort_col)
            elif(S=='1'):
                pol='author_first_name'
                book_list.sort(key=sort_col)
                pol='author_last_name'
                book_list.sort(key=sort_col)
            elif(S=='2'):
                pol='status'
                book_list.sort(key=sort_col)
            elif(S=='3'):
                pol='reader_first_name'
                book_list.sort(key=sort_col)
                pol='reader_last_name'
                book_list.sort(key=sort_col)
            
            if(Obr==S):
                Obr='None'
                book_list=reversed(book_list)
            else:
                Obr=S
        
        context={
                'Search' : Search,
                'Obr' : Obr,
                'N' : fil,
                'book_list' : book_list
                }
        return render(request, 'bookshelf/book_list.html', context=context)
	
class Books_Available(generic.ListView):
    queryset = Book.objects.order_by('title')
    def get_context_data(self, **kwargs):
        logger=A_Logger.objects.filter(status='Reserved')
        context = {}
        book_list=list(self.queryset.values())
        
        logger=list(logger.values())
        logger_id_book=[log['book_id'] for log in logger]
        logger_id_borrower=[log['borrower_id'] for log in logger]
        i=0
        while i<len(book_list):
            author_ = model_to_dict(Author.objects.get(id=book_list[i]['author_id']))
            book_list[i].pop('author_id')
            book_list[i]['author_first_name']=author_['first_name']
            book_list[i]['author_last_name']=author_['last_name']
            if(book_list[i]['id'] not in logger_id_book):
                book_list[i]['status']='Available'
                book_list[i]['reader_first_name']=''
                book_list[i]['reader_last_name']=''
            else:
                del(book_list[i])
                continue
            i+=1
        self.book_list=book_list
        context['book_list'] = book_list
        return context
        
    def post(self, request, *args, **kwargs):
        book_list=self.get_context_data(**kwargs)['book_list']
        fil=''
        if request.POST:
            #считывание размеров таблицы
            #фильтр
            fil = str(request.POST.get('N', None))
            S = str(request.POST.get('S', None))
            Obr=str(request.POST.get('Obr', None))
            Search=str(request.POST.get('Search', None))
            if(Obr==""):
                Obr="0"
            self.queryset=Book.objects.all()
            if(str(request.POST.get('name', None))!='Поиск'):
                fil=Search
            else:
                Search=fil
            i=0
            while i<len(book_list):
                if(all(fil.lower() not in str(title).lower() for title in book_list[i].values())):
                    del(book_list[i])
                else:
                    i+=1
            
            def sort_col(i):
                return i[pol]
            #сортировка
            if(S=='0'):
                pol='title'
                book_list.sort(key=sort_col)
            elif(S=='1'):
                pol='author_first_name'
                book_list.sort(key=sort_col)
                pol='author_last_name'
                book_list.sort(key=sort_col)
            elif(S=='2'):
                pol='status'
                book_list.sort(key=sort_col)
            elif(S=='3'):
                pol='reader_first_name'
                book_list.sort(key=sort_col)
                pol='reader_last_name'
                book_list.sort(key=sort_col)
            
            if(Obr==S):
                Obr='None'
                book_list=reversed(book_list)
            else:
                Obr=S
        
        context={
                'Search' : Search,
                'Obr' : Obr,
                'N' : fil,
                'book_list' : book_list
                }
        return render(request, 'bookshelf/book_list.html', context=context)


