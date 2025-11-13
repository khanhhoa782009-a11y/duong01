#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import os
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

VIETNAMESE_FIRST_NAMES = [
    'Anh', 'Bảo', 'Châu', 'Dũng', 'Đức', 'Giang', 'Hà', 'Hải', 'Hiếu', 'Hoàng',
    'Hùng', 'Huy', 'Khánh', 'Khoa', 'Kiên', 'Linh', 'Long', 'Mai', 'Minh', 'Nam',
    'Ngọc', 'Nhung', 'Phong', 'Phương', 'Quang', 'Quyên', 'Sơn', 'Tâm', 'Thảo', 'Thư',
    'Trâm', 'Trinh', 'Trung', 'Tuấn', 'Tú', 'Uyên', 'Vân', 'Việt', 'Xuân', 'Yến'
]

VIETNAMESE_LAST_NAMES = [
    'Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan', 'Vũ', 'Võ', 'Đặng',
    'Bùi', 'Đỗ', 'Hồ', 'Ngô', 'Dương', 'Lý'
]

FIXED_PASSWORDS = ['tdk12309', 'tdk12308', 'tdk12307', 'tdk12311']

def remove_vietnamese_accents(text):
    accent_map = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'đ': 'd',
        'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
        'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
        'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
        'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
        'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
        'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
        'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
        'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
        'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
        'Đ': 'D'
    }
    result = ''
    for char in text:
        result += accent_map.get(char, char)
    return result

def generate_vietnamese_email():
    last_name = random.choice(VIETNAMESE_LAST_NAMES)
    first_name = random.choice(VIETNAMESE_FIRST_NAMES)
    
    last_name_no_accent = remove_vietnamese_accents(last_name).lower()
    first_name_no_accent = remove_vietnamese_accents(first_name).lower()
    
    random_number = random.randint(100, 9999)
    
    email = f"{last_name_no_accent}{first_name_no_accent}{random_number}@gmail.com"
    
    return email

def get_fixed_password():
    return random.choice(FIXED_PASSWORDS)

def setup_chrome_driver():
    try:
        chromium_path = subprocess.check_output(['which', 'chromium'], text=True).strip()
        print(f"Đã tìm thấy Chromium tại: {chromium_path}")
    except:
        chromium_path = None
        print("Cảnh báo: Không tìm thấy Chromium, sẽ dùng mặc định")
    
    try:
        chromedriver_path = subprocess.check_output(['which', 'chromedriver'], text=True).strip()
        print(f"Đã tìm thấy ChromeDriver tại: {chromedriver_path}")
    except:
        chromedriver_path = None
        print("Cảnh báo: Không tìm thấy ChromeDriver")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    if chromium_path:
        chrome_options.binary_location = chromium_path
    
    print("Đang khởi tạo ChromeDriver service...")
    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
    else:
        service = Service()
    
    print("Đang khởi tạo Chrome driver...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Chrome driver đã được khởi tạo thành công!")
    
    return driver

