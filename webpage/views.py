from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

# หน้าหลัก
def home_view(request):
    return render(request, 'home.html')

# หน้ารายการสินค้าทั้งหมด
def sels_view(request):
    return render(request, 'sels.html')

# หน้าแผนที่
def map_view(request):
    return render(request, 'map.html')

# หน้าเข้าสู่ระบบ
def login_view(request):
    return render(request, 'login/login.html')

# หน้าสมัครสมาชิก
def register_view(request):
    return render(request, 'login/register.html')