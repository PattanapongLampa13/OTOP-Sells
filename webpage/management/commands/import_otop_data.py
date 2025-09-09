import json
from django.core.management.base import BaseCommand
from webpage.models import OtopProduct

class Command(BaseCommand):
    help = 'Imports OTOP product data from otop.json into the database'

    def handle(self, *args, **options):
        # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่ ถ้ามีให้ลบออกก่อน
        if OtopProduct.objects.exists():
            self.stdout.write(self.style.WARNING('Deleting existing OTOP product data...'))
            OtopProduct.objects.all().delete()

        # ระบุ path ไปยังไฟล์ otop.json ของคุณ
        json_file_path = 'otop.json' 

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f'Error decoding JSON from {json_file_path}'))
            return

        products = data.get('Sheet1', [])
        
        for item in products:
            # แปลงข้อมูลจาก key ที่เป็นภาษาไทยเป็นชื่อฟิลด์ในโมเดล
            # และจัดการกับข้อมูลที่อาจจะไม่มีในบาง record
            OtopProduct.objects.create(
                name=item.get("ชื่อสินค้า OTOP", ""),
                location_name=item.get("ชื่อสถานที่จัดจำหน่าย", ""),
                address=item.get("ที่อยู่", ""),
                phone=str(item.get("เบอร์โทรศัพท์", "")),
                latitude=item.get("LAT"),
                longitude=item.get("LONG"),
                # เพิ่มฟิลด์อื่นๆ ตามต้องการ
                description=f'{item.get("อำเภอ", "")}, {item.get("จังหวัด", "")}' # สร้าง description จากข้อมูลที่มี
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} OTOP products.'))

# หมายเหตุ: คุณต้องสร้างโฟลเดอร์ management และ commands ภายในแอป webpage ของคุณก่อน
# webpage/
# ├── management/
# │   ├── __init__.py
# │   └── commands/
# │       ├── __init__.py
# │       └── import_otop_data.py