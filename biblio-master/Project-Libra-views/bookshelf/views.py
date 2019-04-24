from django.shortcuts import render
from django.views import generic
from .models import Book,Log_user,A_Logger,Author
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

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
    model = Book
    queryset = Book.objects.order_by('title')
    name=''
    '''def get_queryset(self):
         self.publisher = get_object_or_404(Author, first_name=self.name)
         return Book.objects.filter(author=self.publisher)'''
    def post(self, request, *args, **kwargs):
        fil=''
        if request.POST:
            #считывание размеров таблицы
            #фильтр
            fil = str(request.POST.get('N', None))
            S = str(request.POST.get('S', None))
            Obr=str(request.POST.get('Obr', None))
            if(Obr==""):
                Obr="0"
            print("\n\n\n", S, "-", Obr, "\n\n\n")
            self.model = Book
            self.queryset=Book.objects.all()
            if(str(request.POST.get('name', None))=='Поиск'):
                self.queryset=self.queryset.filter(title__icontains=fil)
            
            #сортировка
            if(S=='0'):
                self.queryset=self.queryset.order_by('title')
            elif(S=='1'):
                self.queryset=self.queryset.order_by('author__last_name')
            
            if(Obr==S):
                Obr='None'
                self.queryset=reversed(self.queryset)
            else:
                Obr=S
        
        context={
                'Obr' : Obr,
                'N' : fil,
                'book_list' : self.queryset
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
    model = Book
    def get_queryset(self):
        self.publisher = get_object_or_404(A_Logger, status='Reserved')
        return Book.objects.filter(a_logger=self.publisher)
	
class Books_Available(generic.ListView):
    model = Book
    def get_queryset(self):
        self.publisher = get_object_or_404(A_Logger, status='Available')
        return Book.objects.filter(a_logger=self.publisher)


