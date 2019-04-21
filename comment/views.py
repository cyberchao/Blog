from django.shortcuts import render
from.models import Genre
from posts.models import Users as User

def talk(request,blog):
    # 如果没有登录，会获取到 AnonymousUser
    name = request.user
    name = User.objects.get(username=name)
    body = request.POST.get('comment')
    parent = request.POST.get('parent')
    print(parent)
    if not parent:
        Genre.objects.create(name=name,blog=blog,body=body)
    else:
        print(parent)
        parent = Genre.objects.get(id=parent)
        print(parent)
        Genre.objects.create(name=name,blog=blog,body=body,parent=parent)
