import datetime
from django.shortcuts import render
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, BookInstance, Author, Genre
# from django.contrib.admin.views.decorators import staff_member_required




# Create your views here.



def index(request):
    '''View function for home page of site'''

    #Generate counts of some main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # get the session value or give it a default value with 0 if not defined yet
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    #Available books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #all() is implied by default
    num_authors = Author.objects.count()

    num_contains_b = Book.objects.filter(title__icontains='b').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_contains_b': num_contains_b,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)






class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    context_object_name = 'book_list' # name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='b')[:5] # get 5 books with 'b' in the title
    # template_name = 'books/my_arbitrary_template_name_list.html' # specify the template location

    # override the methods in ListView
    def get_queryset(self):
        return Book.objects.filter(title__icontains='b')[:5] # get 5 books with 'b' in the title
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['sth'] = 'just something here'
        # override the method so that you can add sth. arbitrary to thr context
        return context
    




class BookDetailView(generic.DetailView):
    model = Book







class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
    context_object_name = 'author_list'






class AuthorDetailView(generic.DetailView):
    model = Author





class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    




class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )
    


# generate a url based on the input configuraiton name and keys
# it's the equivalent of the {% url %} in template
from django.urls import reverse

from catalog.forms import RenewBookForm

# create a redirect
from django.http import HttpResponseRedirect

# this funciton will return an HTTP404 exception 
# if can not find a corresponding record of object of the model
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required, permission_required
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True) 
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        # create a form and populate it with the input data
        form = RenewBookForm(request.POST)

        # is_valid will check if the data is null
        # and call the clean_FIELD_NAME function to check
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        # a GET means the first time to render the form
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # passing initial argumanets to set up an initial form
        form = RenewBookForm(initial={'due_back':proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # it's an arbitrarily setting to display the initial value
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # not a recommended approach to use __all__
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.delete_author'
    # the default success_url is the detail page in update method and create method
    # but in delete method, that is not automatically existant
    success_url = reverse_lazy('authors')

    # because the book has a foreign key which declare the author on_delete RESTRICT
    # an invalid deletion could happen
    # use a form_valid method to check that and redirect
    def form_valid(self, form):
        try:
            self.get_object().delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse("author-delete", kwargs={'pk':self.get_object().pk}))
    


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.add_book'
    fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.change_book'
    fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.delete_book'
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        try:
            self.get_object().delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse('book-delete', kwargs={'pk': self.get_object().pk}))