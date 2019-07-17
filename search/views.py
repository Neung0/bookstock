from django.shortcuts import render
from django.views.generic import View
# from .forms import BookForm
from search.models import Author

# class BookFormView(View):
#     form_class = BookForm

def index(request):
    auth_list = Author.objects.all().order_by('name')
    context = {'auth_list': auth_list}
    return render(request, 'search/index.html', context)