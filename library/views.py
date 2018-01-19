from django.shortcuts import render_to_response,reverse,render
from django.http import HttpResponseRedirect,Http404,HttpResponse
from .models import books,auther
# Create your views here.
def index(request):
    books_list = books.objects.order_by('name')
    authers = auther.objects.order_by('first_name')
    return render(request,"index1.html", context= {'books':books_list, 'authers':authers, })

def book_detail(request,book_name):
    try:
        name = book_name.replace('_',' ')
        book = books.objects.get(name=name)
    except books.DoesNotExist:
        raise Http404('Books Does not exist')

    return render_to_response("book_detail.html", context= {"book":book })

def auther_detail(request,auther_name):
    try:
        name = auther_name[:3]
        auther_a = auther.objects.filter(first_name__icontains=auther_name[:4]).get(last_name__iendswith=auther_name[-3:])
        book_list = books.objects.filter(auther__first_name__istartswith=name)
    except books.DoesNotExist:
        raise Http404('Auther Does not exist')

    return render(request,"auther_detail.html", context= {"book_list":book_list,"auther":auther_a })

def book_add(request):

    try:
        name = request.POST['book_name']
        auther = request.POST['book_auther']
        published_on = request.POST['book_published']

        book = books(name=name, auther=auther, published_on=published_on)
        book.save()
        id = book.id
        return HttpResponseRedirect(reverse('new_book'))

    except (KeyError, name.DoesNotExist):
        return render(request, 'book_detail.html', {
        'error_message': "You didn't select a choice.",
    })


def new_book(request):
    book= books.objects.last()
    return render(request,"new_book.html",context={'book':book})

