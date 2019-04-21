from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from posts.models import Posts, Remote,Category,Tag
from posts.models import Users as User
import json
from comment.views import talk
from comment.models import Genre

def post(request):
    blogs = Posts.objects.order_by('-timestamp')
    # 一个分页器实例，第一个参数是要被分页的所有对象，第二个参数是每页对象的个数
    paginator = Paginator(blogs, 10)
    # 获取请求的url中page的值,str类型
    page = request.GET.get('page')
    current_page = page if page else 1
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    recent = Posts.objects.order_by('-timestamp')[:3]
    tag_count = get_tag_count()
    category_count = get_category_count()
    """
    print(tag_count) 获取每个标签下blog的个数
    <QuerySet [{'categories__title': 'Django', 'categories__title__count': 1}, {'categories__title': 'Test', 'categories__title__count': 3}, {'categories__title': 'Rest', 'categories__title__count': 2}]>
    """
    context = {
        'blogs': paginated_queryset,  # 所有blog
        'recent': recent,  # 最近上传的3篇blog
        'category_count': category_count,  # 所有分类
        'tag_count': tag_count,  # 所有标签
        'pagerange': paginator.page_range,  # 分页器的一个可迭代对象
        'current_page': int(current_page),  # 当前页
        'pagenum': paginator.num_pages,  # 分页器分页后的页码数量
    }
    return render(request, 'blog.html', context)


def blog(request, id):
    """
    获取client端的ip地址，如果已经在博客阅读者中存在，阅读数不变，否则+1，
    创建一个Posts的ManyToManyField,关联到Remote,
    关联的对象可以通过字段的 RelatedManager 添加、删除和创建。
    """
    ip = request.META['REMOTE_ADDR']
    remote = Remote.objects.filter(ip=ip)
    blog = get_object_or_404(Posts, id=id)
    blog_viewer = blog.views.all()

    allviewer = [viewer.ip for viewer in blog_viewer]
    if ip not in allviewer:
        blog.view_count += 1
        blog.views.create(ip=ip)
        blog.save()
    """
    lte 小于等于
    gte 大于等于
    """
    try:
        pre_page = Posts.objects.filter(id__lte=id).order_by('-id')[1]
    except:
        pre_page = None
    try:
        next_page = Posts.objects.filter(id__gte=id).order_by('id')[1]
    except:
        next_page = None

    recent = Posts.objects.order_by('-timestamp')[:3]
    tag_count = get_tag_count()
    category_count = get_category_count()
    if request.method == 'POST':
        talk(request,blog)
    context = {
        'blog': blog,
        'recent': recent,
        'category_count': category_count,  # 所有分类
        'tag_count': tag_count,
        'pre': pre_page,
        'next': next_page,
        'genres': Genre.objects.filter(blog=blog)
        # 'form': form,
    }
    return render(request, 'post.html', context)


def search(request):
    queryset = Posts.objects.all()
    query = request.GET.get('q')
    span='站内搜索：'
    if query:
        blogs = queryset.filter(Q(title__icontains=query) |
                                Q(overview__icontains=query)).distinct()
    paginator = Paginator(blogs, 10)
    # 获取请求的url中page的值,str类型
    page = request.GET.get('page')
    current_page = page if page else 1
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    recent = Posts.objects.order_by('-timestamp')[:3]
    tag_count = get_tag_count()
    category_count = get_category_count()
    """
    print(tag_count) 获取每个标签下blog的个数
    <QuerySet [{'categories__title': 'Django', 'categories__title__count': 1}, {'categories__title': 'Test', 'categories__title__count': 3}, {'categories__title': 'Rest', 'categories__title__count': 2}]>
    """
    context = {
        'blogs': paginated_queryset,  # 所有blog
        'recent': recent,  # 最近上传的3篇blog
        'category_count': category_count,  # 所有分类
        'tag_count': tag_count,  # 所有标签
        'pagerange': paginator.page_range,  # 分页器的一个可迭代对象
        'current_page': int(current_page),  # 当前页
        'pagenum': paginator.num_pages,  # 分页器分页后的页码数量
        'span':span,
        'title':query,
    }
    return render(request, 'blog.html', context)


