from django.shortcuts import render, reverse
from django.contrib.auth import logout, login
from django.http import Http404, HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User

from .models import Books, Auther, Publication, BookReview
from .form import BookReviewForm, AddBookData, RegisterForm
# Create your views here.


class Register(View):
    def get(self,request):
        form = RegisterForm()
        return render(request,'library/register.html',context={'form':form})

    def post(self,request):
        form = RegisterForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            user = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(user, email, password)
            user.save()
            login(request,user)
            return render(request,'library/login.html')
        return render(request,'library/register.html',context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))



class Index(View):
    books_list = Books.objects.order_by('name')
    authers = Auther.objects.order_by('first_name')
    publication_list = Publication.objects.order_by("name")

    def get(self,request):
       return render(request,"library\index1.html",
            context= {
                'books':self.books_list,
                'authers':self.authers,
                'publication_list':self.publication_list,
                })

    def post(self,request):
        return render(request, "library\index1.html",
            context={
                'books': self.books_list,
                'authers': self.authers,
                'publication_list': self.publication_list,
            })


class BookDetail(View):
    form = BookReviewForm()

    def get(self,request,book_name):
            try:
                form = BookReviewForm()
                name = book_name.replace('_',' ')
                book = Books.objects.get(name=name)
                reviews = BookReview.objects.filter(book=book)[:5]
                context = {"book": book,
                           'reviews': reviews,
                           'form': form, }
            except Books.DoesNotExist:
                raise Http404('Books Does not exist')
            return render(request,"library\\book_detail.html", context )

    def post(self,request,book_name):
            form = BookReviewForm(request.POST)
            if form.is_valid():
                form.save()
            name = book_name.replace('_', ' ')
            book = Books.objects.get(name=name)
            reviews = BookReview.objects.filter(book=book)[:5]
            context = {"book": book,
                       'reviews': reviews,
                       'form': self.form, }
            return render(request,"library\\book_detail.html", context)


class AutherDetail(View):

    def get(self, request, auther_name):
        try:
            name = auther_name[:3]
            auther_a = Auther.objects.filter(first_name__icontains=auther_name[:4]).get(last_name__iendswith=auther_name[-3:])
            book_list = Books.objects.filter(auther__first_name__istartswith=name)

        except Books.DoesNotExist:
            raise Http404('Auther Does not exist')

        return render(request,"library\\auther_detail.html", context= {"book_list":book_list,"auther":auther_a })


class PublicationDetail (DetailView):
    model = Publication
    context_object_name = 'publication_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['publication_list'] = Publication.objects.all()
        return context


class AddBookDataView(View):
    def post(self,request):
        import pdb
        form = AddBookData(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form = AddBookData()
            return render(request, 'library/add_book_data.html', context={'form': form})

        return render(request,'library/add_book_data.html',context={'form':form})

    def get(self, request):
        form = AddBookData()
        return render(request,'library/add_book_data.html', context={'form':form})


class UpdateBookForm (UpdateView):
    model = Books
    fields = ['name','auther', 'published_on', 'publication', 'book_data']
    template_name_suffix = '_update_form'
    success_url = 'index.html'