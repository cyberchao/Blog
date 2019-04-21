from django.shortcuts import render


def index(request):
    queryset = Posts.objects.filter(featured = True)
    context = {
        'object_list': queryset,
    }
    return render(request, 'index.html', context)


def blog(request):
    return render(request, 'blog.html')
