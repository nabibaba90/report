from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

# 👥 Hesap listesi (Kendine göre güncelle)
hesaplar = [
    ("nabi_kekem", "babapro41"),
    ("kullanici_adi2", "sifre2")
]

# 🌐 WebDriver ayarları (Render uyumlu)
def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    return driver

# 🔐 Giriş fonksiyonu
def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)
    time.sleep(8)

# 🚨 Şikayet Gönderme
def report(driver, hedef):
    driver.get(f"https://www.instagram.com/{hedef}/")
    time.sleep(7)
    try:
        # 3 Nokta menüsü
        buttons = driver.find_elements(By.XPATH, '//button')
        for btn in buttons:
            if btn.text.strip() == "...":
                btn.click()
                break
        time.sleep(2)

        # Şikayet Et Adımları
        driver.find_element(By.XPATH, '//button[contains(text(), "Şikayet et")]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(text(), "Bu hesabı şikayet et")]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(text(), "Instagram\'da olmaması gereken içerikler paylaşıyor")]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(text(), "Şiddet, nefret veya sömürü")]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(text(), "İstismar gibi görünüyor")]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(text(), "Cinsel istismar gibi görünüyor")]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[contains(text(), "Evet")]').click()
        time.sleep(2)

        return "✔️ Şikayet başarıyla gönderildi."
    except Exception as e:
        return f"❌ Hata oluştu: {e}"

# 🔁 Tüm hesaplarla çalıştır
def start(hedef_kullanici):
    for username, password in hesaplar:
        driver = setup_browser()
        try:
            login(driver, username, password)
            sonuc = report(driver, hedef_kullanici)
            print(f"{username}: {sonuc}")
        except Exception as ex:
            print(f"{username} hata verdi: {ex}")
        finally:
            driver.quit()
            time.sleep(4)

# 🌐 Flask Arayüz
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/raporla", methods=["POST"])
def raporla():
    hedef = request.form.get("hedef_kullanici")
    start(hedef)
    return f"<h2>{hedef} için işlem tamamlandı.</h2><a href='/'>Geri dön</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
