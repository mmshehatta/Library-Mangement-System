from django.shortcuts import redirect, render , get_object_or_404
from .models import *
from .forms import BookForm , GenreForm
from django.contrib import messages
# Create your views here
#********************* index view************
def index(request):
    if request.method == "POST":
        form = BookForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "Book Added Successfully !")

        cat_form = GenreForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request , 'Genre Added Succeffuly')
    else: 
        form = BookForm()
        cat_form = GenreForm()

    context={
        'books':Book.objects.all(),
        'genres':Genre.objects.all(),
        'categories':Genre.objects.all(),
        'form':BookForm(),
        'cat_form':cat_form,
        'languages':Language.objects.all(),
        'all_books':Book.objects.filter(active=True).count(),
        'sold_book':Book.objects.filter(status='sold').count(),
        'rental_book':Book.objects.filter(status='rental').count(),
        'available_book':Book.objects.filter(status='available').count(),

    }
    return render(request , 'pages/index.html' , context)

#********************* books view************
def books(request):
    search = Book.objects.all()

    title = None
    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains=title)
    context={
        'books':search,
        'genres':Genre.objects.all(),
        'cat_form':GenreForm() ,

    }
    return render(request , 'pages/books.html' , context)
#********************* update view************
def update(request , id):
    book_by_id = get_object_or_404(Book , id=id)
    if request.method =="POST":
        book_update_form = BookForm(request.POST , request.FILES , instance=book_by_id)
        if book_update_form.is_valid():
            book_update_form.save()
            messages.success(request , 'Book Updated Successfully')
            return redirect('/')
    else:
        book_update_form = BookForm(instance=book_by_id)
    context={
            'form':book_update_form
        }
    return render(request , 'pages/update.html', context)
#********************* books view************
def delete(request , id):
    book_by_id = get_object_or_404(Book , id=id)
    if request.method =="POST":
        book_by_id.delete()
        return redirect('lms_app:index')



    return render(request , 'pages/delete.html')
