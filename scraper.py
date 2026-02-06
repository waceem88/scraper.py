import os
import time
import hashlib
from supabase import create_client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# --- 1. الاتصال بالسحابة (Supabase) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ خطأ: لم يتم العثور على المفاتيح السرية!")
    exit()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. إعداد المتصفح الخفي ---
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# --- 3. وظيفة توليد ID ثابت للفريق ---
def generate_team_id(team_name_ar):
    # نستخدم "هاش" للاسم لكي يكون الكود ثابتاً دائماً لنفس الفريق
    # مثال: الشرطة دائماً سيعطي نفس الكود
    hash_object = hashlib.md5(team_name_ar.encode())
    hex_dig = hash_object.hexdigest()[:6].upper() # نأخذ أول 6 حروف
    return f"IRQ_{hex_dig}"

# --- 4. الحصاد الحقيقي (دوري نجوم العراق) ---
def run_harvest():
    print("🚜 بدء الحصاد الآلي لدوري نجوم العراق...")
    driver = setup_driver()
    
    try:
        # رابط دوري نجوم العراق على كووورة
        url = "https://www.kooora.com/?c=26646" 
        driver.get(url)
        time.sleep(3) # انتظار التحميل
        
        print(f"✅ تم الدخول للصفحة: {driver.title}")
        
        # البحث عن روابط الفرق في جدول الترتيب
        # في كووورة، الفرق موجودة في روابط تحتوي على '?team='
        team_links = driver.find_elements(By.XPATH, "//a[contains(@href, '?team=')]")
        
        collected_teams = []
        
        print(f"🔍 وجدنا {len(team_links)} رابط محتمل...")

        seen_names = set() # لتجنب التكرار

        for link in team_links:
            try:
                name_ar = link.text.strip()
                
                # تصفية: نأخذ فقط الأسماء الحقيقية (ليست فارغة ولا أرقام)
                if name_ar and len(name_ar) > 2 and name_ar not in seen_names:
                    team_id = generate_team_id(name_ar)
                    
                    team_data = {
                        "team_id": team_id,
                        "name_ar": name_ar,
                        "name_en": "Unknown", # سنحدثه لاحقاً
                        "city": "Iraq",
                        "logo_url": "Pending"
                    }
                    
                    collected_teams.append(team_data)
                    seen_names.add(name_ar)
                    print(f"✨ تم استخراج: {name_ar} (ID: {team_id})")
            except:
                continue
        
        # --- 5. الإرسال للسحابة (Upsert) ---
        if collected_teams:
            print(f"☁️ جاري رفع {len(collected_teams)} نادي إلى Supabase...")
            # نستخدم upsert لتحديث البيانات الموجودة أو إضافة الجديدة
            data, count = supabase.table('teams').upsert(collected_teams).execute()
            print("✅ تمت العملية بنجاح! البيانات الآن في السحابة.")
        else:
            print("⚠️ لم يتم العثور على فرق، قد يكون هناك تغيير في تصميم الموقع.")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء الحصاد: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_harvest()
