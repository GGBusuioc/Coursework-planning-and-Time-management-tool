@csrf_exempt
def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return render(request, 'sis/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'sis/login.html')
