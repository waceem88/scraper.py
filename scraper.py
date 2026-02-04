import os
import time
from supabase import create_client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 1. الاتصال بالسحابة (يقرأ المفاتيح من الخزنة السرية)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ خطأ: لم يتم العثور على المفاتيح السرية!")
    exit()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. إعداد المتصفح الخفي (Headless Chrome)
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # لا تفتح نافذة
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# 3. الزحف (مثال: سحب عنوان كووورة للتجربة)
def run_harvest():
    print("🚜 بدء الحصاد الآلي...")
    driver = setup_driver()

    try:
        # مثال: الدخول لصفحة الدوري العراقي
        url = "https://www.kooora.com/?c=26646" 
        driver.get(url)
        time.sleep(2)

        page_title = driver.title
        print(f"✅ تم الدخول بنجاح إلى: {page_title}")

        # (هنا سنضيف كود سحب الجداول لاحقاً)
        # الآن سنرسل رسالة تجريبية لقاعدة البيانات للتأكد من الربط

        data = {"name_ar": "نادي التجربة الآلي", "team_id": "TEST_001"}
        # ملاحظة: تأكد أن جدول teams موجود في Supabase
        # supabase.table('teams').insert(data).execute()
        print("☁️ (محاكاة) تم إرسال البيانات للسحابة!")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_harvest()
