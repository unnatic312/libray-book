from django.shortcuts import render_to_response,reverse,render
from django.http import HttpResponseRedirect,Http404
from .models import books, auther, publication
from django.views import View
# Create your views here.



class index(View):
    books_list = books.objects.order_by('name')
    authers = auther.objects.order_by('first_name')
    publication_list = publication.objects.order_by("name")

    def get(self,request):

        return render(request,"library\index1.html",
            context= {'books':self.books_list, 'authers':self.authers, 'publication_list':self.publication_list})
    def POST(self,request):

        return render(request, "library\index1.html",
            context={'books': self.books_list, 'authers': self.authers, 'publication_list': self.publication_list})

class book_detail(View):
    def get(self,request,book_name):
        try:
            name = book_name.replace('_',' ')
            book = books.objects.get(name=name)
        except books.DoesNotExist:
            raise Http404('Books Does not exist')

        return render_to_response("library\\book_detail.html", context= {"book":book })

class auther_detail(View):
    def get(self, request, auther_name):
        try:
            name = auther_name[:3]
            auther_a = auther.objects.filter(first_name__icontains=auther_name[:4]).get(last_name__iendswith=auther_name[-3:])
            book_list = books.objects.filter(auther__first_name__istartswith=name)
        except books.DoesNotExist:
            raise Http404('Auther Does not exist')

        return render(request,"library\\auther_detail.html", context= {"book_list":book_list,"auther":auther_a })

