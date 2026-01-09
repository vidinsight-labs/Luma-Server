# Hızlı Başlangıç Kılavuzu

Bu dokümantasyon, Luma-Server sistemini ilk kez kullanırken izlemeniz gereken adımları detaylı olarak açıklar. Sistem açıldığında bu adımları sırasıyla takip ederek sistemi kullanıma hazır hale getirebilirsiniz.

## 📋 İçindekiler

1. [Cihaz Tanımlama](#1-cihaz-tanımlama)
2. [Cihazları Listeleme](#2-cihazları-listeleme)
3. [Cihazlara Bağlanma (Reconnect)](#3-cihazlara-bağlanma-reconnect)
4. [Kameralara Bağlanma](#4-kameralara-bağlanma)
5. [Proje Oluşturma](#5-proje-oluşturma)
6. [Koleksiyon Oluşturma](#6-koleksiyon-oluşturma)
7. [Tüm Fotoğrafları Silme](#7-tüm-fotoğrafları-silme)
8. [Tüm Kameraları Ayarlama](#8-tüm-kameraları-ayarlama)

---

## 1. Cihaz Tanımlama

Sisteme kullanılacak cihazları (Raspberry Pi) eklemeniz gerekmektedir. Her cihaz için IP adresi ve isim belirtmelisiniz.

### Endpoint

```
POST /api/add-device
```

### Request Body

```json
{
  "name": "Raspberry Pi 1",
  "ip": "192.168.1.100"
}
```

### Parametreler

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `name` | string | Evet | Cihazın benzersiz adı |
| `ip` | string | Evet | Cihazın IP adresi (örn: "192.168.1.100") |

### Örnek Request (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/add-device \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Raspberry Pi 1",
    "ip": "192.168.1.100"
  }'
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Raspberry Pi 1",
    "ip": "192.168.1.100",
    "device_id": "001",
    "cameras": {
      "camera1": {
        "model": "Canon EOS 5D",
        "status": "connected"
      }
    },
    "statistics": {
      "total_photos": 0,
      "storage_used": "0 MB"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

### Hata Durumları

**Cihaz adı zaten mevcut:**
```json
{
  "status": {
    "code": 1,
    "message": "this device name already exists"
  },
  "data": {}
}
```

**IP adresi zaten kayıtlı:**
```json
{
  "status": {
    "code": 1,
    "message": "this device already exists"
  },
  "data": {}
}
```

**Eksik parametre:**
```json
{
  "status": {
    "code": 1,
    "message": "Missing fields: name, ip"
  },
  "data": {}
}
```

### Notlar

- Cihaz eklenirken sistem otomatik olarak cihazdan bilgi çeker (`/api/get-device-data` endpoint'i üzerinden)
- Cihaz adı ve IP adresi benzersiz olmalıdır
- Birden fazla cihaz eklemek için bu adımı tekrarlayın

---

## 2. Cihazları Listeleme

Sisteme kayıtlı tüm cihazları ve güncel durumlarını görüntüleyin.

### Endpoint

```
GET /api/get-device-list
```

### Örnek Request (cURL)

```bash
curl -X GET http://127.0.0.1:8000/api/get-device-list
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": [
    {
      "id": 1,
      "name": "Raspberry Pi 1",
      "ip": "192.168.1.100",
      "device_id": "001",
      "cameras": {
        "camera1": {
          "model": "Canon EOS 5D",
          "status": "connected"
        },
        "camera2": {
          "model": "Canon EOS 6D",
          "status": "disconnected"
        }
      },
      "statistics": {
        "total_photos": 150,
        "storage_used": "2.5 GB"
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T11:45:00Z"
    },
    {
      "id": 2,
      "name": "Raspberry Pi 2",
      "ip": "192.168.1.101",
      "device_id": "002",
      "cameras": {
        "camera1": {
          "model": "Nikon D850",
          "status": "connected"
        }
      },
      "statistics": {
        "total_photos": 75,
        "storage_used": "1.2 GB"
      },
      "created_at": "2024-01-15T10:35:00Z",
      "updated_at": "2024-01-15T11:50:00Z"
    }
  ]
}
```

### Notlar

- Bu endpoint çağrıldığında sistem tüm cihazlardan güncel bilgileri çeker
- Her cihaz için kamera durumları ve istatistikler güncellenir
- Cihaz yoksa boş array döner: `{"status": {"code": 0, "message": "success"}, "data": []}`

---

## 3. Cihazlara Bağlanma (Reconnect)

Tüm cihazlardaki kameraları yeniden bağlar. Bu işlem önce tüm kameraları bağlantıdan keser, sonra tekrar bağlar.

### Endpoint

```
POST /api/reconnect-cameras
```

### Örnek Request (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/reconnect-cameras
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "reconnect cameras request sent"
  },
  "data": {
    "device_responses": [
      {
        "device_id": 1,
        "device_name": "Raspberry Pi 1",
        "device_ip": "192.168.1.100",
        "status": "success",
        "response": {
          "cameras_connected": 2,
          "cameras_disconnected": 0
        }
      },
      {
        "device_id": 2,
        "device_name": "Raspberry Pi 2",
        "device_ip": "192.168.1.101",
        "status": "success",
        "response": {
          "cameras_connected": 1,
          "cameras_disconnected": 0
        }
      }
    ]
  }
}
```

### Hata Durumları

**Cihaz bulunamadı:**
```json
{
  "status": {
    "code": 1,
    "message": "no devices found"
  },
  "data": {}
}
```

**Cihaz bağlantı hatası:**
```json
{
  "status": {
    "code": 0,
    "message": "reconnect cameras request sent"
  },
  "data": {
    "device_responses": [
      {
        "device_id": 1,
        "device_name": "Raspberry Pi 1",
        "device_ip": "192.168.1.100",
        "status": "error",
        "error": "Connection timeout"
      }
    ]
  }
}
```

### Notlar

- Bu işlem tüm cihazlarda paralel olarak çalışır (ThreadPoolExecutor kullanılır)
- Her cihaz için `/api/disconnect-all` ve `/api/connect-all` endpoint'leri çağrılır
- İşlem tamamlanana kadar beklenir (tüm cihazların yanıtı alınır)

---

## 4. Kameralara Bağlanma

Cihazları listeledikten sonra kamera bilgileri otomatik olarak güncellenir. Kameraların bağlı olup olmadığını kontrol etmek için cihaz listesini tekrar çekebilirsiniz.

### Kamera Bilgilerini Görüntüleme

Cihaz listesini çektiğinizde her cihazın `cameras` alanında kamera bilgileri bulunur:

```json
{
  "cameras": {
    "camera1": {
      "model": "Canon EOS 5D",
      "status": "connected",
      "serial_number": "12345678"
    },
    "camera2": {
      "model": "Canon EOS 6D",
      "status": "disconnected",
      "serial_number": "87654321"
    }
  }
}
```

### Kamera Durumları

- **connected**: Kamera başarıyla bağlanmış ve kullanıma hazır
- **disconnected**: Kamera bağlantısı yok veya bağlantı hatası

### Notlar

- Kamera bilgileri cihaz listesi çekildiğinde otomatik güncellenir
- Kameralar bağlı değilse önce "Cihazlara Bağlanma" adımını tekrarlayın
- Her cihazda birden fazla kamera olabilir

---

## 5. Proje Oluşturma

Fotoğrafları organize etmek için bir proje oluşturun. Projeler, koleksiyonları ve dosyaları gruplamak için kullanılır.

### Endpoint

```
POST /api/create-project/
```

### Request Body

```json
{
  "name": "Ürün Fotoğraf Çekimi"
}
```

### Parametreler

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `name` | string | Evet | Projenin benzersiz adı |

### Örnek Request (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/create-project/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ürün Fotoğraf Çekimi"
  }'
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Ürün Fotoğraf Çekimi",
    "path": "/path/to/projects/Ürün Fotoğraf Çekimi",
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

### Hata Durumları

**Proje adı zaten mevcut:**
```json
{
  "status": {
    "code": 1,
    "message": "this project name already exists"
  },
  "data": {}
}
```

**Eksik parametre:**
```json
{
  "status": {
    "code": 1,
    "message": "Missing fields: name"
  },
  "data": {}
}
```

### Notlar

- Proje oluşturulduğunda fiziksel bir klasör de oluşturulur
- Proje adı benzersiz olmalıdır
- Proje silindiğinde içindeki tüm koleksiyonlar ve dosyalar da silinir

---

## 6. Koleksiyon Oluşturma

Koleksiyon oluşturulduğunda sistem otomatik olarak:
1. Flash ayarlarına göre kamera ve flash'ı tetikler
2. Tüm cihazlardan fotoğrafları toplar
3. Fotoğrafları koleksiyon klasörüne kaydeder
4. Veritabanına dosya kayıtlarını ekler

### Endpoint

```
POST /api/create-collection/<project_id>
```

### Request Body

```json
{
  "name": "Koleksiyon 1"
}
```

### Parametreler

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `name` | string | Evet | Koleksiyonun benzersiz adı |
| `project_id` | integer | Evet | URL parametresi olarak gönderilir |

### Örnek Request (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/create-collection/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Koleksiyon 1"
  }'
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Koleksiyon 1",
    "path": "/path/to/projects/Ürün Fotoğraf Çekimi/Koleksiyon 1",
    "project": 1,
    "created_at": "2024-01-15T12:15:00Z"
  }
}
```

### Hata Durumları

**Proje bulunamadı:**
```json
{
  "status": {
    "code": 2,
    "message": "project not found"
  },
  "data": {}
}
```

**Koleksiyon adı zaten mevcut:**
```json
{
  "status": {
    "code": 1,
    "message": "this collection name already exists"
  },
  "data": {}
}
```

### İşlem Akışı

1. **Flash Tetikleme**: `FlashSetting.get_settings()` ile flash gecikme ayarı alınır ve `trigger()` fonksiyonu çağrılır
2. **Fotoğraf Toplama**: Tüm cihazlardan paralel olarak fotoğraf listesi çekilir (`get_photo_list()`)
3. **Fotoğraf İndirme**: Her fotoğraf için `get_device_photo()` ile fotoğraf indirilir
4. **Dosya Kaydetme**: Fotoğraflar koleksiyon klasörüne kaydedilir
5. **Veritabanı Kaydı**: Her dosya için `File` modeli oluşturulur

### Notlar

- Koleksiyon oluşturulurken tüm cihazlardan fotoğraflar otomatik toplanır
- Flash ayarları (`/api/get-flash-setting`) önceden yapılandırılmalıdır
- İşlem tamamlanana kadar beklenir (tüm fotoğraflar indirilene kadar)
- Fotoğraf yoksa koleksiyon yine de oluşturulur, ancak dosya kaydı olmaz

---

## 7. Tüm Fotoğrafları Silme

Tüm cihazlardaki tüm fotoğrafları silmek için bu endpoint'i kullanın.

### Endpoint

```
DELETE /api/delete-all-photos
```

### Örnek Request (cURL)

```bash
curl -X DELETE http://127.0.0.1:8000/api/delete-all-photos
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "delete all photos request sent"
  },
  "data": {
    "device_responses": [
      {
        "device_id": 1,
        "device_name": "Raspberry Pi 1",
        "device_ip": "192.168.1.100",
        "status": "success",
        "response": {
          "deleted_count": 150,
          "message": "All photos deleted successfully"
        }
      },
      {
        "device_id": 2,
        "device_name": "Raspberry Pi 2",
        "device_ip": "192.168.1.101",
        "status": "success",
        "response": {
          "deleted_count": 75,
          "message": "All photos deleted successfully"
        }
      }
    ]
  }
}
```

### Hata Durumları

**Cihaz bulunamadı:**
```json
{
  "status": {
    "code": 1,
    "message": "no devices found"
  },
  "data": {}
}
```

**Cihaz bağlantı hatası:**
```json
{
  "status": {
    "code": 0,
    "message": "delete all photos request sent"
  },
  "data": {
    "device_responses": [
      {
        "device_id": 1,
        "device_name": "Raspberry Pi 1",
        "device_ip": "192.168.1.100",
        "status": "error",
        "error": "Connection timeout"
      }
    ]
  }
}
```

### Notlar

- Bu işlem geri alınamaz! Tüm cihazlardaki tüm fotoğraflar kalıcı olarak silinir
- İşlem tüm cihazlarda paralel olarak çalışır
- Her cihaz için `/api/delete-all-photos` endpoint'i çağrılır
- İşlem tamamlanana kadar beklenir

---

## 8. Tüm Kameraları Ayarlama

Tüm cihazlardaki kameralara aynı ayarları uygulamak için bu endpoint'i kullanın.

### Endpoint

```
PATCH /api/update-camera-setting
```

### Request Body

```json
{
  "iso_speed": "400",
  "shutter_speed": "1/60",
  "aperture": "8",
  "white_balance": "Auto",
  "image_format": "L",
  "drive_mode": "Single",
  "metering_mode": "Evaluative",
  "picture_style": "Standard"
}
```

### Parametreler

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `iso_speed` | string | Hayır | ISO hızı (Auto, 100, 200, 400, 800, 1600, 3200, 6400) |
| `shutter_speed` | string | Hayır | Enstantane hızı (örn: "1/60", "bulb", "30") |
| `aperture` | string | Hayır | Diyafram değeri (4, 4.5, 5, 5.6, 6.3, 7.1, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22, 25) |
| `white_balance` | string | Hayır | Beyaz dengesi (Auto, Daylight, Shadow, Cloudy, Tungsten, Fluorescent, Flash, Manual) |
| `image_format` | string | Hayır | Görüntü formatı (L, cL, M, cM, S1, cS1, S2, S3, RAW + L, RAW) |
| `drive_mode` | string | Hayır | Çekim modu (Single, Continuous, Timer 10 sec, Timer 2 sec, Continuous timer) |
| `metering_mode` | string | Hayır | Ölçüm modu (Evaluative, Partial, Center-weighted average) |
| `picture_style` | string | Hayır | Resim stili (Auto, Standard, Portrait, Landscape, Neutral, Faithful, Monochrome, User defined 1-3) |

### Örnek Request (cURL)

```bash
curl -X PATCH http://127.0.0.1:8000/api/update-camera-setting \
  -H "Content-Type: application/json" \
  -d '{
    "iso_speed": "400",
    "shutter_speed": "1/60",
    "aperture": "8",
    "white_balance": "Auto"
  }'
```

### Örnek Response (Başarılı)

```json
{
  "status": {
    "code": 0,
    "message": "update success"
  },
  "data": {
    "id": 1,
    "iso_speed": "400",
    "shutter_speed": "1/60",
    "aperture": "8",
    "white_balance": "Auto",
    "image_format": "L",
    "drive_mode": "Single",
    "metering_mode": "Evaluative",
    "picture_style": "Auto",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T12:30:00Z",
    "device_responses": [
      {
        "device_id": 1,
        "device_name": "Raspberry Pi 1",
        "device_ip": "192.168.1.100",
        "status": "success",
        "response": {
          "message": "Settings applied successfully"
        }
      },
      {
        "device_id": 2,
        "device_name": "Raspberry Pi 2",
        "device_ip": "192.168.1.101",
        "status": "success",
        "response": {
          "message": "Settings applied successfully"
        }
      }
    ]
  }
}
```

### Hata Durumları

**Validasyon hatası:**
```json
{
  "status": {
    "code": 1,
    "message": "validation error"
  },
  "errors": {
    "iso_speed": ["Invalid choice: '5000'"]
  }
}
```

**Cihazlara gönderim hatası:**
```json
{
  "status": {
    "code": 0,
    "message": "settings updated but failed to send to devices: Connection timeout"
  },
  "data": {
    "id": 1,
    "iso_speed": "400",
    "shutter_speed": "1/60",
    "aperture": "8",
    ...
  }
}
```

### Notlar

- Ayarlar önce veritabanında güncellenir, sonra tüm cihazlara gönderilir
- Sadece gönderilen parametreler güncellenir (partial update)
- İşlem tüm cihazlarda paralel olarak çalışır
- Her cihaz için `/api/set-device-settings` endpoint'i çağrılır
- Ayarlar singleton pattern ile saklanır (tek bir ayar kaydı)

---

## 🔄 Tam İşlem Akışı Özeti

Sistemi ilk açtığınızda izlemeniz gereken tam sıra:

```
1. POST /api/add-device          → Cihazları sisteme ekle
2. GET /api/get-device-list      → Cihazları ve kamera durumlarını kontrol et
3. POST /api/reconnect-cameras   → Kameraları yeniden bağla (gerekirse)
4. GET /api/get-device-list      → Kamera bağlantılarını doğrula
5. POST /api/create-project/     → Yeni proje oluştur
6. POST /api/create-collection/<project_id> → Koleksiyon oluştur (fotoğrafları topla)
7. DELETE /api/delete-all-photos → Tüm fotoğrafları temizle (gerekirse)
8. PATCH /api/update-camera-setting → Kamera ayarlarını yapılandır
```

## 💡 İpuçları

- **İlk Kurulum**: Sistem açıldığında önce tüm cihazları ekleyin ve bağlantılarını kontrol edin
- **Kamera Ayarları**: Fotoğraf çekmeden önce kamera ayarlarını yapılandırın
- **Flash Ayarları**: Koleksiyon oluşturmadan önce flash gecikme ayarını (`/api/update-flash-setting`) yapılandırın
- **Hata Kontrolü**: Her adımda response'daki `status.code` değerini kontrol edin (0 = başarılı, 1+ = hata)
- **Paralel İşlemler**: Cihaz işlemleri paralel çalışır, bu yüzden çoklu cihazlarda hızlıdır

## ⚠️ Önemli Uyarılar

- **Fotoğraf Silme**: `DELETE /api/delete-all-photos` işlemi geri alınamaz!
- **Cihaz Bağlantısı**: Cihazların aynı ağda olması ve API endpoint'lerini desteklemesi gerekir
- **Flash Tetikleme**: Koleksiyon oluşturulurken flash tetiklenir, bu yüzden donanım hazır olmalıdır
- **Proje Silme**: Proje silindiğinde içindeki tüm koleksiyonlar ve dosyalar da silinir

