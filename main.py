from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

# 👥 Hesap listesi (İstediğin kadar ekleyebilirsin)
hesaplar = [
    ("nabi_kekem", "babapro41"),
    ("kullanici_adi2", "sifre2")
]

# 🌐 WebDriver (Render uyumlu)
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

# 🚨 Şikayet etme işlemi (Dil uyumlu: Türkçe + İngilizce)
def report(driver, hedef):
    driver.get(f"https://www.instagram.com/{hedef}/")
    time.sleep(7)
    try:
        # 3 nokta butonu
        buttons = driver.find_elements(By.XPATH, '//button')
        for btn in buttons:
            if btn.text.strip() == "..." or btn.get_attribute("aria-label") == "Options":
                btn.click()
                break
        time.sleep(2)

        # Şikayet Et adımları (hem TR hem EN destekli)
        def click_any(texts):
            for t in texts:
                try:
                    driver.find_element(By.XPATH, f'//button[contains(text(), "{t}")]').click()
                    time.sleep(2)
                    return
                except:
                    continue
            raise Exception(f"Seçenek bulunamadı: {texts}")

        click_any(["Şikayet et", "Report"])
        click_any(["Bu hesabı şikayet et", "Report Account"])
        click_any(["Instagram'da olmaması gereken içerikler paylaşıyor", "Sharing content that shouldn’t be on Instagram"])
        click_any(["Şiddet, nefret veya sömürü", "Violence or threat of violence"])
        click_any(["İstismar gibi görünüyor", "Looks like abuse"])
        click_any(["Cinsel istismar gibi görünüyor", "Sexual abuse"])
        click_any(["Evet", "Yes"])

        return "✔️ Şikayet başarıyla gönderildi."
    except Exception as e:
        return f"❌ Hata oluştu: {str(e)}"

# 🔁 Her hesapla sırayla çalış
def start(hedef_kullanici):
    loglar = []
    for username, password in hesaplar:
        driver = setup_browser()
        try:
            login(driver, username, password)
            sonuc = report(driver, hedef_kullanici)
            loglar.append(f"{username}: {sonuc}")
        except Exception as ex:
            loglar.append(f"{username} hata verdi: {str(ex)}")
        finally:
            driver.quit()
            time.sleep(4)
    return loglar

# 🌐 Arayüz
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/raporla", methods=["POST"])
def raporla():
    hedef = request.form.get("hedef_kullanici")
    if not hedef:
        return jsonify({"message": "Hedef kullanıcı adı girilmedi!"})
    loglar = start(hedef)
    return jsonify({"message": "\n".join(loglar)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