def register_account(email, password):
    driver = None
    try:
        print(f"Đang khởi tạo trình duyệt...")
        driver = setup_chrome_driver()
        
        print(f"Đang truy cập trang đăng ký...")
        driver.get("https://app.bumx.vn/register")
        
        wait = WebDriverWait(driver, 20)
        
        print(f"Đang đợi form đăng ký xuất hiện...")
        time.sleep(3)
        
        print(f"Đang điền email: {email}")
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='email']")))
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(1)
        
        print(f"Đang điền mật khẩu...")
        password_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        
        if len(password_inputs) >= 2:
            password_inputs[0].clear()
            password_inputs[0].send_keys(password)
            time.sleep(1)
            
            print(f"Đang điền xác nhận mật khẩu...")
            password_inputs[1].clear()
            password_inputs[1].send_keys(password)
            time.sleep(1)
        else:
            print("Cảnh báo: Không tìm thấy đủ 2 trường mật khẩu!")
            return False
        
        print(f"Đang tìm nút đăng ký...")
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Tìm thấy {len(buttons)} button trên trang")
        
        for i, btn in enumerate(buttons):
            btn_text = btn.text.strip()
            btn_html = (btn.get_attribute('outerHTML') or '')[:200]
            print(f"  Button {i+1}: text='{btn_text}', HTML={btn_html}")
        
        register_button = None
        for btn in buttons:
            btn_text = btn.text.strip().upper()
            if 'ĐĂNG KÝ' in btn_text or 'DANG KY' in btn_text:
                register_button = btn
                print(f"Đã tìm thấy nút đăng ký qua text matching")
                break
        
        if not register_button:
            try:
                register_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                print(f"Đã tìm thấy nút đăng ký qua button[type='submit']")
            except:
                pass
        
        if not register_button:
            try:
                register_button = driver.find_element(By.XPATH, "//button[contains(@class, 'register') or contains(@class, 'submit')]")
                print(f"Đã tìm thấy nút đăng ký qua class")
            except:
                pass
        
        if not register_button:
            print("Không tìm thấy nút đăng ký!")
            driver.save_screenshot("debug_screenshot.png")
            print("Đã lưu screenshot debug vào debug_screenshot.png")
            return False
        
        print(f"Đang nhấn nút đăng ký...")
        driver.execute_script("arguments[0].click();", register_button)
        
        print(f"Đang đợi kết quả đăng ký...")
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"URL hiện tại: {current_url}")
        
        if "login" in current_url.lower() or "dashboard" in current_url.lower() or current_url != "https://app.bumx.vn/register":
            print(f"✓ Đăng ký thành công!")
            return True
        else:
            page_text = driver.find_element(By.TAG_NAME, 'body').text
            if "thành công" in page_text.lower() or "success" in page_text.lower():
                print(f"✓ Đăng ký thành công!")
                return True
            else:
                print(f"⚠ Có thể đăng ký thất bại. Vui lòng kiểm tra.")
                print(f"Nội dung trang: {page_text[:200]}")
                return False
                
    except Exception as e:
        print(f"✗ Lỗi khi đăng ký: {str(e)}")
        return False
        
    finally:
        if driver:
            print(f"Đang đóng trình duyệt...")
            driver.quit()

def save_account_info(email, password, success):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "THÀNH CÔNG" if success else "THẤT BẠI"
    
    with open("registered_accounts.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Thời gian: {timestamp}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Mật khẩu: {password}\n")
        f.write(f"Trạng thái: {status}\n")
        f.write(f"{'='*60}\n")
    
    print(f"\nĐã lưu thông tin vào file: registered_accounts.txt")

# --- PHẦN ĐƯỢC CHỈNH SỬA BẮT ĐẦU TỪ ĐÂY ---

def main():
    print("="*60)
    print("      CÔNG CỤ TỰ ĐỘNG ĐĂNG KÝ TÀI KHOẢN BUMX.VN")
    print("            (Sẽ chạy 2 lần và tự động dừng)")
    print("="*60)
    
    # Vòng lặp for để chạy đúng 2 lần
    for i in range(2):
        print(f"\n--- Bắt đầu đăng ký tài khoản {i + 1}/2 ---")
        
        email = generate_vietnamese_email()
        password = get_fixed_password()
        
        print(f"Email: {email}")
        print(f"Mật khẩu: {password}\n")
        
        success = register_account(email, password)
        
        save_account_info(email, password, success)
        
        if success:
            print(f"✓ Hoàn tất tài khoản {i + 1}/2: THÀNH CÔNG")
        else:
            print(f"⚠ Hoàn tất tài khoản {i + 1}/2: THẤT BẠI (Vui lòng kiểm tra log)")
        
        print("-" * 60)
        
        # Thêm 1 khoảng nghỉ ngắn 5 giây giữa 2 lần chạy
        if i == 0:
            print("\nNghỉ 5 giây trước khi đăng ký tài khoản tiếp theo...\n")
            time.sleep(5)

    print("\nĐÃ HOÀN THÀNH 2 LƯỢT ĐĂNG KÝ. TẠM BIỆT!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Xử lý nếu người dùng nhấn Ctrl+C trong lúc đang đăng ký
        print("\n\nĐã nhận lệnh dừng (Ctrl+C). Đang dọn dẹp và thoát...")

