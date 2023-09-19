from django.shortcuts import render

from login.models import RegisterUser
from django.shortcuts import redirect


# Create your views here.

def index(request):
    login_msg = "login successfully"
    return render(request, "index.html", {"login_msg":login_msg})

def register(request):
    if request.method == "POST":
        # get the user mame and password
        userName = request.POST.get("username")
        userPassword = request.POST.get("userpassword")
        userRePassword = request.POST.get("userrepassword")
        try:
            user=RegisterUser.objects.get(reg_name=userName)
            # user already exist then return to home page
            if user:
                msg = "user already exist"
                return render(request, "register.html", {"msg":msg})
        except:
            if userPassword != userRePassword:
                error_msg = "passwords not the same"
                return render(request, "register.html", {"error_msg":error_msg})
        else:
            register = RegisterUser()
            # save the username and user psw to the database
            register.reg_name = userName
            register.reg_pwd = userPassword
            register.save()
            return redirect("/login/")
    else:
        return render(request, "register.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if register.method == "POST":
        userName = request.POST.get("username")
        userPassword = request.POST.get("userpassword")
        try:
            user = RegisterUser.objects.get(reg_name=userName)

            if userPassword == user.reg_pwd:
                return redirect("/index/")
            else:
                error_msg = "wrong password"
                return render(request, "login_html", {"error_msg":error_msg})
        except:
            error_msg = "user not exist"
            return render(request, "login.html", {"error_msg":error_msg})

