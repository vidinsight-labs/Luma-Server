# Sistem Çalışma Mantığı

Bu dokümantasyon, Luma-Server sisteminin çalışma mantığını, veri akışını ve işlem süreçlerini detaylı olarak açıklar.

## 📋 İçindekiler

- [Genel Çalışma Mantığı](#genel-çalışma-mantığı)
- [Temel İşlem Akışları](#temel-işlem-akışları)
- [Paralel İşlem Yönetimi](#paralel-işlem-yönetimi)
- [Donanım Kontrolü](#donanım-kontrolü)
- [Hata Yönetimi](#hata-yönetimi)
- [Veri Senkronizasyonu](#veri-senkronizasyonu)

---

## Genel Çalışma Mantığı

Luma-Server, merkezi bir kontrol noktası olarak çalışır ve aşağıdaki prensiplere göre işler:

1. **Merkezi Yönetim:** Tüm cihazlar ve ayarlar merkezi sunucudan yönetilir
2. **Paralel İşlemler:** Çoklu cihaz işlemleri paralel olarak yürütülür
3. **Singleton Ayarlar:** Kamera ve flash ayarları tek bir instance olarak saklanır
4. **Otomatik Tetikleme:** Collection oluşturulurken otomatik fotoğraf çekimi yapılır

---

## Temel İşlem Akışları

### 1. Sistem Başlatma Akışı

```
1. Django Sunucusu Başlatılır
   └─ settings.py yüklenir
   └─ URL routing yapılandırılır
   └─ Middleware zinciri oluşturulur

2. İlk İstek Geldiğinde
   └─ CameraSetting.get_settings() → Singleton oluşturulur (varsayılan değerler)
   └─ FlashSetting.get_settings() → Singleton oluşturulur (delay=0)

3. Veritabanı Hazır
   └─ Migration'lar uygulanmış olmalı
   └─ SQLite dosyası hazır
```

### 2. Cihaz Ekleme Akışı

```
Frontend → POST /api/add-device
    │
    ├─ Request: { "name": "...", "ip": "..." }
    │
    ▼
AddDevice View
    │
    ├─ Validasyon (name, ip eksik mi?)
    ├─ Benzersizlik kontrolü (name, ip zaten var mı?)
    │
    ▼
PiRequests.get_device_data(ip)
    │
    ├─ HTTP GET → http://{ip}/api/get-device-data
    │   └─ Response: { "device": {...}, "cameras": {...} }
    │
    ▼
Device.objects.create(...)
    │
    ├─ Veritabanına kaydet
    ├─ cameras JSONField → Cihazdan gelen kamera bilgileri
    ├─ statistics JSONField → Cihaz istatistikleri
    │
    ▼
Response → Frontend
    └─ { "status": {...}, "data": {...} }
```

### 3. Collection Oluşturma ve Fotoğraf Çekimi Akışı

```
Frontend → POST /api/create-collection/<project_id>
    │
    ├─ Request: { "name": "Collection 1" }
    │
    ▼
CreateCollection View
    │
    ├─ Project kontrolü (var mı?)
    ├─ Collection adı benzersizlik kontrolü
    ├─ Klasör oluştur (projects/{project_name}/{collection_name})
    │
    ▼
Collection.objects.create(...)
    │
    ├─ Veritabanına kaydet
    │
    ▼
FlashSetting.get_settings()
    │
    ├─ Flash delay değerini al (milisaniye)
    │
    ▼
CamTrigger.trigger(delay)
    │
    ├─ USB4751L_DigitalOutput("USB-4751L")
    ├─ initialize() → Cihazı başlat
    │
    ├─ camera_on() → Bit 1'i temizle (0xFD)
    ├─ time.sleep(delay / 1000) → Flash gecikmesi
    ├─ flash_on() → Bit 2'yi temizle (0xFB)
    ├─ time.sleep(0.2) → Flash süresi (200ms)
    ├─ flash_off() → Bit 2'yi set et (0x04)
    ├─ time.sleep(0.8) → Kalan kamera süresi
    ├─ camera_off() → Bit 1'i set et (0x02)
    ├─ reset_all() → Tüm bitleri 0xFF yap
    └─ close() → Cihazı kapat
    │
    ▼
PiRequests.get_photo_list(devices)
    │
    ├─ ThreadPoolExecutor(max_workers=10)
    │   │
    │   ├─ Thread 1: Device 1 → GET /api/get-photo-list
    │   ├─ Thread 2: Device 2 → GET /api/get-photo-list
    │   ├─ Thread 3: Device 3 → GET /api/get-photo-list
    │   └─ ... (tüm cihazlar paralel)
    │
    ├─ Tüm thread'ler tamamlanana kadar bekle
    ├─ Tüm fotoğraf listelerini birleştir
    │
    ▼
Her fotoğraf için:
    │
    ├─ PiRequests.get_device_photo(download_url)
    │   └─ HTTP GET → Fotoğrafı indir
    │
    ├─ Dosya sistemine kaydet
    │   └─ {collection_path}/{filename}
    │
    └─ File.objects.create(...)
        └─ Veritabanına kaydet
    │
    ▼
Response → Frontend
    └─ { "status": {...}, "data": {...} }
```

### 4. Kamera Ayarlarını Güncelleme Akışı

```
Frontend → PATCH /api/update-camera-setting
    │
    ├─ Request: { "iso_speed": "400", "shutter_speed": "1/60" }
    │
    ▼
UpdateCameraSetting View
    │
    ├─ CameraSetting.get_settings() → Singleton ayarları al
    │
    ▼
CameraSettingSerializer
    │
    ├─ Partial update (sadece gönderilen alanlar)
    ├─ Validasyon (geçerli değerler mi?)
    │
    ▼
settings.save()
    │
    ├─ Veritabanında güncelle
    │
    ▼
Device.objects.all()
    │
    ├─ Tüm cihazları al
    │
    ▼
PiRequests.set_device_settings(devices, settings)
    │
    ├─ ThreadPoolExecutor(max_workers=10)
    │   │
    │   ├─ Thread 1: Device 1 → POST /api/set-device-settings
    │   │   └─ Request: { "iso": "400", "shutterspeed": "1/60", ... }
    │   ├─ Thread 2: Device 2 → POST /api/set-device-settings
    │   └─ ... (tüm cihazlar paralel)
    │
    ├─ Tüm thread'ler tamamlanana kadar bekle
    ├─ Her cihazdan gelen response'ları topla
    │
    ▼
Response → Frontend
    └─ {
        "status": {...},
        "data": {
            ...settings,
            "device_responses": [...]
        }
    }
```

### 5. Cihaz Listesi Getirme Akışı

```
Frontend → GET /api/get-device-list
    │
    ▼
GetDeviceList View
    │
    ├─ Device.objects.all() → Tüm cihazları al
    │
    ▼
Her cihaz için:
    │
    ├─ PiRequests.get_device_data(device.ip)
    │   └─ HTTP GET → http://{ip}/api/get-device-data
    │       └─ Response: { "device": {...}, "cameras": {...} }
    │
    ├─ device.cameras = response.get("cameras")
    ├─ device.statistics = response.get("device").get("statistics")
    │
    └─ device.save() → Güncelle
    │
    ▼
DeviceSerializer(devices, many=True)
    │
    ├─ Tüm cihazları JSON'a çevir
    │
    ▼
Response → Frontend
    └─ { "status": {...}, "data": [...] }
```

---

## Paralel İşlem Yönetimi

### ThreadPoolExecutor Kullanımı

Sistem, çoklu cihaz işlemlerinde `ThreadPoolExecutor` kullanır:

```python
from concurrent.futures import ThreadPoolExecutor

def process_devices_parallel(devices, function):
    results = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(function, device) 
            for device in devices
        ]
        
        for future in futures:
            result = future.result()  # Tüm thread'ler bitene kadar bekler
            results.append(result)
    
    return results
```

### Paralel İşlem Senaryoları

1. **Fotoğraf Listesi Toplama:**
   - Her cihazdan paralel olarak fotoğraf listesi çekilir
   - Maksimum 10 thread aynı anda çalışır

2. **Ayar Gönderme:**
   - Tüm cihazlara paralel olarak ayarlar gönderilir
   - Her cihazın yanıtı beklenir

3. **Kameraları Yeniden Bağlama:**
   - Tüm cihazlarda paralel olarak reconnect işlemi yapılır

### Thread Güvenliği

- Her thread kendi device objesi ile çalışır
- Veritabanı işlemleri Django ORM tarafından yönetilir (thread-safe)
- HTTP istekleri `requests` kütüphanesi ile yapılır (thread-safe)

---

## Donanım Kontrolü

### USB-4751L Kontrol Akışı

```
trigger(delay) çağrılır
    │
    ▼
USB4751L_DigitalOutput("USB-4751L")
    │
    ├─ _load_dll() → BDaq DLL'ini yükle
    │   └─ Olası konumlar:
    │       ├─ biodaq.dll
    │       ├─ C:\Program Files\Advantech\DAQNavi\Bin\biodaq.dll
    │       └─ C:\Windows\System32\biodaq.dll
    │
    ├─ _setup_function_signatures() → C API fonksiyon imzaları
    │
    ▼
initialize()
    │
    ├─ find_device_by_name("USB-4751L") → Cihazı bul
    ├─ AdxDeviceOpen() → Cihazı aç
    ├─ AdxDeviceGetModuleHandle() → DIO modül handle'ı al
    └─ reset_all() → Başlangıç sinyali (0xFF)
    │
    ▼
Kamera/Flash Tetikleme
    │
    ├─ camera_on() → Bit 1 = 0 (0xFD)
    │   └─ AdxDoWritePorts(module_handle, 0, 1, 0xFD)
    │
    ├─ time.sleep(delay / 1000) → Flash gecikmesi
    │
    ├─ flash_on() → Bit 2 = 0 (0xFB)
    │   └─ AdxDoWritePorts(module_handle, 0, 1, 0xFB)
    │
    ├─ time.sleep(0.2) → Flash süresi (200ms)
    │
    ├─ flash_off() → Bit 2 = 1 (0x04)
    │   └─ AdxDoWritePorts(module_handle, 0, 1, 0x04)
    │
    ├─ time.sleep(0.8) → Kalan kamera süresi
    │
    ├─ camera_off() → Bit 1 = 1 (0x02)
    │   └─ AdxDoWritePorts(module_handle, 0, 1, 0x02)
    │
    └─ reset_all() → Tüm bitler = 1 (0xFF)
        └─ AdxDoWritePorts(module_handle, 0, 1, 0xFF)
    │
    ▼
close()
    │
    └─ AdxDeviceClose(device_handle) → Cihazı kapat
```

### Bit Manipülasyonu

```
Port 0 Byte Değeri: 0xFF (11111111)

Bit 1 (Kamera): 0 = AÇIK, 1 = KAPALI
Bit 2 (Flash):  0 = AÇIK, 1 = KAPALI

camera_on():  0xFF & 0xFD = 0xFD (11111101) → Bit 1 = 0
camera_off(): 0xFF | 0x02 = 0xFF (11111111) → Bit 1 = 1

flash_on():   0xFF & 0xFB = 0xFB (11111011) → Bit 2 = 0
flash_off():  0xFF | 0x04 = 0xFF (11111111) → Bit 2 = 1
```

---

## Hata Yönetimi

### Hata Seviyeleri

1. **API Level:**
   - Tüm endpoint'ler HTTP 200 OK döner
   - Hata durumları `status.code` ile belirtilir
   - `code: 0` = başarılı, `code: 1+` = hata

2. **Business Logic Level:**
   - Exception handling ile hatalar yakalanır
   - Hata mesajları response'a eklenir
   - İşlem devam edebilir veya durdurulabilir

3. **Device Level:**
   - Connection errors → `status: "error"` döner
   - Timeout → Exception fırlatılır
   - Her cihaz için ayrı hata yönetimi

### Hata Akış Örnekleri

#### Senaryo 1: Cihaz Bağlantı Hatası

```
PiRequests.get_device_data(ip)
    │
    ├─ requests.get() → Connection timeout
    │
    ▼
Exception yakalanır
    │
    └─ AddDevice View → Hata response döner
        └─ { "status": { "code": 1, "message": "..." } }
```

#### Senaryo 2: Paralel İşlemde Kısmi Hata

```
PiRequests.set_device_settings(devices, settings)
    │
    ├─ Thread 1: Device 1 → Success
    ├─ Thread 2: Device 2 → Connection Error
    └─ Thread 3: Device 3 → Success
    │
    ▼
device_responses = [
    { "status": "success", ... },
    { "status": "error", "error": "Connection timeout" },
    { "status": "success", ... }
]
    │
    ▼
Response → Frontend
    └─ {
        "status": { "code": 0, "message": "update success" },
        "data": {
            ...settings,
            "device_responses": [...]  // Hatalı cihaz da dahil
        }
    }
```

---

## Veri Senkronizasyonu

### Singleton Pattern

**CameraSetting ve FlashSetting** singleton pattern kullanır:

```python
@classmethod
def get_settings(cls):
    settings, created = cls.objects.get_or_create(pk=1)
    return settings
```

**Avantajları:**
- Tek bir ayar kaydı garantisi
- Tüm sistem aynı ayarları kullanır
- Güncelleme tüm sistemde geçerli olur

### Cihaz Veri Senkronizasyonu

**Senkronizasyon Noktaları:**

1. **Cihaz Eklendiğinde:**
   - Cihazdan güncel bilgiler çekilir
   - Veritabanına kaydedilir

2. **Cihaz Listesi İstendiğinde:**
   - Tüm cihazlardan güncel bilgiler çekilir
   - Veritabanı güncellenir

3. **Ayar Güncellendiğinde:**
   - Veritabanında güncellenir
   - Tüm cihazlara gönderilir

---

## Zamanlama ve Sıralama

### Collection Oluşturma Zamanlaması

```
t=0ms:     Collection oluşturulmaya başlanır
t=10ms:    FlashSetting.get_settings() → delay değeri alınır
t=20ms:    CamTrigger.trigger(delay) başlar
t=30ms:    camera_on() → Kamera AÇIK
t=30+delay: flash_on() → Flash AÇIK
t=30+delay+200ms: flash_off() → Flash KAPALI
t=30+delay+1000ms: camera_off() → Kamera KAPALI
t=1050ms:  Fotoğraf listesi toplama başlar (paralel)
t=2000ms:  Fotoğraflar indirilmeye başlar
t=5000ms:  Tüm fotoğraflar kaydedilir
t=5100ms:  Response döner
```

### Paralel İşlem Zamanlaması

```
Sequential (Sıralı):
  Device 1: 500ms
  Device 2: 500ms
  Device 3: 500ms
  Total: 1500ms

Parallel (Paralel):
  Device 1: 500ms ┐
  Device 2: 500ms ├─ Aynı anda
  Device 3: 500ms ┘
  Total: 500ms (3x daha hızlı)
```

---

## Önbellekleme ve Optimizasyon

### Mevcut Durum

- ❌ Caching yok
- ✅ Paralel işlemler (ThreadPoolExecutor)
- ✅ Singleton ayarlar (tek sorgu)

### Önerilen Optimizasyonlar

1. **Device List Cache:**
   - Cihaz listesi 30 saniye cache'lenebilir
   - Redis veya in-memory cache

2. **Settings Cache:**
   - Ayarlar cache'lenebilir
   - Güncelleme sonrası cache invalidate

3. **Photo List Cache:**
   - Fotoğraf listeleri kısa süre cache'lenebilir
   - Yeni collection sonrası invalidate

---

## Sonuç

Luma-Server, merkezi kontrol ve paralel işlem prensiplerine dayalı olarak çalışır. Sistem, çoklu cihaz yönetimi ve donanım kontrolü için optimize edilmiştir. Hata yönetimi ve veri senkronizasyonu güvenilir bir şekilde yapılandırılmıştır.

