from django.shortcuts import render_to_response,render
from django.http import Http404
from django.views import View

from .models import Books, Auther, Publication, BookReview
from .form import BookReviewForm
# Create your views here.



class Index(View):
    books_list = Books.objects.order_by('name')
    authers = Auther.objects.order_by('first_name')
    publication_list = Publication.objects.order_by("name")

    def get(self,request):
        form = BookReviewForm()
        reviews = BookReview.objects.order_by('-date_on')
        return render(request,"library\index1.html",
            context= {
                'books':self.books_list,
                'authers':self.authers,
                'publication_list':self.publication_list,
                'reviews':reviews,
                'form':form,
            })

    def post(self,request):
        reviews = BookReview.objects.order_by('-date_on')
        form = BookReviewForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, "library\index1.html",
            context={
                'books': self.books_list,
                'authers': self.authers,
                'publication_list': self.publication_list,
                'reviews': reviews,
                'form': form,
            })

class BookDetail(View):

    def get(self,request,book_name):
        try:
            name = book_name.replace('_',' ')
            book = Books.objects.get(name=name)

        except Books.DoesNotExist:
            raise Http404('Books Does not exist')

        return render_to_response("library\\book_detail.html", context= {"book":book })

class AutherDetail(View):

    def get(self, request, auther_name):
        try:
            name = auther_name[:3]
            auther_a = Auther.objects.filter(first_name__icontains=auther_name[:4]).get(last_name__iendswith=auther_name[-3:])
            book_list = Books.objects.filter(auther__first_name__istartswith=name)

        except Books.DoesNotExist:
            raise Http404('Auther Does not exist')

        return render(request,"library\\auther_detail.html", context= {"book_list":book_list,"auther":auther_a })

