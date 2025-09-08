


from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

from .models import OtopProduct
import json
from django.core.serializers import serialize

# Create your views here.

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



def map_view(request):
    # ดึงข้อมูลสินค้า OTOP ทั้งหมด
    products = OtopProduct.objects.all()
    
    # แปลงข้อมูล QuerySet เป็น GeoJSON format ที่ใช้ง่ายใน JavaScript
    # หรือจะแปลงเป็น JSON ธรรมดาก็ได้
    products_json = serialize('json', products, fields=('name', 'latitude', 'longitude'))

    # ดึง API Key จาก settings.py (วิธีที่ปลอดภัยกว่า)
    # อย่าลืมไปเพิ่ม GOOGLE_MAPS_API_KEY = "your_key" ในไฟล์ settings.py
    from django.conf import settings
    api_key = settings.GOOGLE_MAPS_API_KEY

    context = {
        'products_json': products_json,
        'api_key': api_key,
    }
    return render(request, 'webpage/map_template.html', context)