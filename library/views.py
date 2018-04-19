from django.shortcuts import render, reverse
from django.contrib.auth import logout
from django.http import Http404,HttpResponseRedirect
from django.views import View
from django.views.generic import FormView
from rest_framework.authtoken.models import Token
from django.core.serializers import serialize
from django.contrib.auth.views import LoginView
from django.http.response import JsonResponse

from .models import Books, Auther, Publication, BookReview
from .form import BookReviewForm

# Overriding Default Login Method
REDIRECT_FIELD_NAME = 'next'
import warnings
from django.contrib.auth.forms import AuthenticationForm
from django.utils.deprecation import RemovedInDjango21Warning
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# .....START................Login Override....................................
def login(request, template_name='library/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=False):
    warnings.warn(
        'The login() view is superseded by the class-based LoginView().',
        RemovedInDjango21Warning, stacklevel=2
    )
    return Login.as_view(
        template_name=template_name,
        redirect_field_name=redirect_field_name,
        form_class=authentication_form,
        extra_context=extra_context,
        redirect_authenticated_user=redirect_authenticated_user,
    )(request)


class Login(LoginView):
    def form_valid(self, form):
        super().form_valid(form)
        token, created = Token.objects.get_or_create(user=self.request.user)
        auth_token = serialize('json',
                               Token.objects.filter(user=self.request.user),
                               fields=('user',))
        self.request.session['auth_token'] = token.key
        return HttpResponseRedirect(self.get_success_url())
# .............Login Override..........END................................


# Define Post save to create auth Token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Index(View):
    books_list = Books.objects.order_by('name')
    authers = Auther.objects.order_by('first_name')
    publication_list = Publication.objects.order_by("name")

    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)

        request.session['auth_token'] = token.key

        return render(request,"library/index1.html",
            context= {
                'books':self.books_list,
                'authers':self.authers,
                'publication_list':self.publication_list,
                'token':request.session['auth_token'],
                })

    def post(self,request):
        return render(request, "library/index1.html",
                    context={
                        'books': self.books_list,
                        'authers': self.authers,
                        'publication_list': self.publication_list,
                    })


class BookDetail(FormView):
    form_class = BookReviewForm
    template_name = "library/book_detail.html"
    success_url = "/"
    http_method_names = [u'get', u'post']

    def get(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        try:
            form = BookReviewForm()
            name = kwargs['book_name'].replace('_',' ')
            book = Books.objects.get(name=name)
            reviews = BookReview.objects.filter(book=book)
            context = {"book": book,
                       'reviews': reviews,
                       'form': form,
                       'token':token.key,
                       }
        except Books.DoesNotExist:
            raise Http404('Books Does not exist')
        return render(request, self.template_name, context)

    def form_valid(self, form):
            token = Token.objects.get(user=self.request.user)
            if self.request.session['auth_token'] == token.key:
                # Check for authenticated token for logged user
                form.save()

            return JsonResponse({'result':'Success'})


class AutherDetail(View):

    def get(self, request, auther_name):
        try:
            name = auther_name[:3]
            auther_a = Auther.objects.filter(first_name__icontains=auther_name[:4]).get(last_name__iendswith=auther_name[-3:])
            book_list = Books.objects.filter(auther__first_name__istartswith=name)

        except Books.DoesNotExist:
            raise Http404('Auther Does not exist')

        return render(request,"library/auther_detail.html", context= {"book_list":book_list,"auther":auther_a })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))