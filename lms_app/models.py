from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns

# **************************************** Genre **************************
class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

# **************************************** Language **************************
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

# **************************************** Book **************************
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200 , verbose_name='عنوان الكتاب')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True , verbose_name='اسم المؤلف')
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="اكتب وصف للكتاب هنا" , verbose_name='وصف للكتاب')
    isbn = models.CharField(max_length=13,
                            unique=True,verbose_name='رقم الكتاب' ,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>', )
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    """ Some fileds from lms by abdo gamal"""
    book_img = models.ImageField(upload_to="books_pics" , null=True , blank=True)
    author_img =models.ImageField(upload_to="author_pics" , null=True , blank=True)
    pages = models.IntegerField(null=True , blank=True)
    price = models.DecimalField(max_digits=5 , decimal_places=2 , null=True , blank=True)
    rental_price_day = models.DecimalField(max_digits=5 , decimal_places=2 , null=True , blank=True)
    rental_period = models.IntegerField(null=True , blank=True)
    total_rental = models.DecimalField(max_digits=5 , decimal_places=2 , null=True , blank=True)
    active = models.BooleanField(default=True)
    book_status=(
    ('available' , 'available'),
    ('rental'  , 'rental'),
    ('sold' , 'sold')
    )
    status = models.CharField(max_length=50 , choices=book_status)

    
    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

# **************************************** BookInstance **************************
import uuid  # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)

# **************************************** Author **************************
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.first_name, self.last_name)
