from django.shortcuts import render
from django.views import generic
from .models import Book,Log_user,A_Logger,Author
# Create your views here.
def main_page(request):
	num_books = Book.objects.all().count()
	user_num= Log_user.objects.all().count()
	num_authors= Author.objects.all().count()
	ln_books= A_Logger.objects.filter(status__exact='Available').count()
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
	
def user_profile(request):

	return render(request, 'bookshelf/user_profile.html', context={})

class Books(generic.ListView):
    model = Book
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title='вге') # Get 5 books containing the title war
    '''template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location '''

class Authors(generic.ListView):
    model = Author
	

class Users(generic.ListView):
    model = Log_user




