from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.conf import settings # เพิ่มเข้ามา
import json
import os


def load_otop_data():
    """
    ฟังก์ชันสำหรับโหลดข้อมูลจาก otop.json และแปลง Key ให้เป็นภาษาอังกฤษ
    เพื่อให้ง่ายต่อการใช้งานใน Template
    """
    products = []
    json_file_path = os.path.join(settings.BASE_DIR, 'otop.json')

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            raw_products = data.get('Sheet1', [])
            
            for p in raw_products:
                products.append({
                    'name': p.get('ชื่อสินค้า OTOP'),
                    'municipality': p.get('อปท.'),
                    'district': p.get('อำเภอ'),
                    'province': p.get('จังหวัด'),
                    'sale_location_name': p.get('ชื่อสถานที่จัดจำหน่าย'),
                    'address': p.get('ที่อยู่'),
                    'phone': p.get('เบอร์โทรศัพท์'),
                    'lat': p.get('LAT'),
                    'long': p.get('LONG'),
                })

    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file {json_file_path}.")
        
    return products


# Create your views here.

# หน้าหลัก
def home_view(request):
    # แสดงสินค้าแนะนำ 6 ชิ้นแรก
    all_products = load_otop_data()
    featured_products = all_products[:6]
    context = {'featured_products': featured_products}
    return render(request, 'home.html', context)

# หน้ารายการสินค้าทั้งหมด
def sels_view(request):
    products = load_otop_data()
    return render(request, 'sels.html', {'products': products})

# หน้าเข้าสู่ระบบ
def login_view(request):
    return render(request, 'login/login.html')

# หน้าสมัครสมาชิก
def register_view(request):
    return render(request, 'login/register.html')


# หน้าแผนที่
def map_view(request):
    all_products = load_otop_data()
    
    # กรองข้อมูลเฉพาะที่มีพิกัด Latitude และ Longitude
    otop_locations = [
        p for p in all_products if p.get('lat') is not None and p.get('long') is not None
    ]
    
    # เตรียมข้อมูลสำหรับส่งไปให้ JavaScript บนแผนที่
    locations_data = [
        {
            "name": loc.get("name"),
            "latitude": loc.get("lat"),
            "longitude": loc.get("long"),
            "location_name": loc.get("sale_location_name")
        } for loc in otop_locations
    ]
    # แปลง Python list of dicts เป็น JSON string
    locations_json = json.dumps(locations_data, ensure_ascii=False)

    api_key = settings.GOOGLE_MAPS_API_KEY

    context = {
        'locations_json': locations_json,
        'api_key': api_key,
    }
    return render(request, 'webpage/map_template.html', context)