@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo    Luma-Server Otomatik Kurulum
echo ========================================
echo.

REM Renk kodları (Windows 10+)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

REM Python'un yuklu olup olmadigini kontrol et
echo [1/9] Python kurulumu kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[HATA] Python bulunamadi!%RESET%
    echo.
    echo Lutfen Python 3.8+ yukleyin:
    echo 1. https://www.python.org/downloads/ adresine gidin
    echo 2. Python'u indirin ve yukleyin
    echo 3. Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin
    echo 4. Bu script'i tekrar calistirin
    echo.
    pause
    exit /b 1
)

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

REM Virtual environment kontrolu ve olusturma
echo [2/9] Virtual environment kontrol ediliyor...
if exist "venv\" (
    echo %YELLOW%[BILGI] Virtual environment zaten mevcut%RESET%
) else (
    echo [BILGI] Virtual environment olusturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo %RED%[HATA] Virtual environment olusturulamadi!%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%[OK] Virtual environment olusturuldu%RESET%
)
echo.

REM Virtual environment'i aktif et
echo [3/9] Virtual environment aktif ediliyor...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo %RED%[HATA] Virtual environment aktif edilemedi!%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%[OK] Virtual environment aktif%RESET%
) else (
    echo %RED%[HATA] Virtual environment script bulunamadi!%RESET%
    pause
    exit /b 1
)
echo.

REM pip'i guncelle
echo [4/9] pip guncelleniyor...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo %YELLOW%[UYARI] pip guncellenemedi, devam ediliyor...%RESET%
) else (
    echo %GREEN%[OK] pip guncellendi%RESET%
)
echo.

REM Bagimliliklari kontrol et ve yukle
echo [5/9] Bagimliliklari kontrol ediliyor...
if exist "requirements.txt" (
    echo [BILGI] Bagimliliklari yukleniyor (bu biraz zaman alabilir)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo %RED%[HATA] Bagimliliklar yuklenemedi!%RESET%
        echo.
        echo Lutfen asagidaki komutlari manuel olarak calistirin:
        echo   pip install Django
        echo   pip install djangorestframework
        echo   pip install django-cors-headers
        echo   pip install requests
        echo.
        pause
        exit /b 1
    )
    echo %GREEN%[OK] Bagimliliklar yuklendi%RESET%
) else (
    echo %RED%[HATA] requirements.txt bulunamadi!%RESET%
    pause
    exit /b 1
)
echo.

REM Yuklenen paketleri goster
echo [BILGI] Yuklenen paketler:
pip list | findstr /i "django djangorestframework cors requests"
echo.

REM Veritabani migration kontrolu
echo [6/9] Veritabani hazirlaniyor...
if exist "db.sqlite3" (
    echo %YELLOW%[BILGI] Veritabani dosyasi zaten mevcut%RESET%
    echo [BILGI] Yeni migration'lar uygulaniyor...
) else (
    echo [BILGI] Veritabani olusturuluyor...
)

python manage.py migrate --no-input
if errorlevel 1 (
    echo %RED%[HATA] Veritabani migration hatasi!%RESET%
    echo.
    echo Lutfen asagidaki komutu manuel olarak calistirin:
    echo   python manage.py migrate
    echo.
    pause
    exit /b 1
)
echo %GREEN%[OK] Veritabani hazir%RESET%
echo.

REM XNavi kurulum kontrolu
echo [7/9] XNavi kurulumu kontrol ediliyor...
if exist "XNavi.exe" (
    echo %GREEN%[OK] XNavi.exe bulundu%RESET%
    echo.
    echo %YELLOW%[ONEMLI] XNavi kurulumu gereklidir!%RESET%
    echo.
    echo XNavi, Advantech USB-4751L donanimi icin gerekli yapilandirma aracidir.
    echo Kamera ve flash kontrolu icin XNavi'nin kurulu olmasi gerekmektedir.
    echo.
    set /p INSTALL_XNAVI="XNavi'yi simdi kurmak ister misiniz? (E/H): "
    if /i "!INSTALL_XNAVI!"=="E" (
        echo.
        echo [BILGI] XNavi.exe baslatiliyor...
        echo [BILGI] Lutfen kurulum sihirbazini takip edin.
        echo.
        start "" "XNavi.exe"
        echo.
        echo %YELLOW%[BILGI] XNavi kurulum penceresi acildi.%RESET%
        echo [BILGI] Kurulum tamamlandiktan sonra bu pencereye donun.
        echo.
        pause
    ) else (
        echo %YELLOW%[UYARI] XNavi kurulumu atlandi.%RESET%
        echo [UYARI] XNavi'yi daha sonra manuel olarak kurmaniz gerekecektir.
        echo [UYARI] XNavi.exe dosyasini cift tiklayarak kurulumu baslatabilirsiniz.
    )
) else (
    echo %YELLOW%[UYARI] XNavi.exe bulunamadi!%RESET%
    echo [UYARI] XNavi kurulumu atlandi.
    echo [UYARI] Eger XNavi gerekiyorsa, dosyayi proje klasorune ekleyin.
)
echo.

REM Port kontrolu
echo [8/9] Port kontrolu yapiliyor...
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo %YELLOW%[UYARI] Port 8000 zaten kullaniliyor olabilir!%RESET%
    echo [UYARI] Sunucu baslatilirken hata alirsaniz, baska bir port kullanin
    echo.
)
echo.

REM Kurulum ozeti
echo ========================================
echo    Kurulum Tamamlandi!
echo ========================================
echo.
echo %GREEN%[BASARILI]%RESET% Tum adimlar basariyla tamamlandi.
echo.
echo Sonraki adimlar:
echo 1. XNavi kurulumu tamamlandiysa devam edebilirsiniz
echo 2. Sunucuyu baslatmak icin: start.bat dosyasini calistirin
echo 3. Veya manuel olarak: python manage.py runserver
echo 4. Tarayicinizda acin: http://127.0.0.1:8000/
echo.
echo Dokumantasyon: docs\windows-kurulum.md
echo XNavi kurulumu: docs\windows-kurulum.md#xnavi-kurulumu
echo.

REM Kullaniciya sunucuyu baslatmak isteyip istemedigini sor
set /p START_SERVER="Sunucuyu simdi baslatmak ister misiniz? (E/H): "
if /i "%START_SERVER%"=="E" (
    echo.
    echo ========================================
    echo    Sunucu baslatiliyor...
    echo ========================================
    echo.
    echo Tarayicinizda acin: http://127.0.0.1:8000/
    echo Durdurmak icin: Ctrl+C
    echo.
    python manage.py runserver
) else (
    echo.
    echo Kurulum tamamlandi. Sunucuyu baslatmak icin start.bat dosyasini calistirin.
)

echo.
pause
