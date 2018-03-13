import os
import mimetypes

from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .filters import BookFilter
from .form import BookReviewForm, AddBookData, RegisterForm, AddAutherForm
from .models import Books, Auther, Publication, BookReview
from .serializers import BookSerializer, BookReviewSerializer, AutherSerializer, PublicationSerializer

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

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
    active = User.objects.aggregate(
        total_users=Count('id'),
        total_active_users=Count('id', filter=F('is_active')),
    )


    def get(self,request):
        f = BookFilter(request.GET, queryset=Books.objects.all())
        context = {
            'books': self.books_list,
            'authers': self.authers,
            'publication_list': self.publication_list,
            'filter': f,
        }
        context.update(self.active)

        return render(request,"library\index1.html", context=context,
            )

    def post(self,request):
        context = {
            'books': self.books_list,
            'authers': self.authers,
            'publication_list': self.publication_list,
        }
        context.update(self.active)

        return render(request, "library\index1.html", context=context,
            )


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
        context['books'] = Books.objects.filter(publication=context['object'])
        return context


class AddBookDataView(View):
    def post(self,request):
        import pdb
        form_b = AddBookData(request.POST, request.FILES)
        form_a = AddAutherForm(request.POST)
        if form_b.is_valid() and form_a.is_valid():
            form_b.save()
            form_a.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form_b = AddBookData(request.POST, request.FILES)
            form_a = AddAutherForm(request.POST)
            return render(request, 'library/add_book_data.html', context={'form_b':form_b, 'form_a':form_a})

        return render(request,'library/add_book_data.html',context={'form_b':form_b, 'form_a':form_a})

    def get(self, request):
        form_a = AddBookData()
        form_b = AddAutherForm()
        return render(request,'library/add_book_data.html', context={'form_b':form_b, 'form_a':form_a})


class UpdateBookForm (UpdateView):
    model = Books
    fields = ['name','auther', 'published_on', 'publication', 'book_data']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')


# serializer Views
class BookSerializerViewset(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookReviewSerializerViewset(ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer


class AutherSerializerViewset(ModelViewSet):
    queryset = Auther.objects.all()
    serializer_class = AutherSerializer


class PublicationSerializerViewset(ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class BookSerializerTemplateView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name= 'library/book_serializer.html'

    def get(self, request, pk):
        book = Books.objects.get(pk=pk)
        serializer = BookSerializer(book, context={'request':request})
        return Response({'book':book, 'serializer':serializer }, template_name= 'library/book_serializer.html')

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return redirect('index')
        return Response({'book':book, 'serializer':serializer }, template_name= 'library/book_serializer.html')


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            # mimetypes.guess_type automatically takes content type of file
            type, encoding = mimetypes.guess_type(path)
            content_type_guess = type

            # content_type='application/forcedownload' will actually force to download anyformat data
            response = HttpResponse(fh.read(), content_type='application/forcedownload')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404