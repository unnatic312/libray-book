from django.shortcuts import render, reverse
from django.contrib.auth import logout
from django.http import Http404,HttpResponseRedirect
from django.views import View

from .models import Books, Auther, Publication, BookReview
from .form import BookReviewForm
# Create your views here.

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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))