from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect


from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    list = request.user.username
    print(list)
    return render(request, "index.html",{"list":list})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            msg="올바른 유저ID와 패스워드를 입력하세요."
            try:
                # print(User.objects.all())
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg="존재하지 않는 ID입니다. "
            else:
                if user.check_password(raw_password):
                    msg=None
                    login(request,user)
                    return redirect('/')
                else:
                    msg="비밀번호가 틀렸습니다."
        else:
            msg="form is not valid."           
        # 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # 2. login 할 때 form을 활용해주세요						
    else:
        msg = None
        form = LoginForm()
    return render(request, "login.html", {"form": form,"msg":msg})


def logout_view(request):
    logout(request)
    # 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요						
    return HttpResponseRedirect("/")

@login_required
# 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
def user_list_view(request):
    # 7. /users 에 user 목록을 출력해주세요
    # 9. user 목록은 pagination이 되게 해주세요
    page = int(request.GET.get("page", 1))
    users = User.objects.all().order_by("-id")   #Users의 모든 객체를 user로 담음
    paginator = Paginator(users, 3)              #paginator 분할 객체 , 페이지 당 개수
    users = paginator.get_page(page)
    return render(request, "users.html", {"users": users})
