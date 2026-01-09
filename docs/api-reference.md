# API Reference

Bu dokümantasyon, Luma-Server API'sinin tüm endpoint'lerini detaylı olarak açıklar.

## 📋 İçindekiler

- [Genel Bilgiler](#genel-bilgiler)
- [Response Formatı](#response-formatı)
- [Status Kodları](#status-kodları)
- [Proje Yönetimi](#proje-yönetimi)
- [Collection Yönetimi](#collection-yönetimi)
- [Dosya Yönetimi](#dosya-yönetimi)
- [Cihaz Yönetimi](#cihaz-yönetimi)
- [Ayar Yönetimi](#ayar-yönetimi)

---

## Genel Bilgiler

### Base URL

```
http://127.0.0.1:8000
```

### Content-Type

Tüm POST ve PATCH istekleri için:
```
Content-Type: application/json
```

### Response Formatı

Tüm API yanıtları aşağıdaki formatı kullanır:

```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": { ... }
}
```

### Status Kodları

| Code | Açıklama |
|------|----------|
| 0 | İşlem başarılı |
| 1 | Genel hata (eksik parametre, validasyon hatası, vb.) |
| 2 | Kaynak bulunamadı (bazı endpoint'lerde) |
| 3 | Kaynak bulunamadı (bazı endpoint'lerde) |

---

## Proje Yönetimi

### 1. Proje Oluştur

Yeni bir proje oluşturur.

**Endpoint:** `POST /api/create-project/`

**Request Body:**
```json
{
  "name": "string (required)"
}
```

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Proje Adı",
    "path": "/path/to/projects/Proje Adı",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"Missing fields: name"`
- `code: 1` - Proje adı zaten mevcut: `"this project name already exists"`
- `code: 1` - Klasör oluşturma hatası: `"Failed to create directory: ..."`

**Örnek (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/create-project/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Yeni Proje"}'
```

---

### 2. Proje Listesi

Tüm projeleri listeler.

**Endpoint:** `GET /api/get-project-list`

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": [
    {
      "id": 1,
      "name": "Proje 1",
      "path": "/path/to/projects/Proje 1",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Proje 2",
      "path": "/path/to/projects/Proje 2",
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-project-list
```

---

### 3. Proje Detayı

Belirli bir projenin detaylarını getirir.

**Endpoint:** `GET /api/get-project-detail/<project_id>`

**URL Parametreleri:**
- `project_id` (integer, required) - Proje ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Proje Adı",
    "path": "/path/to/projects/Proje Adı",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"project_id required"`
- `code: 3` - Proje bulunamadı: `"project not found"`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-project-detail/1
```

---

### 4. Proje Güncelle

Proje bilgilerini günceller (partial update).

**Endpoint:** `PATCH /api/update-project/<project_id>`

**URL Parametreleri:**
- `project_id` (integer, required) - Proje ID'si

**Request Body:**
```json
{
  "name": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "partial update success"
  },
  "data": {
    "id": 1,
    "name": "Güncellenmiş Proje Adı",
    "path": "/path/to/projects/Güncellenmiş Proje Adı",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"project_id required"`
- `code: 2` - Validasyon hatası: `"validation error"` (errors objesi içerir)
- `code: 3` - Proje bulunamadı: `"project not found"`

**Örnek (cURL):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/update-project/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Yeni İsim"}'
```

---

### 5. Proje Sil

Projeyi ve tüm içeriğini siler.

**Endpoint:** `DELETE /api/delete-project/<project_id>`

**URL Parametreleri:**
- `project_id` (integer, required) - Proje ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {}
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"project_id required"`
- `code: 3` - Proje bulunamadı: `"project not found"`

**⚠️ Uyarı:** Bu işlem geri alınamaz! Proje silindiğinde içindeki tüm collection'lar ve dosyalar da silinir.

**Örnek (cURL):**
```bash
curl -X DELETE http://127.0.0.1:8000/api/delete-project/1
```

---

### 6. Proje İndir

Projeyi ZIP formatında indirir.

**Endpoint:** `GET /api/download-project/<project_id>`

**URL Parametreleri:**
- `project_id` (integer, required) - Proje ID'si

**Response:**
- Content-Type: `application/zip`
- Dosya adı: `{project_name}.zip`
- Binary ZIP dosyası

**Hata Durumları (JSON):**
- `code: 1` - Eksik parametre: `"project_id required"`
- `code: 2` - Proje bulunamadı: `"project not found"`
- `code: 3` - Proje collection'ı yok: `"project has no collections"`
- `code: 1` - ZIP oluşturma hatası: `"Failed to create zip: ..."`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/download-project/1 \
  -o project.zip
```

---

## Collection Yönetimi

### 1. Collection Oluştur

Yeni bir collection oluşturur ve otomatik olarak fotoğrafları toplar.

**Endpoint:** `POST /api/create-collection/<project_id>`

**URL Parametreleri:**
- `project_id` (integer, required) - Proje ID'si

**Request Body:**
```json
{
  "name": "string (required)"
}
```

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Collection 1",
    "path": "/path/to/projects/Proje/Collection 1",
    "project": 1,
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"Missing fields: name, project_id"`
- `code: 2` - Proje bulunamadı: `"project not found"`
- `code: 1` - Collection adı zaten mevcut: `"this collection name already exists"`
- `code: 1` - Klasör oluşturma hatası: `"Failed to create directory: ..."`

**Notlar:**
- Collection oluşturulurken flash tetiklenir ve tüm cihazlardan fotoğraflar toplanır
- Fotoğraflar otomatik olarak collection klasörüne kaydedilir
- İşlem tamamlanana kadar beklenir

**Örnek (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/create-collection/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Collection 1"}'
```

---

### 2. Collection Listesi

Bir projeye ait tüm collection'ları listeler.

**Endpoint:** `GET /api/get-collection-list/<project_id>`

**URL Parametreleri:**
- `project_id` (integer, required) - Proje ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": [
    {
      "id": 1,
      "name": "Collection 1",
      "path": "/path/to/projects/Proje/Collection 1",
      "project": 1,
      "created_at": "2024-01-15T12:00:00Z"
    }
  ]
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"project_id required"`
- `code: 2` - Proje bulunamadı: `"project not found"`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-collection-list/1
```

---

### 3. Collection Detayı

Belirli bir collection'ın detaylarını getirir.

**Endpoint:** `GET /api/get-collection-detail/<collection_id>`

**URL Parametreleri:**
- `collection_id` (integer, required) - Collection ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "Collection 1",
    "path": "/path/to/projects/Proje/Collection 1",
    "project": 1,
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"collection_id required"`
- `code: 2` - Collection bulunamadı: `"collection not found"`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-collection-detail/1
```

---

### 4. Collection İndir

Collection'ı ZIP formatında indirir.

**Endpoint:** `GET /api/download-collection/<collection_id>`

**URL Parametreleri:**
- `collection_id` (integer, required) - Collection ID'si

**Response:**
- Content-Type: `application/zip`
- Dosya adı: `{collection_name}.zip`
- Binary ZIP dosyası

**Hata Durumları (JSON):**
- `code: 1` - Eksik parametre: `"collection_id required"`
- `code: 2` - Collection bulunamadı: `"collection not found"`
- `code: 3` - Collection'da dosya yok: `"collection has no files"`
- `code: 1` - ZIP oluşturma hatası: `"Failed to create zip: ..."`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/download-collection/1 \
  -o collection.zip
```

---

### 5. Collection Sil

Collection'ı ve tüm içeriğini siler.

**Endpoint:** `DELETE /api/delete-collection/<collection_id>`

**URL Parametreleri:**
- `collection_id` (integer, required) - Collection ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {}
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"collection_id required"`
- `code: 2` - Collection bulunamadı: `"collection not found"`

**⚠️ Uyarı:** Bu işlem geri alınamaz! Collection silindiğinde içindeki tüm dosyalar da silinir.

**Örnek (cURL):**
```bash
curl -X DELETE http://127.0.0.1:8000/api/delete-collection/1
```

---

## Dosya Yönetimi

### 1. Dosya Listesi

Bir collection'a ait tüm dosyaları listeler.

**Endpoint:** `GET /api/get-file-list/<collection_id>`

**URL Parametreleri:**
- `collection_id` (integer, required) - Collection ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": [
    {
      "id": 1,
      "name": "IMG_001.jpg",
      "path": "/path/to/collection/IMG_001.jpg",
      "size": 5242880,
      "collection": 1,
      "created_at": "2024-01-15T12:00:00Z"
    }
  ]
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"collection_id required"`
- `code: 3` - Collection bulunamadı: `"collection not found"`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-file-list/1
```

---

### 2. Dosya Detayı

Belirli bir dosyanın detaylarını getirir.

**Endpoint:** `GET /api/get-file-detail/<file_id>`

**URL Parametreleri:**
- `file_id` (integer, required) - Dosya ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "name": "IMG_001.jpg",
    "path": "/path/to/collection/IMG_001.jpg",
    "size": 5242880,
    "collection": 1,
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"file_id required"`
- `code: 3` - Dosya bulunamadı: `"file not found"`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-file-detail/1
```

---

### 3. Dosya İndir

Dosyayı indirir.

**Endpoint:** `GET /api/download-file/<file_id>`

**URL Parametreleri:**
- `file_id` (integer, required) - Dosya ID'si

**Response:**
- Content-Type: Dosya tipine göre (image/jpeg, image/png, vb.)
- Dosya adı: Orijinal dosya adı
- Binary dosya içeriği

**Hata Durumları (JSON):**
- `code: 1` - Eksik parametre: `"file_id required"`
- `code: 2` - Dosya bulunamadı: `"file not found"`
- `code: 3` - Dosya dosya sisteminde bulunamadı: `"file not found on filesystem"`
- `code: 1` - Dosya okuma hatası: `"Failed to read file: ..."`

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/download-file/1 \
  -o image.jpg
```

---

## Cihaz Yönetimi

### 1. Cihaz Ekle

Yeni bir cihaz (Raspberry Pi) ekler.

**Endpoint:** `POST /api/add-device`

**Request Body:**
```json
{
  "name": "string (required)",
  "ip": "string (required)"
}
```

**Response (200 OK):**
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

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"Missing fields: name, ip"`
- `code: 1` - Cihaz adı zaten mevcut: `"this device name already exists"`
- `code: 1` - IP adresi zaten kayıtlı: `"this device already exists"`
- `code: 1` - Unique field çakışması: `"conflict on unique fields"`

**Notlar:**
- Cihaz eklenirken otomatik olarak cihazdan bilgi çekilir (`/api/get-device-data` endpoint'i)
- Cihaz adı ve IP adresi benzersiz olmalıdır

**Örnek (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/add-device \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Raspberry Pi 1",
    "ip": "192.168.1.100"
  }'
```

---

### 2. Cihaz Listesi

Tüm cihazları listeler ve güncel durumlarını çeker.

**Endpoint:** `GET /api/get-device-list`

**Response (200 OK):**
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
        }
      },
      "statistics": {
        "total_photos": 150,
        "storage_used": "2.5 GB"
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T11:45:00Z"
    }
  ]
}
```

**Notlar:**
- Bu endpoint çağrıldığında tüm cihazlardan güncel bilgiler çekilir
- Kamera durumları ve istatistikler güncellenir

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-device-list
```

---

### 3. Cihaz Güncelle

Cihaz bilgilerini günceller (partial update).

**Endpoint:** `PATCH /api/update-device/<device_id>`

**URL Parametreleri:**
- `device_id` (integer, required) - Cihaz ID'si

**Request Body:**
```json
{
  "name": "string (optional)",
  "ip": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "partial update success"
  },
  "data": {
    "id": 1,
    "name": "Güncellenmiş Cihaz Adı",
    "ip": "192.168.1.100",
    "device_id": "001",
    "cameras": {...},
    "statistics": {...},
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"device_id required"`
- `code: 2` - Validasyon hatası: `"validation error"` (errors objesi içerir)
- `code: 3` - Cihaz bulunamadı: `"device not found"`

**Örnek (cURL):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/update-device/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Yeni İsim"}'
```

---

### 4. Cihaz Sil

Cihazı sistemden siler.

**Endpoint:** `DELETE /api/delete-device/<device_id>`

**URL Parametreleri:**
- `device_id` (integer, required) - Cihaz ID'si

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {}
}
```

**Hata Durumları:**
- `code: 1` - Eksik parametre: `"device_id required"`
- `code: 3` - Cihaz bulunamadı: `"device not found"`

**Örnek (cURL):**
```bash
curl -X DELETE http://127.0.0.1:8000/api/delete-device/1
```

---

### 5. Kameraları Yeniden Bağla

Tüm cihazlardaki kameraları yeniden bağlar.

**Endpoint:** `POST /api/reconnect-cameras`

**Response (200 OK):**
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
          "cameras_connected": 2
        }
      }
    ]
  }
}
```

**Hata Durumları:**
- `code: 1` - Cihaz bulunamadı: `"no devices found"`
- `code: 1` - Bağlantı hatası: `"failed to reconnect cameras: ..."`

**Notlar:**
- İşlem tüm cihazlarda paralel olarak çalışır
- Her cihaz için önce `/api/disconnect-all`, sonra `/api/connect-all` çağrılır

**Örnek (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/reconnect-cameras
```

---

### 6. Tüm Fotoğrafları Sil

Tüm cihazlardaki tüm fotoğrafları siler.

**Endpoint:** `DELETE /api/delete-all-photos`

**Response (200 OK):**
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
          "deleted_count": 150
        }
      }
    ]
  }
}
```

**Hata Durumları:**
- `code: 1` - Cihaz bulunamadı: `"no devices found"`
- `code: 1` - Silme hatası: `"failed to delete photos: ..."`

**⚠️ Uyarı:** Bu işlem geri alınamaz! Tüm cihazlardaki tüm fotoğraflar kalıcı olarak silinir.

**Notlar:**
- İşlem tüm cihazlarda paralel olarak çalışır
- Her cihaz için `/api/delete-all-photos` endpoint'i çağrılır

**Örnek (cURL):**
```bash
curl -X DELETE http://127.0.0.1:8000/api/delete-all-photos
```

---

### 7. Cihazları Resetle

Tüm cihazları resetler.

**Endpoint:** `POST /api/reset-devices`

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "reset devices request sent"
  },
  "data": {
    "device_responses": [
      {
        "device_id": 1,
        "device_name": "Raspberry Pi 1",
        "device_ip": "192.168.1.100",
        "status": "success",
        "response": {
          "message": "Camera reset successfully"
        }
      }
    ]
  }
}
```

**Hata Durumları:**
- `code: 1` - Cihaz bulunamadı: `"no devices found"`
- `code: 1` - Reset hatası: `"failed to reset devices: ..."`

**Notlar:**
- İşlem tüm cihazlarda paralel olarak çalışır
- Her cihaz için `/api/reset-camera` endpoint'i çağrılır

**Örnek (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/reset-devices
```

---

## Ayar Yönetimi

### 1. Kamera Ayarlarını Getir

Mevcut kamera ayarlarını getirir.

**Endpoint:** `GET /api/get-camera-setting`

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "iso_speed": "Auto",
    "shutter_speed": "1/60",
    "aperture": "8",
    "white_balance": "Auto",
    "image_format": "L",
    "drive_mode": "Single",
    "metering_mode": "Evaluative",
    "picture_style": "Auto",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

**Notlar:**
- Ayarlar singleton pattern ile saklanır (tek bir ayar kaydı)
- İlk çağrıda varsayılan ayarlar oluşturulur

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-camera-setting
```

---

### 2. Kamera Ayarlarını Güncelle

Kamera ayarlarını günceller ve tüm cihazlara gönderir.

**Endpoint:** `PATCH /api/update-camera-setting`

**Request Body:**
```json
{
  "iso_speed": "string (optional)",
  "shutter_speed": "string (optional)",
  "aperture": "string (optional)",
  "white_balance": "string (optional)",
  "image_format": "string (optional)",
  "drive_mode": "string (optional)",
  "metering_mode": "string (optional)",
  "picture_style": "string (optional)"
}
```

**Geçerli Değerler:**

**ISO Speed:**
- `"Auto"`, `"100"`, `"200"`, `"400"`, `"800"`, `"1600"`, `"3200"`, `"6400"`

**Shutter Speed:**
- `"bulb"`, `"30"`, `"25"`, `"20"`, `"15"`, `"13"`, `"10.3"`, `"8"`, `"6.3"`, `"5"`, `"4"`, `"3.2"`, `"2.5"`, `"2"`, `"1.6"`, `"1.3"`, `"1"`, `"0.8"`, `"0.6"`, `"0.5"`, `"0.4"`, `"0.3"`, `"1/4"`, `"1/5"`, `"1/6"`, `"1/8"`, `"1/10"`, `"1/13"`, `"1/15"`, `"1/20"`, `"1/25"`, `"1/30"`, `"1/40"`, `"1/50"`, `"1/60"`, `"1/80"`, `"1/100"`, `"1/125"`, `"1/160"`, `"1/200"`, `"1/250"`, `"1/320"`, `"1/400"`, `"1/500"`, `"1/640"`, `"1/800"`, `"1/1000"`, `"1/1250"`, `"1/1600"`, `"1/2000"`, `"1/2500"`, `"1/3200"`, `"1/4000"`

**Aperture:**
- `"4"`, `"4.5"`, `"5"`, `"5.6"`, `"6.3"`, `"7.1"`, `"8"`, `"9"`, `"10"`, `"11"`, `"13"`, `"14"`, `"16"`, `"18"`, `"20"`, `"22"`, `"25"`

**White Balance:**
- `"Auto"`, `"Daylight"`, `"Shadow"`, `"Cloudy"`, `"Tungsten"`, `"Fluorescent"`, `"Flash"`, `"Manual"`

**Image Format:**
- `"L"`, `"cL"`, `"M"`, `"cM"`, `"S1"`, `"cS1"`, `"S2"`, `"S3"`, `"RAW + L"`, `"RAW"`

**Drive Mode:**
- `"Single"`, `"Continuous"`, `"Timer 10 sec"`, `"Timer 2 sec"`, `"Continuous timer"`

**Metering Mode:**
- `"Evaluative"`, `"Partial"`, `"Center-weighted average"`

**Picture Style:**
- `"Auto"`, `"Standard"`, `"Portrait"`, `"Landscape"`, `"Neutral"`, `"Faithful"`, `"Monochrome"`, `"User defined 1"`, `"User defined 2"`, `"User defined 3"`

**Response (200 OK):**
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
      }
    ]
  }
}
```

**Hata Durumları:**
- `code: 1` - Validasyon hatası: `"validation error"` (errors objesi içerir)
- `code: 0` - Ayarlar güncellendi ancak cihazlara gönderilemedi: `"settings updated but failed to send to devices: ..."`

**Notlar:**
- Ayarlar önce veritabanında güncellenir, sonra tüm cihazlara gönderilir
- Sadece gönderilen parametreler güncellenir (partial update)
- İşlem tüm cihazlarda paralel olarak çalışır

**Örnek (cURL):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/update-camera-setting \
  -H "Content-Type: application/json" \
  -d '{
    "iso_speed": "400",
    "shutter_speed": "1/60",
    "aperture": "8"
  }'
```

---

### 3. Flash Ayarlarını Getir

Mevcut flash ayarlarını getirir.

**Endpoint:** `GET /api/get-flash-setting`

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": 1,
    "delay": 0,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

**Notlar:**
- Ayarlar singleton pattern ile saklanır (tek bir ayar kaydı)
- `delay` değeri milisaniye cinsindendir
- İlk çağrıda varsayılan değer (0) oluşturulur

**Örnek (cURL):**
```bash
curl -X GET http://127.0.0.1:8000/api/get-flash-setting
```

---

### 4. Flash Ayarlarını Güncelle

Flash ayarlarını günceller.

**Endpoint:** `PATCH /api/update-flash-setting`

**Request Body:**
```json
{
  "delay": "integer (optional)"
}
```

**Parametreler:**
- `delay` (integer, optional) - Flash gecikme süresi (milisaniye)

**Response (200 OK):**
```json
{
  "status": {
    "code": 0,
    "message": "update success"
  },
  "data": {
    "id": 1,
    "delay": 100,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T12:30:00Z"
  }
}
```

**Hata Durumları:**
- `code: 1` - Validasyon hatası: `"validation error"` (errors objesi içerir)

**Notlar:**
- Flash gecikme ayarı, collection oluşturulurken flash tetikleme sırasında kullanılır
- Delay değeri milisaniye cinsindendir

**Örnek (cURL):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/update-flash-setting \
  -H "Content-Type: application/json" \
  -d '{"delay": 100}'
```

---

## Hata Yönetimi

### Genel Hata Formatı

Tüm hatalar aşağıdaki formatı kullanır:

```json
{
  "status": {
    "code": 1,
    "message": "Hata mesajı"
  },
  "data": {},
  "errors": {}  // Validasyon hatalarında mevcut
}
```

### HTTP Status Kodları

Tüm endpoint'ler HTTP 200 OK döner. Hata durumları response body içindeki `status.code` ile belirtilir.

### Yaygın Hata Mesajları

| Mesaj | Açıklama |
|-------|----------|
| `"Missing fields: ..."` | Eksik zorunlu parametreler |
| `"validation error"` | Validasyon hatası (errors objesi içerir) |
| `"not found"` | Kaynak bulunamadı |
| `"already exists"` | Kayıt zaten mevcut |
| `"conflict on unique fields"` | Unique field çakışması |
| `"no devices found"` | Cihaz bulunamadı |
| `"Failed to create directory"` | Klasör oluşturma hatası |
| `"Failed to create zip"` | ZIP oluşturma hatası |
| `"Failed to read file"` | Dosya okuma hatası |

---

## Rate Limiting

Şu anda rate limiting uygulanmamaktadır. Production ortamında rate limiting eklenmesi önerilir.

## Authentication

Şu anda authentication uygulanmamaktadır. Production ortamında authentication eklenmesi önerilir.

## CORS

CORS yapılandırması `django-cors-headers` ile yapılabilir. Production ortamında `ALLOWED_ORIGINS` ayarlanmalıdır.

