from django.shortcuts import render, redirect
from .forms import NewUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Users as User
from django.core.mail import send_mail
from Crypto.Cipher import AES
import base64
from Crypto.Random import get_random_bytes
from django.core.files.base import ContentFile


# 加密，key必须是不小于16位的byte类型
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce


def home(request):
    return render(request, 'home.html')


# 注册方法
def signup(request):
    if request.method == 'POST':
        newuser = NewUser(request.POST)
        # 可以自定义valid验证规则，如果有效，写入数据库并重定向页面
        if newuser.is_valid():
            user = newuser.cleaned_data['username']
            email = newuser.cleaned_data['email']
            password = newuser.cleaned_data['password']
            user = User.objects.create_user(user, email, password)
            user.is_active = False
            user.save()
            # 加密，key必须是不小于16位的byte类型
            para = email
            data = para.encode('utf-8')
            ciphertext = cipher.encrypt(data)
            # 加密结果转换成字符串
            code = base64.encodebytes(ciphertext).decode('utf-8')
            code = code.replace(
                '/', 'slash').replace('=', 'equal').replace('+', 'plus').replace('%', 'percent')
            active_url = 'pandacoder.top/active/' + code
            send_mail('验证邮件', '请点击以下链接以激活您的账号：' + active_url,
                      'pr951029@163.com', [email], fail_silently=False)

            messages.success(request, '注册成功,但是为了确定您输入的邮箱属于您本人，请查收激活邮件！')
            return redirect('/')
        # 验证不通过返回错误
        else:
            return render(request, 'signup.html', {'form': newuser})
    return render(request, 'signup.html')

# 激活方法


def active(request, code):
    code = code.replace('slash', '/').replace('equal',
                                              '=').replace('plus', '+').replace('percent', '%')
    decrybyte = base64.decodebytes(code.encode('utf-8'))
    cipher2 = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher2.decrypt(decrybyte)
    data = data.decode('utf-8')
    getuser = User.objects.get(email=data)
    if getuser:
        getuser.is_active = True
        getuser.save()
        login(request, getuser)
        messages.success(request, '恭喜，您已成功激活账号！')
        return redirect('/')

# 登录方法


def loginde(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active is True:
                login(request, user)
                messages.success(request, '登录成功')
                return redirect('/')
            else:
                messages.success(request, '您尚未验证您的邮箱')
                return redirect('/login')
        else:
            messages.success(request, '用户不存在或密码错误')
            return redirect('/login')
    return render(request, 'login.html')


# 注销
def logoutde(request):
    logout(request)
    messages.success(request, '退出登录')
    return redirect('/')


# 资料页面
def profile(request):
    user = User.objects.get(username=request.user)
    return render(request, 'profile.html', {'user': user})


def handle_uploaded_file(f):
    with open('../static/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# 修改资料页面


def change_profile(request):
    if request.method == 'POST':
        profile_picture = request.FILES['avatar']
        print(type(profile_picture))
        user = User.objects.get(username=str(request.user))
        user.profile_picture = profile_picture
        website = request.POST.get('website')
        github = request.POST.get('github')
        introduction = request.POST.get('introduction')
        user.website = website
        user.github = github
        user.introduction = introduction
        user.save()
        # # 如果资料已存在则更新到最新提交，否则新建
        # file = request.FILES['file']
        # print(file)
        # file = ContentFile(profile_picture.read())
        # User.profile_picture.save('test.jpg', file)
        # User.save

        # User.objects.update(
        #     user=request.user,
        #     nickname=nickname,
        #     gender=gender,
        #     introduction=introduction)
        messages.success(request, '资料已修改')
        return redirect('/')
    return render(request, 'change-profile.html')
