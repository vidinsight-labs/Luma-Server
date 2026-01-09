@echo off
setlocal enabledelayedexpansion
echo ========================================
echo    Luma-Server Hizli Baslatma
echo ========================================
echo.

REM Python'un yuklu olup olmadigini kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi! Lutfen Python 3.8+ yukleyin.
    pause
    exit /b 1
)

echo [1/6] Python versiyonu kontrol ediliyor...
python --version
echo.

REM manage.py dosyasının varlığını kontrol et
if not exist "manage.py" (
    echo [HATA] manage.py bulunamadi! Lutfen proje klasorunde calistirdiginizdan emin olun.
    pause
    exit /b 1
)

REM Virtual environment kontrolu
if exist "venv\" (
    echo [2/6] Virtual environment zaten mevcut.
    set VENV_EXISTS=1
) else (
    echo [2/6] Virtual environment olusturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo [HATA] Virtual environment olusturulamadi!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment olusturuldu.
    set VENV_EXISTS=0
)
echo.

REM Virtual environment'i aktif et
echo [3/6] Virtual environment aktif ediliyor...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [HATA] Virtual environment aktif edilemedi!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment aktif.
) else (
    echo [HATA] Virtual environment script bulunamadi!
    pause
    exit /b 1
)
echo.

REM Bağımlılıkları kontrol et ve yükle
echo [4/6] Bagimliliklari kontrol ediliyor...
if exist "requirements.txt" (
    REM Sadece eksik paketleri yükle (mevcut paketlere dokunma)
    pip install -r requirements.txt --quiet --upgrade-strategy only-if-needed
    if errorlevel 1 (
        echo [UYARI] Bazı bagimliliklar yuklenemedi! Devam ediliyor...
    ) else (
        echo [OK] Bagimliliklar hazir.
    )
) else (
    echo [UYARI] requirements.txt bulunamadi! Bagimliliklar yuklenmeyecek.
)
echo.

REM Veritabanı migration kontrolü
echo [5/6] Veritabani hazirlaniyor...
REM Sadece yeni migration'ları uygula (mevcut veritabanına dokunma)
python manage.py migrate --no-input
if errorlevel 1 (
    echo [UYARI] Veritabani migration hatasi! Mevcut veritabani korunuyor, devam ediliyor...
) else (
    echo [OK] Veritabani hazir.
)
echo.

REM Port kontrolü (opsiyonel - 8000 portu kullanılıyorsa uyarı)
echo [6/6] Port kontrolu yapiliyor...
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [UYARI] Port 8000 zaten kullaniliyor olabilir!
    echo [UYARI] Sunucu baslatilirken hata alirsaniz, baska bir port kullanin:
    echo [UYARI] python manage.py runserver 8001
    echo.
)
echo.

echo ========================================
echo    Sunucu baslatiliyor...
echo    Tarayicinizda acin: http://127.0.0.1:8000
echo    Durdurmak icin: Ctrl+C
echo ========================================
echo.

REM Sunucuyu başlat
python manage.py runserver

pause

