from django import forms
from tinymce import TinyMCE
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class NewUser(forms.Form):
    username = forms.CharField(
        max_length=15,
        label='用户名',
        error_messages={
            'max_length': '用户名不能大于15位',
            'required': '用户名不能为空',
        }
    )
    password = forms.CharField(
        min_length=6,
        label='密码',
        # widget=forms.widgets.PasswordInput(),
        error_messages={
            'min_length': '密码不能少于6位',
            'required': '密码不能为空',
        }
    )
    re_password = forms.CharField(
        min_length=6,
        label='确认密码',
        widget=forms.widgets.PasswordInput(),
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.widgets.EmailInput(),
        error_messages={
            'invalid': '邮箱格式不正确',
            'required': '邮箱不能为空',
        }
    )

    # 自定义的验证规则，判断用户名或邮箱重复，密码不匹配
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        all_user = list(User.objects.all().values_list('username'))
        all_email = list(User.objects.all().values_list('email'))
        if (username,) in all_user:
            self.add_error('username', ValidationError('用户名已存在'))
        else:
            if (email,) in all_email:
                self.add_error('email', ValidationError('邮箱已被注册'))
            else:
                if re_password != password:
                    self.add_error('re_password', ValidationError('两次密码不一致'))
                else:
                    return self.cleaned_data


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
