from django.shortcuts import render_to_response,reverse,render
from django.http import HttpResponseRedirect,Http404,HttpResponse
from .models import books, auther, publication,users
from .form import login_form
from django.views import View
# Create your views here.

class login(View):
    def get(self, request):
        form = login_form()
        return render(request, 'library/login.html', {'form': form})

    def post(self,request):
            form = login_form(request.POST)
            if form.is_valid():
                return HttpResponse("Successfully login")

            return render(request,'library/login.html',{'form':form})
class index(View):
    def get(self,request):
        books_list = books.objects.order_by('name')
        authers = auther.objects.order_by('first_name')
        publication_list = publication.objects.order_by("name")
        return render(request,"library\index1.html", context= {'books':books_list, 'authers':authers, 'publication_list':publication_list})

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
class book_add(View):
    def get(request):

        try:
            name = request.POST['book_name']
            auther = request.POST['book_auther']
            published_on = request.POST['book_published']

            book = books(name=name, auther=auther, published_on=published_on)
            book.save()
            id = book.id
            return HttpResponseRedirect(reverse('new_book'))

        except (KeyError, name.DoesNotExist):
            return render(request, 'library\\book_detail.html', {
            'error_message': "You didn't select a choice.",
        })

class new_book(View):
    def get(self,request):
        book= books.objects.last()
        return render(request,"library\\new_book.html",context={'book':book})

