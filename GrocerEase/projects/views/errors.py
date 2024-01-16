from django.shortcuts import render



def custom_error_page(request, not_found):
    return render(request, 'errors/404.html', {'not_found': not_found})
