from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ProfileForm, SignupForm
from django.contrib.auth import get_user_model # 프로필


login = LoginView.as_view(template_name="accounts/login_form.html")

def logout(request):
    messages.success(request, '로그아웃되었습니다.')
    return logout_then_login(request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, '회원가입 환영합니다.')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form':form,
    })

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 수정/저장했습니다.')
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html",{'form':form

    })

@login_required
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    # post_list = Post.objects.filter(author=page_user)
    # post_list_count = post_list.count()  # 실제 데이터베이스에 count 쿼리를 던지게 됩니다.

    # if request.user.is_authenticated:
    #     is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    # else:
    #     is_follow = False

    return render(request, "accounts/user_page.html", {
        "page_user": page_user,
        # "post_list": post_list,
        # "post_list_count": post_list_count,
        # "is_follow": is_follow,
    })