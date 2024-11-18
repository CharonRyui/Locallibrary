from django.urls import reverse
from django.db import models
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
import uuid
from django.conf import settings
from datetime import date




# Create your models here.



class Genre(models.Model):
    '''model representing a book genre set'''
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre(e.g. Science Fiction)")
    
    def __str__(self):
        '''Sting for representing the model object'''
        return self.name
    
    def get_absolute_url(self):
        '''Returns the url to access a particular genre instance'''
        # We will define a URL mapping with the name 'genre-detail' and associate a view and a template to it
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        '''The metadata of the model
            constraints indicates how we keep the data unique

            Here we keep the lower case of name being unique
        '''
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'genre_name_case_insensitive_unique',
                violation_error_message = 'Genre already exists(case insensitive match)'
            )
        ]



class Language(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book's natural language")

    def get_absolute_url(self):
        return reverse('langugae-detail', args=[str(self.id)])
    def __str__(self):
        return self.name
    class Mete():
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'language_name_case_insensitive_unique',
                violation_error_message = 'Language already exists(class insensitive match)'
            )
        ]



class Book(models.Model):
    '''model representing a book'''

    title = models.CharField(max_length=200)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    # a book has an author so foreignkey is used here
    # and restrict means it's impossible to delete an author if he has a book still
    # here the author is a string because it haven't been defined yet
        # but using a string is also a way set up the relation
        # while it can be a little implicit if something is wrong
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')

    # for the ISBN should be upper cased, we prompt a verbose name here
    isbn = models.CharField("ISBN", max_length=13, unique=True, help_text='13 characters ISBN number')
    # a book have many genres and a genres may map many books
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        '''Create a string for the genre. This is required to diaplay genre in Admin'''
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
    



class BookInstance(models.Model):
    '''representing a specific copy of a book which can be borrowed from the library'''
    # uuid is a type signify a unique instance
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    ## 关联一个settings内置的user类型
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    # use choices to recommend the value of status
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        # 返回自己的id和书名的结合
        return f'{self.id} ({self.book.title})'
    
    ## the property decorator means the method will be called to tell if the
    ## object is 'falsy' (means null or return false)
    @property
    def is_overdue(self):
        '''determine if a book is overdue based on due date and current date'''
        return bool(self.due_back and date.today() > self.due_back)




class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(verbose_name='died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', "first_name"]
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
