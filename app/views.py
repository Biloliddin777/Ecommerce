from django.db.models import Min, Max, Avg, Count, OuterRef, Subquery
from django.shortcuts import render

from app import models
from app.models import Author, Book


def index(request):
    authors = Author.objects.all().aggregate(authors_count=Count('id'))
    count = authors.get('authors_count')
    return render(request, 'app/index.html', {'count': count})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'app/index.html', {'books': books})

def magic(request):
    books1 = Book.objects.values('author__name').annotate(book_count=Count('id'))
    books2 = Book.objects.values('author__name').annotate(max_price=Max('price'))
    books3 = Book.objects.values('author__name').annotate(min_price=Min('price'))
    books4 = Book.objects.values('author__name').annotate(avg=Avg('price'))

    authors = Author.objects.all()

    context = {
        'books1': books1,
        'books2': books2,
        'books3': books3,
        'books4': books4,
        'authors': authors,
    }

    return render(request, 'app/index.html', context)