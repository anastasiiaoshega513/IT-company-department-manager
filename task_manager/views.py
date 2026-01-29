from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def index(request: HttpRequest) -> HttpResponse:
    # num_of_books = Book.objects.count()
    # num_of_authors = Author.objects.count()
    # num_of_literary_formats = LiteraryFormat.objects.count()
    # num_visits = request.session.get("num_of_visits", 0)
    # request.session["num_of_visits"] = num_visits + 1
    context = {
        # "num_of_books": num_of_books,
        # "num_of_authors": num_of_authors,
        # "num_of_literary_formats": num_of_literary_formats,
        # "num_visits": num_visits + 1,
    }
    return render(request,"task_manager/index.html", context=context)
