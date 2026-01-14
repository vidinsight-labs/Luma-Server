@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo    Luma-Server Hizli Baslatma
echo ========================================
echo.

REM Renk kodları (Windows 10+)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

REM Python'un yuklu olup olmadigini kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[HATA] Python bulunamadi!%RESET%
    echo.
    echo Lutfen Python 3.8+ yukleyin veya setup.bat dosyasini calistirin.
    echo.
    pause
    exit /b 1
)

echo [1/6] Python versiyonu kontrol ediliyor...
python --version
echo %GREEN%[OK] Python bulundu%RESET%
echo.

REM manage.py dosyasinin varligini kontrol et
if not exist "manage.py" (
    echo %RED%[HATA] manage.py bulunamadi!%RESET%
    echo.
    echo Lutfen proje klasorunde calistirdiginizdan emin olun.
    echo Mevcut klasor: %CD%
    echo.
    pause
    exit /b 1
)

REM Virtual environment kontrolu
if exist "venv\" (
    echo [2/6] Virtual environment bulundu, aktif ediliyor...
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        if errorlevel 1 (
            echo %YELLOW%[UYARI] Virtual environment aktif edilemedi! Sistem Python'u kullanilacak.%RESET%
        ) else (
            echo %GREEN%[OK] Virtual environment aktif%RESET%
        )
    ) else (
        echo %YELLOW%[UYARI] Virtual environment script bulunamadi! Sistem Python'u kullanilacak.%RESET%
    )
) else (
    echo %YELLOW%[UYARI] Virtual environment bulunamadi!%RESET%
    echo [BILGI] Ilk kurulum icin setup.bat dosyasini calistirmaniz onerilir.
    echo [BILGI] Sistem Python'u kullanilacak.
)
echo.

REM Bagimliliklari kontrol et
echo [3/6] Bagimliliklari kontrol ediliyor...
if exist "requirements.txt" (
    REM Eksik paketleri kontrol et ve yukle
    pip show django >nul 2>&1
    if errorlevel 1 (
        echo [BILGI] Eksik bagimliliklar yukleniyor...
        pip install -r requirements.txt --quiet --upgrade-strategy only-if-needed
        if errorlevel 1 (
            echo %YELLOW%[UYARI] Bazı bagimliliklar yuklenemedi! Devam ediliyor...%RESET%
        ) else (
            echo %GREEN%[OK] Bagimliliklar hazir%RESET%
        )
    ) else (
        echo %GREEN%[OK] Bagimliliklar zaten yuklu%RESET%
    )
) else (
    echo %YELLOW%[UYARI] requirements.txt bulunamadi!%RESET%
)
echo.

REM Veritabani migration kontrolu
echo [4/6] Veritabani hazirlaniyor...
if not exist "db.sqlite3" (
    echo [BILGI] Veritabani olusturuluyor...
)
python manage.py migrate --no-input
if errorlevel 1 (
    echo %YELLOW%[UYARI] Veritabani migration hatasi! Devam ediliyor...%RESET%
) else (
    echo %GREEN%[OK] Veritabani hazir%RESET%
)
echo.

REM Port kontrolu
echo [5/6] Port kontrolu yapiliyor...
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo %YELLOW%[UYARI] Port 8000 zaten kullaniliyor olabilir!%RESET%
    echo [BILGI] Sunucu baslatilirken hata alirsaniz, baska bir port kullanin:
    echo [BILGI] python manage.py runserver 8001
    echo.
)
echo.

REM Sunucu bilgileri
echo [6/6] Sunucu hazirlaniyor...
echo.

echo ========================================
echo    Sunucu baslatiliyor...
echo ========================================
echo.
echo %GREEN%Tarayicinizda acin: http://127.0.0.1:8000/%RESET%
echo Durdurmak icin: Ctrl+C
echo.
echo ========================================
echo.

REM Sunucuyu baslat
python manage.py runserver

if errorlevel 1 (
    echo.
    echo %RED%[HATA] Sunucu baslatilamadi!%RESET%
    echo.
    echo Olası nedenler:
    echo - Port 8000 zaten kullaniliyor
    echo - Bagimliliklar eksik (setup.bat calistirin)
    echo - Veritabani hatasi
    echo.
)

pause

