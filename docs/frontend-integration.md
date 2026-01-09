# Frontend Entegrasyon Kılavuzu

Bu dokümantasyon, frontend uygulamalarının Luma-Server API'sine nasıl bağlanacağını ve kullanacağını açıklar.

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [CORS Yapılandırması](#cors-yapılandırması)
- [API Bağlantısı](#api-bağlantısı)
- [Örnek Kodlar](#örnek-kodlar)
- [Hata Yönetimi](#hata-yönetimi)
- [Best Practices](#best-practices)

---

## Genel Bakış

Luma-Server, RESTful API sağlar ve herhangi bir frontend framework'ü ile kullanılabilir (React, Vue, Angular, Vanilla JavaScript, vb.).

### Base URL

```
Development: http://127.0.0.1:8000
Production:  https://your-domain.com
```

### API Endpoint Pattern

```
http://127.0.0.1:8000/api/{endpoint}
```

---

## CORS Yapılandırması

### Backend Yapılandırması

Luma-Server'da CORS zaten yapılandırılmıştır (`django-cors-headers`). Ancak production için ayarlanması gerekir.

**settings.py'ye ekleyin:**

```python
# CORS ayarları
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default
    "http://localhost:5173",  # Vite default
    "http://localhost:4200",  # Angular default
    "https://your-frontend-domain.com",  # Production
]

# Veya tüm origin'lere izin ver (sadece development)
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Sadece development için!

# İzin verilen HTTP metodları
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# İzin verilen header'lar
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

### Frontend'de CORS Kontrolü

Modern tarayıcılar CORS'u otomatik yönetir. Özel bir yapılandırma gerekmez.

---

## API Bağlantısı

### 1. Base URL Yapılandırması

#### JavaScript/TypeScript

```javascript
// config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

export default API_BASE_URL;
```

#### React (Axios)

```javascript
// api/client.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
```

#### Vue.js (Axios)

```javascript
// api/client.js
import axios from 'axios';

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
```

---

## Örnek Kodlar

### React Örnekleri

#### 1. Proje Listesi Getirme

```javascript
// services/projectService.js
import apiClient from '../api/client';

export const getProjectList = async () => {
  try {
    const response = await apiClient.get('/get-project-list');
    
    if (response.data.status.code === 0) {
      return {
        success: true,
        data: response.data.data,
      };
    } else {
      return {
        success: false,
        error: response.data.status.message,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};
```

#### 2. Proje Oluşturma

```javascript
// services/projectService.js
export const createProject = async (name) => {
  try {
    const response = await apiClient.post('/create-project/', {
      name: name,
    });
    
    if (response.data.status.code === 0) {
      return {
        success: true,
        data: response.data.data,
      };
    } else {
      return {
        success: false,
        error: response.data.status.message,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};
```

#### 3. React Component Örneği

```javascript
// components/ProjectList.jsx
import React, { useState, useEffect } from 'react';
import { getProjectList, createProject } from '../services/projectService';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [newProjectName, setNewProjectName] = useState('');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setLoading(true);
    setError(null);
    
    const result = await getProjectList();
    
    if (result.success) {
      setProjects(result.data);
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    
    if (!newProjectName.trim()) {
      setError('Proje adı boş olamaz');
      return;
    }

    setLoading(true);
    setError(null);

    const result = await createProject(newProjectName);
    
    if (result.success) {
      setNewProjectName('');
      loadProjects(); // Listeyi yenile
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  if (loading && projects.length === 0) {
    return <div>Yükleniyor...</div>;
  }

  return (
    <div>
      <h2>Projeler</h2>
      
      <form onSubmit={handleCreateProject}>
        <input
          type="text"
          value={newProjectName}
          onChange={(e) => setNewProjectName(e.target.value)}
          placeholder="Proje adı"
        />
        <button type="submit" disabled={loading}>
          Proje Oluştur
        </button>
      </form>

      {error && <div style={{ color: 'red' }}>{error}</div>}

      <ul>
        {projects.map((project) => (
          <li key={project.id}>
            {project.name} - {new Date(project.created_at).toLocaleDateString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProjectList;
```

#### 4. Cihaz Listesi ve Kamera Ayarları

```javascript
// services/deviceService.js
import apiClient from '../api/client';

export const getDeviceList = async () => {
  try {
    const response = await apiClient.get('/get-device-list');
    
    if (response.data.status.code === 0) {
      return {
        success: true,
        data: response.data.data,
      };
    } else {
      return {
        success: false,
        error: response.data.status.message,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};

export const updateCameraSettings = async (settings) => {
  try {
    const response = await apiClient.patch('/update-camera-setting', settings);
    
    if (response.data.status.code === 0) {
      return {
        success: true,
        data: response.data.data,
      };
    } else {
      return {
        success: false,
        error: response.data.status.message,
        errors: response.data.errors,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};
```

#### 5. Collection Oluşturma (Fotoğraf Çekimi)

```javascript
// services/collectionService.js
import apiClient from '../api/client';

export const createCollection = async (projectId, name) => {
  try {
    const response = await apiClient.post(`/create-collection/${projectId}`, {
      name: name,
    });
    
    if (response.data.status.code === 0) {
      return {
        success: true,
        data: response.data.data,
      };
    } else {
      return {
        success: false,
        error: response.data.status.message,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};
```

#### 6. Dosya İndirme

```javascript
// services/fileService.js
import apiClient from '../api/client';

export const downloadFile = async (fileId, filename) => {
  try {
    const response = await apiClient.get(`/download-file/${fileId}`, {
      responseType: 'blob', // Binary dosya için
    });
    
    // Blob'u dosya olarak indir
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    return {
      success: true,
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};
```

---

### Vue.js Örnekleri

#### 1. Vue Component Örneği

```vue
<template>
  <div>
    <h2>Projeler</h2>
    
    <form @submit.prevent="createProject">
      <input v-model="newProjectName" placeholder="Proje adı" />
      <button type="submit" :disabled="loading">Proje Oluştur</button>
    </form>

    <div v-if="error" style="color: red">{{ error }}</div>

    <ul v-if="!loading">
      <li v-for="project in projects" :key="project.id">
        {{ project.name }}
      </li>
    </ul>
    <div v-else>Yükleniyor...</div>
  </div>
</template>

<script>
import apiClient from '../api/client';

export default {
  data() {
    return {
      projects: [],
      loading: false,
      error: null,
      newProjectName: '',
    };
  },
  mounted() {
    this.loadProjects();
  },
  methods: {
    async loadProjects() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await apiClient.get('/get-project-list');
        
        if (response.data.status.code === 0) {
          this.projects = response.data.data;
        } else {
          this.error = response.data.status.message;
        }
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    async createProject() {
      if (!this.newProjectName.trim()) {
        this.error = 'Proje adı boş olamaz';
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await apiClient.post('/create-project/', {
          name: this.newProjectName,
        });
        
        if (response.data.status.code === 0) {
          this.newProjectName = '';
          this.loadProjects();
        } else {
          this.error = response.data.status.message;
        }
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
```

---

### Vanilla JavaScript Örnekleri

#### 1. Fetch API Kullanımı

```javascript
// api.js
const API_BASE_URL = 'http://127.0.0.1:8000/api';

async function getProjectList() {
  try {
    const response = await fetch(`${API_BASE_URL}/get-project-list`);
    const data = await response.json();
    
    if (data.status.code === 0) {
      return {
        success: true,
        data: data.data,
      };
    } else {
      return {
        success: false,
        error: data.status.message,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

async function createProject(name) {
  try {
    const response = await fetch(`${API_BASE_URL}/create-project/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name }),
    });
    
    const data = await response.json();
    
    if (data.status.code === 0) {
      return {
        success: true,
        data: data.data,
      };
    } else {
      return {
        success: false,
        error: data.status.message,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

// Kullanım
getProjectList().then((result) => {
  if (result.success) {
    console.log('Projeler:', result.data);
  } else {
    console.error('Hata:', result.error);
  }
});
```

---

## Hata Yönetimi

### API Response Formatı

Tüm API yanıtları aşağıdaki formatı kullanır:

```javascript
{
  "status": {
    "code": 0,        // 0 = başarılı, 1+ = hata
    "message": "success"
  },
  "data": { ... },   // Başarılı durumda veri
  "errors": { ... }  // Validasyon hatalarında
}
```

### Hata Yönetimi Utility

```javascript
// utils/apiErrorHandler.js
export const handleApiResponse = (response) => {
  if (response.data.status.code === 0) {
    return {
      success: true,
      data: response.data.data,
    };
  } else {
    return {
      success: false,
      error: response.data.status.message,
      errors: response.data.errors || null,
      code: response.data.status.code,
    };
  }
};

export const handleApiError = (error) => {
  if (error.response) {
    // API'den hata yanıtı geldi
    return {
      success: false,
      error: error.response.data?.status?.message || 'API Hatası',
      code: error.response.data?.status?.code || 1,
    };
  } else if (error.request) {
    // İstek gönderildi ama yanıt alınamadı
    return {
      success: false,
      error: 'Sunucuya bağlanılamadı',
      code: -1,
    };
  } else {
    // İstek hazırlanırken hata oluştu
    return {
      success: false,
      error: error.message || 'Bilinmeyen hata',
      code: -2,
    };
  }
};
```

### Axios Interceptor Kullanımı

```javascript
// api/client.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Token ekleme, logging vb.
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Başarılı yanıtları işle
    return response;
  },
  (error) => {
    // Hata yanıtlarını işle
    if (error.response?.status === 500) {
      console.error('Sunucu hatası:', error.response.data);
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## Best Practices

### 1. Environment Variables

```javascript
// .env
REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_API_TIMEOUT=30000
```

### 2. Loading States

```javascript
const [loading, setLoading] = useState(false);

const fetchData = async () => {
  setLoading(true);
  try {
    // API çağrısı
  } finally {
    setLoading(false);
  }
};
```

### 3. Error Boundaries (React)

```javascript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('API Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Bir şeyler yanlış gitti.</h1>;
    }

    return this.props.children;
  }
}
```

### 4. Retry Logic

```javascript
const fetchWithRetry = async (url, options, retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
};
```

### 5. Request Cancellation

```javascript
// AbortController kullanımı
const controller = new AbortController();

fetch(url, { signal: controller.signal })
  .then(response => response.json())
  .catch(error => {
    if (error.name === 'AbortError') {
      console.log('İstek iptal edildi');
    }
  });

// İptal et
controller.abort();
```

---

## Örnek Proje Yapısı

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.js          # Axios instance
│   │   └── endpoints.js       # Endpoint constants
│   ├── services/
│   │   ├── projectService.js
│   │   ├── collectionService.js
│   │   ├── deviceService.js
│   │   └── fileService.js
│   ├── utils/
│   │   ├── apiErrorHandler.js
│   │   └── apiResponseHandler.js
│   └── components/
│       ├── ProjectList.jsx
│       ├── DeviceList.jsx
│       └── CollectionList.jsx
└── .env
```

---

## Test Etme

### Postman Collection

Projede `postman_collection.json` dosyası mevcuttur. Postman'de import ederek test edebilirsiniz.

### cURL Örnekleri

Tüm endpoint'ler için cURL örnekleri [API Reference](api-reference.md) dokümantasyonunda mevcuttur.

---

## Sorun Giderme

### CORS Hatası

**Hata:** `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Çözüm:**
1. Backend'de `CORS_ALLOWED_ORIGINS` ayarını kontrol edin
2. Frontend URL'ini ekleyin
3. Development için `CORS_ALLOW_ALL_ORIGINS = True` kullanabilirsiniz

### Connection Refused

**Hata:** `Failed to fetch` veya `Network Error`

**Çözüm:**
1. Backend sunucusunun çalıştığından emin olun
2. Base URL'in doğru olduğunu kontrol edin
3. Firewall ayarlarını kontrol edin

### 404 Not Found

**Hata:** `404 Not Found`

**Çözüm:**
1. Endpoint URL'ini kontrol edin (`/api/` prefix'i var mı?)
2. HTTP metodunu kontrol edin (GET, POST, PATCH, DELETE)
3. URL parametrelerini kontrol edin

---

## Sonuç

Luma-Server API'si, standart RESTful prensiplere uygun olarak tasarlanmıştır ve herhangi bir frontend framework'ü ile kolayca entegre edilebilir. Bu kılavuzdaki örnekleri kullanarak hızlıca entegrasyon yapabilirsiniz.

