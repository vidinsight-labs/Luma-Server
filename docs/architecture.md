# Sistem Mimarisi

Bu dokümantasyon, Luma-Server sisteminin mimari yapısını, bileşenlerini ve çalışma prensiplerini açıklar.

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Sistem Bileşenleri](#sistem-bileşenleri)
- [Mimari Katmanlar](#mimari-katmanlar)
- [Veri Akışı](#veri-akışı)
- [Teknoloji Stack](#teknoloji-stack)
- [Veritabanı Şeması](#veritabanı-şeması)

---

## Genel Bakış

Luma-Server, çoklu kamera ve flash kontrolü için tasarlanmış bir Django REST API sunucusudur. Sistem, merkezi bir sunucu üzerinden Raspberry Pi cihazlarını yönetir ve Advantech USB-4751L donanımı ile kamera/flash tetikleme yapar.

### Sistem Mimarisi Diyagramı

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Uygulaması                      │
│              (React, Vue, Angular, vb.)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       │ (JSON)
┌──────────────────────▼──────────────────────────────────────┐
│                  Luma-Server (Django)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Layer (Django REST Framework)                   │  │
│  │  - Project Views                                     │  │
│  │  - Collection Views                                  │  │
│  │  - File Views                                        │  │
│  │  - Device Views                                      │  │
│  │  - Setting Views                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                                │  │
│  │  - Serializers                                       │  │
│  │  - Utils (PiRequests, CamTrigger)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Data Layer                                          │  │
│  │  - Models (Project, Collection, File, Device, etc.) │  │
│  │  - SQLite Database                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌──── ▼──────────────┐
│ Raspberry Pi │ │ Raspberry  │ │  USB-4751LHardware │
│   Device 1   │ │   Pi 2     │ │   (Tetik Kutusu)   │
│              │ │            │ │                    │
│  - Cameras   │ │ - Cameras  │ │ - Camera Trigger   │
│  - API       │ │ - API      │ │ - Flash Trigger    │  
│  - Storage   │ │ - Storage  │ │                    │
└──────────────┘ └────────────┘ └────────────────────┘ 
                                
```

---

## Sistem Bileşenleri

### 1. API Katmanı (Django REST Framework)

**Konum:** `api/views/`

**Sorumluluklar:**
- HTTP isteklerini işleme
- Request/Response validasyonu
- HTTP status kodları yönetimi
- Endpoint routing

**Bileşenler:**
- `ProjectViews/` - Proje yönetimi
- `CollectionViews/` - Collection yönetimi
- `FileViews/` - Dosya yönetimi
- `DeviceViews/` - Cihaz yönetimi
- `SettingViews/` - Ayar yönetimi

### 2. Business Logic Katmanı

**Konum:** `api/serializers/`, `api/utils/`

**Sorumluluklar:**
- Veri serileştirme/deserileştirme
- Cihaz iletişimi (HTTP istekleri)
- Donanım kontrolü (USB-4751L)
- Paralel işlem yönetimi

**Bileşenler:**
- **Serializers:** Model ↔ JSON dönüşümü
- **PiRequests:** Raspberry Pi cihazları ile HTTP iletişimi
- **CamTrigger:** USB-4751L donanım kontrolü

### 3. Veri Katmanı

**Konum:** `api/models/`

**Sorumluluklar:**
- Veri modelleme
- Veritabanı işlemleri
- İlişkisel veri yönetimi

**Modeller:**
- `Project` - Proje bilgileri
- `Collection` - Collection bilgileri (Project'e bağlı)
- `File` - Dosya bilgileri (Collection'a bağlı)
- `Device` - Cihaz bilgileri
- `CameraSetting` - Kamera ayarları (Singleton)
- `FlashSetting` - Flash ayarları (Singleton)

### 4. Cihaz Katmanı (Raspberry Pi)

**Sorumluluklar:**
- Kamera bağlantı yönetimi
- Fotoğraf çekimi
- Fotoğraf depolama
- API endpoint'leri sağlama

**Gerekli Endpoint'ler:**
- `GET /api/get-device-data` - Cihaz bilgileri
- `GET /api/get-photo-list` - Fotoğraf listesi
- `POST /api/set-device-settings` - Kamera ayarları
- `DELETE /api/delete-all-photos` - Fotoğrafları sil
- `GET /api/disconnect-all` - Kameraları bağlantıdan kes
- `GET /api/connect-all` - Kameraları bağla
- `GET /api/reset-camera` - Kamerayı resetle

### 5. Donanım Katmanı (USB-4751L)

**Konum:** `api/utils/CamTrigger.py`

**Sorumluluklar:**
- Kamera tetikleme
- Flash tetikleme
- Senkronize tetikleme

**Özellikler:**
- Windows DLL entegrasyonu (Advantech BDaq SDK)
- Bit bazlı dijital output kontrolü
- Zamanlama kontrolü (delay, duration)

---

## Mimari Katmanlar

### Katman 1: Presentation Layer (Frontend)

- Kullanıcı arayüzü
- API istekleri
- Veri görselleştirme

### Katman 2: API Layer

- RESTful endpoint'ler
- Request/Response işleme
- Hata yönetimi

### Katman 3: Business Logic Layer

- İş mantığı
- Cihaz iletişimi
- Donanım kontrolü
- Paralel işlem yönetimi

### Katman 4: Data Layer

- Veritabanı işlemleri
- Model yönetimi
- Veri doğrulama

### Katman 5: Device Layer

- Raspberry Pi cihazları
- Kamera kontrolü
- Fotoğraf yönetimi

### Katman 6: Hardware Layer

- USB-4751L donanımı
- Dijital I/O kontrolü

---

## Veri Akışı

### Senaryo 1: Collection Oluşturma ve Fotoğraf Toplama

```
1. Frontend → POST /api/create-collection/<project_id>
   └─ Request: { "name": "Collection 1" }

2. API Layer → CreateCollection View
   ├─ Collection modeli oluştur
   ├─ Klasör oluştur
   └─ Business Logic'e geç

3. Business Logic
   ├─ FlashSetting.get_settings() → Flash delay al
   ├─ CamTrigger.trigger(delay) → Donanımı tetikle
   │   └─ USB-4751L → Kamera/Flash sinyalleri
   ├─ PiRequests.get_photo_list(devices) → Tüm cihazlardan foto listesi
   │   └─ ThreadPoolExecutor → Paralel HTTP istekleri
   │       ├─ Device 1 → GET /api/get-photo-list
   │       └─ Device 2 → GET /api/get-photo-list
   └─ Her fotoğraf için:
       ├─ PiRequests.get_device_photo(url) → Fotoğraf indir
       ├─ Dosya sistemine kaydet
       └─ File modeli oluştur

4. Response → Frontend
   └─ { "status": {...}, "data": {...} }
```

### Senaryo 2: Kamera Ayarlarını Güncelleme

```
1. Frontend → PATCH /api/update-camera-setting
   └─ Request: { "iso_speed": "400", "shutter_speed": "1/60" }

2. API Layer → UpdateCameraSetting View
   ├─ CameraSetting.get_settings() → Singleton ayarları al
   ├─ Serializer ile validasyon
   └─ Veritabanında güncelle

3. Business Logic
   └─ PiRequests.set_device_settings(devices, settings)
       └─ ThreadPoolExecutor → Paralel HTTP istekleri
           ├─ Device 1 → POST /api/set-device-settings
           └─ Device 2 → POST /api/set-device-settings

4. Response → Frontend
   └─ { "status": {...}, "data": {...}, "device_responses": [...] }
```

### Senaryo 3: Cihaz Ekleme

```
1. Frontend → POST /api/add-device
   └─ Request: { "name": "Raspberry Pi 1", "ip": "192.168.1.100" }

2. API Layer → AddDevice View
   ├─ Validasyon (name, ip)
   └─ Business Logic'e geç

3. Business Logic
   └─ PiRequests.get_device_data(ip)
       └─ HTTP GET → http://192.168.1.100/api/get-device-data
           └─ Response: { "device": {...}, "cameras": {...} }

4. Data Layer
   └─ Device.objects.create(...) → Veritabanına kaydet

5. Response → Frontend
   └─ { "status": {...}, "data": {...} }
```

---

## Teknoloji Stack

### Backend

| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| Python | 3.8+ | Ana programlama dili |
| Django | 5.2.7 | Web framework |
| Django REST Framework | - | REST API framework |
| django-cors-headers | - | CORS yönetimi |
| requests | - | HTTP istekleri |
| ctypes | - | DLL entegrasyonu (Windows) |

### Veritabanı

| Teknoloji | Kullanım |
|-----------|----------|
| SQLite | Geliştirme (varsayılan) |
| PostgreSQL/MySQL | Production (önerilen) |

### Donanım

| Bileşen | Kullanım |
|---------|----------|
| Advantech USB-4751L | Kamera/Flash tetikleme |
| BDaq SDK | Windows DLL |

### Cihazlar

| Bileşen | Kullanım |
|---------|----------|
| Raspberry Pi | Cihaz yönetimi |
| Canon/Nikon Kameralar | Fotoğraf çekimi |

---

## Veritabanı Şeması

### İlişki Diyagramı

```
Project (1) ────< (N) Collection (1) ────< (N) File

Device (N) ────< (1) CameraSetting (Singleton)
Device (N) ────< (1) FlashSetting (Singleton)
```

### Model Detayları

#### Project
- `id` (Primary Key)
- `name` (CharField, unique)
- `path` (CharField)
- `created_at` (DateTimeField)

#### Collection
- `id` (Primary Key)
- `name` (CharField)
- `path` (CharField)
- `project` (ForeignKey → Project)
- `created_at` (DateTimeField)

#### File
- `id` (Primary Key)
- `name` (CharField)
- `path` (CharField)
- `size` (IntegerField)
- `collection` (ForeignKey → Collection)
- `created_at` (DateTimeField)

#### Device
- `id` (Primary Key)
- `name` (CharField, unique)
- `ip` (CharField, unique)
- `device_id` (CharField)
- `cameras` (JSONField)
- `statistics` (JSONField)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

#### CameraSetting (Singleton)
- `id` (Primary Key, always 1)
- `iso_speed` (CharField, choices)
- `shutter_speed` (CharField, choices)
- `aperture` (CharField, choices)
- `white_balance` (CharField, choices)
- `image_format` (CharField, choices)
- `drive_mode` (CharField, choices)
- `metering_mode` (CharField, choices)
- `picture_style` (CharField, choices)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

#### FlashSetting (Singleton)
- `id` (Primary Key, always 1)
- `delay` (IntegerField, milliseconds)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

---

## Güvenlik Mimarisi

### Mevcut Durum

- ❌ Authentication yok
- ❌ Authorization yok
- ✅ CORS desteği (django-cors-headers)
- ⚠️ CSRF koruması (varsayılan Django)

### Production Önerileri

1. **Authentication:**
   - JWT token authentication
   - Session-based authentication
   - API key authentication

2. **Authorization:**
   - Role-based access control (RBAC)
   - Permission system

3. **HTTPS:**
   - SSL/TLS sertifikası
   - Güvenli iletişim

4. **Rate Limiting:**
   - API rate limiting
   - DDoS koruması

---

## Performans Optimizasyonları

### Mevcut Optimizasyonlar

1. **Paralel İşlemler:**
   - ThreadPoolExecutor ile cihaz işlemleri
   - Maksimum 10 thread

2. **Veritabanı:**
   - SQLite (küçük ölçek için yeterli)
   - Index'ler (Django otomatik)

### Önerilen Optimizasyonlar

1. **Caching:**
   - Redis cache
   - Device listesi cache
   - Settings cache

2. **Database:**
   - PostgreSQL (büyük ölçek)
   - Connection pooling
   - Query optimization

3. **Async Operations:**
   - Celery ile background tasks
   - Fotoğraf indirme async

---

## Ölçeklenebilirlik

### Mevcut Limitler

- **Cihaz Sayısı:** Sınırsız (ThreadPoolExecutor max 10 thread)
- **Fotoğraf Boyutu:** Dosya sistemi limiti
- **Eşzamanlı İstek:** Django varsayılan limitleri

### Ölçeklendirme Stratejileri

1. **Horizontal Scaling:**
   - Load balancer
   - Multiple server instances

2. **Database Scaling:**
   - Read replicas
   - Sharding

3. **File Storage:**
   - Cloud storage (S3, Azure Blob)
   - CDN entegrasyonu

---

## Hata Yönetimi

### Hata Seviyeleri

1. **API Level:**
   - HTTP 200 OK (her zaman)
   - Status code (0 = success, 1+ = error)

2. **Business Logic Level:**
   - Exception handling
   - Error logging

3. **Device Level:**
   - Connection errors
   - Timeout handling
   - Retry mechanism

### Hata Akışı

```
Exception → Business Logic → API View → Response
                                    ↓
                            { "status": { "code": 1, "message": "..." } }
```

---

## Monitoring ve Logging

### Önerilen Monitoring

1. **Application Monitoring:**
   - Django logging
   - Error tracking (Sentry)

2. **System Monitoring:**
   - Server metrics
   - Database performance

3. **API Monitoring:**
   - Request/Response logging
   - Performance metrics

---

## Deployment Mimarisi

### Geliştirme Ortamı

```
Developer Machine
  └─ Django Development Server (runserver)
      └─ SQLite Database
```

### Production Ortamı (Önerilen)

```
Load Balancer
  ├─ Django Server 1 (Gunicorn/uWSGI)
  ├─ Django Server 2 (Gunicorn/uWSGI)
  └─ Django Server N (Gunicorn/uWSGI)
      └─ PostgreSQL Database (Primary)
          └─ PostgreSQL Database (Replica)
```

---

## Sonuç

Luma-Server, modüler ve ölçeklenebilir bir mimariye sahiptir. Katmanlı yapısı sayesinde bakım ve geliştirme kolaydır. Production ortamında güvenlik ve performans iyileştirmeleri yapılmalıdır.