def get_tag_count():
    """
    获取tag名字以及对应的数量
    values 可以获取到具体某个字段的值，annotate 是聚集函数，起汇总作用，Count是表达式
    也是annotate必须的
    print(Posts.objects.values('tags__title').annotate(Count('tags__title')))
    """
    queryset = Posts.objects.values(
        'tags__id', 'tags__title').annotate(Count('tags__title'))
    return queryset


def get_category_count():

    query = Posts.objects.values('category__id', 'category__title').annotate(Count('category__title'))
    # print(Posts.objects.values('categories__title').annotate(Count('categories__title')))
    queryset = Category.objects.annotate(Count('posts'))
    print(query)
    print(type(queryset))
    return queryset


def get_Users(user):
    qs = User.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    else:
        return None


def get_category_blogs(request, id):
    blogs = Posts.objects.filter(category=id)
    # 一个分页器实例，第一个参数是要被分页的所有对象，第二个参数是每页对象的个数
    category_title = Category.objects.get(id=id).title
    span='查询分类：'
    paginator = Paginator(blogs, 10)
    # 获取请求的url中page的值,str类型
    page = request.GET.get('page')
    current_page = page if page else 1
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    recent = Posts.objects.order_by('-timestamp')[:3]
    tag_count = get_tag_count()
    category_count = get_category_count()
    cate = {}
    """
    print(tag_count) 获取每个标签下blog的个数
    <QuerySet [{'categories__title': 'Django', 'categories__title__count': 1}, {'categories__title': 'Test', 'categories__title__count': 3}, {'categories__title': 'Rest', 'categories__title__count': 2}]>
    """
    context = {
        'blogs': paginated_queryset,  # 所有blog
        'recent': recent,  # 最近上传的3篇blog
        'category_count': category_count,  # 所有分类
        'tag_count': tag_count,  # 所有标签
        'pagerange': paginator.page_range,  # 分页器的一个可迭代对象
        'current_page': int(current_page),  # 当前页
        'pagenum': paginator.num_pages,  # 分页器分页后的页码数量
        'span':span,
        'title':category_title,
    }
    return render(request, 'blog.html', context)


def get_tag_blogs(request, id):
    blogs = Posts.objects.filter(tags=id)
    tag_title = Tag.objects.get(id=id).title
    span='查询标签：'
    # 一个分页器实例，第一个参数是要被分页的所有对象，第二个参数是每页对象的个数
    paginator = Paginator(blogs, 10)
    # 获取请求的url中page的值,str类型
    page = request.GET.get('page')
    current_page = page if page else 1
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    recent = Posts.objects.order_by('-timestamp')[:3]
    tag_count = get_tag_count()
    category_count = get_category_count()
    """
    print(tag_count) 获取每个标签下blog的个数
    <QuerySet [{'categories__title': 'Django', 'categories__title__count': 1}, {'categories__title': 'Test', 'categories__title__count': 3}, {'categories__title': 'Rest', 'categories__title__count': 2}]>
    """
    context = {
        'blogs': paginated_queryset,  # 所有blog
        'recent': recent,  # 最近上传的3篇blog
        'category_count': category_count,  # 所有分类
        'tag_count': tag_count,  # 所有标签
        'pagerange': paginator.page_range,  # 分页器的一个可迭代对象
        'current_page': int(current_page),  # 当前页
        'pagenum': paginator.num_pages,  # 分页器分页后的页码数量
        'span':span,
        'title':tag_title,
    }
    return render(request, 'blog.html', context)


def about(request):
    return render(request,'About.html')


def license(request):
    lic = {'code':147258,'time':'20190410'}
    return HttpResponse(json.dumps(lic))
