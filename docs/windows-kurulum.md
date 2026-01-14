# Windows Kurulum Kılavuzu

Bu dokümantasyon, Luma-Server projesini Windows işletim sisteminde sıfırdan kurulumdan dev sunucunun ayağa kaldırılmasına kadar tüm adımları detaylı olarak açıklar.

## 📋 İçindekiler

1. [Gereksinimler](#gereksinimler)
2. [GitHub'dan Projeyi İndirme](#githubdan-projeyi-indirme)
3. [Python Kurulumu](#python-kurulumu)
4. [Proje Kurulumu](#proje-kurulumu)
5. [Virtual Environment Oluşturma](#virtual-environment-oluşturma)
6. [Bağımlılıkları Yükleme](#bağımlılıkları-yükleme)
7. [Veritabanı Hazırlama](#veritabanı-hazırlama)
8. [XNavi Kurulumu](#xnavi-kurulumu)
9. [Dev Sunucuyu Başlatma](#dev-sunucuyu-başlatma)
10. [Otomatik Kurulum (Batch Dosyası)](#otomatik-kurulum-batch-dosyası)
11. [Sorun Giderme](#sorun-giderme)

---

## 🔧 Gereksinimler

### Sistem Gereksinimleri

- **İşletim Sistemi**: Windows 10 veya üzeri
- **Python**: 3.8 veya üzeri
- **Git**: Projeyi klonlamak için (opsiyonel, ZIP indirme de mümkün)
- **İnternet Bağlantısı**: Bağımlılıkları indirmek için

### Yazılım Gereksinimleri

- Python 3.8+ (https://www.python.org/downloads/)
- Git (opsiyonel) (https://git-scm.com/download/win)
- Code Editor (Visual Studio Code, PyCharm, vb.)

---

## 📥 GitHub'dan Projeyi İndirme

### Yöntem 1: Git ile Klonlama (Önerilen)

1. **Git'i yükleyin** (eğer yüklü değilse):
   - https://git-scm.com/download/win adresinden indirin
   - Kurulum sırasında "Add Git to PATH" seçeneğini işaretleyin

2. **Komut İstemi (CMD) veya PowerShell'i açın**:
   - `Win + R` tuşlarına basın
   - `cmd` veya `powershell` yazın ve Enter'a basın

3. **Projeyi klonlayın**:
   ```bash
   cd C:\Users\<KullanıcıAdınız>\Desktop
   git clone <repository-url>
   cd Luma-Server
   ```

   **Not**: `<repository-url>` yerine gerçek GitHub repository URL'ini yazın.
   Örnek: `git clone https://github.com/kullaniciadi/Luma-Server.git`

### Yöntem 2: ZIP Olarak İndirme

1. **GitHub repository sayfasına gidin**
2. **Yeşil "Code" butonuna tıklayın**
3. **"Download ZIP" seçeneğini seçin**
4. **ZIP dosyasını bir klasöre çıkarın** (örn: `C:\Users\<KullanıcıAdınız>\Desktop\Luma-Server`)
5. **Komut İstemi'ni açın ve proje klasörüne gidin**:
   ```bash
   cd C:\Users\<KullanıcıAdınız>\Desktop\Luma-Server
   ```

---

## 🐍 Python Kurulumu

### Adım 1: Python'u İndirme

1. **Python resmi sitesine gidin**: https://www.python.org/downloads/
2. **"Download Python" butonuna tıklayın** (en son sürüm otomatik indirilir)
3. **İndirilen `.exe` dosyasını çalıştırın**

### Adım 2: Python Kurulum Ayarları

Kurulum sırasında **mutlaka** aşağıdaki seçeneği işaretleyin:

- ✅ **"Add Python to PATH"** (Çok önemli!)

Bu seçenek Python'u sistem PATH'ine ekler ve komut satırından erişilebilir hale getirir.

### Adım 3: Kurulumu Tamamlama

1. **"Install Now"** butonuna tıklayın
2. Kurulum tamamlanana kadar bekleyin
3. **"Close"** butonuna tıklayın

### Adım 4: Python Kurulumunu Doğrulama

1. **Yeni bir Komut İstemi (CMD) veya PowerShell penceresi açın**
   - Önemli: Eski pencereyi kapatıp yeni bir tane açın (PATH değişikliklerinin yüklenmesi için)

2. **Python'un yüklü olup olmadığını kontrol edin**:
   ```bash
   python --version
   ```
   
   Beklenen çıktı: `Python 3.8.x` veya üzeri

3. **pip'in yüklü olup olmadığını kontrol edin**:
   ```bash
   pip --version
   ```
   
   Beklenen çıktı: `pip 20.x.x` veya üzeri

### ⚠️ Python Bulunamıyorsa

Eğer `python --version` komutu çalışmıyorsa:

1. **Python'u PATH'e manuel ekleyin**:
   - `Win + R` → `sysdm.cpl` → Enter
   - "Advanced" sekmesi → "Environment Variables"
   - "System variables" altında "Path" seçin → "Edit"
   - "New" → Python kurulum yolunu ekleyin (örn: `C:\Python38\` ve `C:\Python38\Scripts\`)
   - "OK" ile tüm pencereleri kapatın
   - **Yeni bir CMD penceresi açın** ve tekrar deneyin

2. **Alternatif olarak `py` komutunu kullanın**:
   ```bash
   py --version
   ```

---

## 📦 Proje Kurulumu

### Adım 1: Proje Klasörüne Gitme

Komut İstemi veya PowerShell'de proje klasörüne gidin:

```bash
cd C:\Users\<KullanıcıAdınız>\Desktop\Luma-Server
```

**Not**: `<KullanıcıAdınız>` yerine Windows kullanıcı adınızı yazın.

### Adım 2: Proje Yapısını Kontrol Etme

Proje klasöründe aşağıdaki dosyaların olduğundan emin olun:

- `manage.py`
- `requirements.txt`
- `README.md`
- `LumaServer/` klasörü
- `api/` klasörü

Kontrol için:
```bash
dir
```

---

## 🔐 Virtual Environment Oluşturma

Virtual environment, projenin bağımlılıklarını sistem Python'undan izole eder. Bu, farklı projeler arasında çakışmaları önler.

### Adım 1: Virtual Environment Oluşturma

Proje klasöründe şu komutu çalıştırın:

```bash
python -m venv venv
```

**Alternatif** (eğer `python` çalışmıyorsa):
```bash
py -m venv venv
```

Bu komut `venv` adında bir klasör oluşturur.

### Adım 2: Virtual Environment'ı Aktif Etme

**Windows CMD için**:
```bash
venv\Scripts\activate.bat
```

**Windows PowerShell için**:
```bash
venv\Scripts\Activate.ps1
```

Eğer PowerShell'de execution policy hatası alırsanız:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Adım 3: Aktif Olduğunu Doğrulama

Virtual environment aktif olduğunda, komut satırının başında `(venv)` görünür:

```
(venv) C:\Users\KullanıcıAdı\Desktop\Luma-Server>
```

### Adım 4: pip'i Güncelleme (Önerilen)

Virtual environment aktifken pip'i güncelleyin:

```bash
python -m pip install --upgrade pip
```

---

## 📚 Bağımlılıkları Yükleme

### Adım 1: requirements.txt Dosyasını Kontrol Etme

Proje klasöründe `requirements.txt` dosyasının olduğundan emin olun:

```bash
type requirements.txt
```

### Adım 2: Bağımlılıkları Yükleme

Virtual environment aktifken (komut satırında `(venv)` görünüyor olmalı):

```bash
pip install -r requirements.txt
```

Bu komut aşağıdaki paketleri yükler:
- Django
- djangorestframework
- django-cors-headers
- requests

### Adım 3: Yükleme İşlemini Doğrulama

Yüklenen paketleri kontrol edin:

```bash
pip list
```

Aşağıdaki paketlerin listelenmiş olması gerekir:
- Django
- djangorestframework
- django-cors-headers
- requests

---

## 🗄️ Veritabanı Hazırlama

Luma-Server, varsayılan olarak SQLite veritabanı kullanır. İlk kurulumda veritabanı dosyasını oluşturmak için migration'ları çalıştırmanız gerekir.

### Adım 1: Migration'ları Çalıştırma

Virtual environment aktifken:

```bash
python manage.py migrate
```

Bu komut:
- Veritabanı dosyasını oluşturur (`db.sqlite3`)
- Tüm tabloları oluşturur
- İlk verileri yükler (eğer varsa)

### Adım 2: Veritabanı Dosyasını Kontrol Etme

Migration işlemi tamamlandıktan sonra proje klasöründe `db.sqlite3` dosyasının oluştuğunu kontrol edin:

```bash
dir db.sqlite3
```

---

## 🔌 XNavi Kurulumu

XNavi, Advantech USB-4751L donanımı için gerekli olan yapılandırma ve kurulum aracıdır. Kamera ve flash kontrolü için XNavi'nin kurulu ve yapılandırılmış olması gerekmektedir.

### Adım 1: XNavi.exe Dosyasını Kontrol Etme

Proje klasöründe `XNavi.exe` dosyasının olduğundan emin olun:

```bash
dir XNavi.exe
```

Eğer dosya yoksa, projeyi GitHub'dan tekrar indirin veya dosyayı proje klasörüne ekleyin.

### Adım 2: XNavi Kurulumunu Başlatma

1. **XNavi.exe dosyasını çift tıklayarak çalıştırın**

   ![XNavi Kurulum - Adım 1](xnavi%20setup/1.png)
   
   *Kurulum başlangıç ekranı*

2. **Kurulum sihirbazını takip edin**

   Kurulum sihirbazı açıldığında "Next" butonuna tıklayarak devam edin.

   ![XNavi Kurulum - Adım 2](xnavi%20setup/2.png)
   
   *Kurulum sihirbazı ekranı*

### Adım 3: Kurulum Ayarları

Kurulum sırasında:

1. **Kurulum konumunu seçin** (varsayılan konum genellikle uygundur)
2. **Kurulum seçeneklerini gözden geçirin**
3. **"Install" veya "Next" butonlarına tıklayarak kurulumu tamamlayın**

### Adım 4: Kurulumu Doğrulama

Kurulum tamamlandıktan sonra:

1. **XNavi'nin başarıyla kurulduğundan emin olun**
2. **Gerekirse bilgisayarı yeniden başlatın** (kurulum sihirbazı önerirse)

### ⚠️ Önemli Notlar

- **XNavi kurulumu**, Advantech USB-4751L donanımı kullanılacaksa **zorunludur**
- XNavi kurulmadan kamera ve flash kontrolü çalışmayabilir
- Kurulum sırasında yönetici yetkileri gerekebilir
- USB-4751L cihazının bilgisayara bağlı olması gerekmez (kurulum için)

### 🔧 Sorun Giderme

**XNavi.exe çalışmıyorsa:**
- Yönetici olarak çalıştırmayı deneyin (sağ tık → "Run as administrator")
- Antivirus yazılımının dosyayı engellemediğinden emin olun
- Windows Defender veya diğer güvenlik yazılımlarını kontrol edin

**Kurulum hatası alıyorsanız:**
- Önceki XNavi kurulumlarını kaldırın (Control Panel → Programs and Features)
- Geçici dosyaları temizleyin
- Bilgisayarı yeniden başlatın ve tekrar deneyin

---

## 🚀 Dev Sunucuyu Başlatma

### Yöntem 1: Manuel Başlatma

Virtual environment aktifken:

```bash
python manage.py runserver
```

Sunucu başladığında şu mesajı görürsünüz:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Yöntem 2: Özel Port ile Başlatma

8000 portu kullanılıyorsa farklı bir port kullanabilirsiniz:

```bash
python manage.py runserver 8001
```

### Yöntem 3: Batch Dosyası ile Başlatma (Önerilen)

Proje klasöründe `start.bat` dosyasını çift tıklayarak çalıştırın. Bu dosya:
- Python kurulumunu kontrol eder
- Virtual environment'ı aktif eder (varsa)
- Bağımlılıkları kontrol eder
- Migration'ları çalıştırır
- Sunucuyu başlatır

### Sunucuyu Durdurma

Sunucuyu durdurmak için:
- Komut satırında `Ctrl + C` tuşlarına basın

### Sunucuya Erişim

Sunucu çalıştıktan sonra tarayıcınızda şu adrese gidin:

```
http://127.0.0.1:8000/
```

veya

```
http://localhost:8000/
```

---

## ⚡ Otomatik Kurulum (Batch Dosyası)

Proje klasöründe `setup.bat` dosyası bulunur. Bu dosya tüm kurulum adımlarını otomatik olarak gerçekleştirir.

### setup.bat Kullanımı

1. **setup.bat dosyasını çift tıklayın** veya Komut İstemi'nden çalıştırın:
   ```bash
   setup.bat
   ```

2. **Dosya şu işlemleri otomatik yapar**:
   - Python kurulumunu kontrol eder
   - Virtual environment oluşturur (yoksa)
   - Virtual environment'ı aktif eder
   - pip'i günceller
   - Bağımlılıkları yükler
   - Migration'ları çalıştırır
   - XNavi kurulumunu kontrol eder ve kurulumu başlatır (isteğe bağlı)
   - Sunucuyu başlatır (isteğe bağlı)

### start.bat Kullanımı

Kurulum tamamlandıktan sonra, her seferinde sunucuyu başlatmak için:

1. **start.bat dosyasını çift tıklayın**

Bu dosya:
- Virtual environment'ı aktif eder
- Bağımlılıkları kontrol eder
- Migration'ları kontrol eder
- Sunucuyu başlatır

---

## 🔍 Sorun Giderme

### Problem 1: "python is not recognized"

**Çözüm**:
- Python'un PATH'e eklendiğinden emin olun
- Yeni bir CMD penceresi açın
- `py` komutunu deneyin: `py --version`

### Problem 2: "pip is not recognized"

**Çözüm**:
- Python kurulumunda pip'in yüklendiğinden emin olun
- `python -m pip --version` komutunu deneyin
- Virtual environment içinde pip kullanın

### Problem 3: "ModuleNotFoundError: No module named 'django'"

**Çözüm**:
- Virtual environment'ın aktif olduğundan emin olun (komut satırında `(venv)` görünmeli)
- `pip install -r requirements.txt` komutunu tekrar çalıştırın

### Problem 4: "Port 8000 is already in use"

**Çözüm**:
- Farklı bir port kullanın: `python manage.py runserver 8001`
- 8000 portunu kullanan uygulamayı kapatın:
  ```bash
  netstat -ano | findstr :8000
  taskkill /PID <PID_NUMARASI> /F
  ```

### Problem 5: "Migration hatası"

**Çözüm**:
- `db.sqlite3` dosyasını silin (dikkat: tüm veriler silinir!)
- `python manage.py migrate` komutunu tekrar çalıştırın

### Problem 6: "Virtual environment aktif olmuyor"

**Çözüm**:
- CMD kullanıyorsanız: `venv\Scripts\activate.bat`
- PowerShell kullanıyorsanız:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  venv\Scripts\Activate.ps1
  ```

### Problem 7: "Git clone çalışmıyor"

**Çözüm**:
- Git'in yüklü olduğundan emin olun
- GitHub'dan ZIP olarak indirin
- ZIP dosyasını çıkarın

### Problem 8: "Bağımlılıklar yüklenirken hata"

**Çözüm**:
- İnternet bağlantınızı kontrol edin
- pip'i güncelleyin: `python -m pip install --upgrade pip`
- Proxy/firewall ayarlarınızı kontrol edin
- Tek tek yüklemeyi deneyin:
  ```bash
  pip install Django
  pip install djangorestframework
  pip install django-cors-headers
  pip install requests
  ```

---

## ✅ Kurulum Kontrol Listesi

Kurulumun başarılı olduğunu doğrulamak için:

- [ ] Python 3.8+ yüklü (`python --version`)
- [ ] pip yüklü (`pip --version`)
- [ ] Proje klasörüne gidildi
- [ ] Virtual environment oluşturuldu (`venv` klasörü var)
- [ ] Virtual environment aktif (`(venv)` komut satırında görünüyor)
- [ ] Bağımlılıklar yüklendi (`pip list` ile kontrol)
- [ ] Migration'lar çalıştırıldı (`db.sqlite3` dosyası var)
- [ ] XNavi kuruldu (USB-4751L donanımı kullanılacaksa zorunlu)
- [ ] Sunucu başlatıldı (`http://127.0.0.1:8000/` erişilebilir)

---

## 📝 Sonraki Adımlar

Kurulum tamamlandıktan sonra:

1. **API Dokümantasyonunu İnceleyin**: `docs/api-reference.md`
2. **Hızlı Başlangıç Kılavuzunu Takip Edin**: `docs/quick-start.md`
3. **Postman Collection'ı İndirin**: `LumaServer API.postman_collection.json`

---

## 🆘 Yardım ve Destek

Sorun yaşarsanız:

1. **README.md** dosyasını kontrol edin
2. **Sorun Giderme** bölümünü inceleyin
3. **GitHub Issues** sayfasında benzer sorunları arayın
4. **Yeni bir issue** açın

---

## 📚 Ek Kaynaklar

- [Django Dokümantasyonu](https://docs.djangoproject.com/)
- [Django REST Framework Dokümantasyonu](https://www.django-rest-framework.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Windows'ta Python Kurulumu](https://docs.python.org/3/using/windows.html)

---

**Son Güncelleme**: 2024
