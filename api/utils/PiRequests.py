import requests
from concurrent.futures import ThreadPoolExecutor


def get_device_data(ip):
    response = requests.get(f"http://{ip}/api/get-device-data")
    return response.json()


def get_device_photo(url):
    response = requests.get(url)
    return response


def _get_photo_list_single_device(device):
    """Tek bir cihazdan fotoğraf listesini al (thread için)"""
    try:
        response = requests.get(f"http://{device.ip}/api/get-photo-list")
        response.raise_for_status()
        photos = response.json().get("photos", [])
        return {"device": device, "photos": photos, "status": "success"}
    except requests.exceptions.RequestException as e:
        return {"device": device, "photos": [], "status": "error", "error": str(e)}


def get_photo_list(devices):
    """Tüm cihazlardan fotoğraf listelerini eş zamanlı olarak al"""
    merged = []
    
    # ThreadPoolExecutor ile eş zamanlı istekler
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Tüm cihazlar için future'ları oluştur
        futures = [
            executor.submit(_get_photo_list_single_device, device) 
            for device in devices
        ]
        
        # TÜM future'ların tamamlanmasını bekle
        for future in futures:
            result = future.result()  # Bu satır tüm thread bitene kadar bekler
            if result["status"] == "success":
                merged.extend(result["photos"])
    
    return merged


def _set_device_settings_single(device, setting_data):
    """Tek bir cihaza ayar gönder (thread için)"""
    try:
        response = requests.post(
            f"http://{device.ip}/api/set-device-settings",
            json=setting_data,
        )
        response.raise_for_status()
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "success",
            "response": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "error",
            "error": str(e)
        }


def set_device_settings(devices, settings):
    """
    Tüm cihazlara kamera ayarlarını eş zamanlı olarak gönderir.
    TÜM istekler bitene kadar bekler.

    Args:
        devices: Device queryset veya list
        settings: CameraSetting instance

    Returns:
        list: Her cihazdan gelen response'ların listesi
    """
    setting_data = {
        "iso": settings.iso_speed,
        "shutterspeed": settings.shutter_speed,
        "aperture": settings.aperture,
        "whitebalance": settings.white_balance,
        "imageformat": settings.image_format,
        "drivemode": settings.drive_mode,
        "meteringmode": settings.metering_mode,
        "picturestyle": settings.picture_style,
    }

    merged = []
    
    # ThreadPoolExecutor ile eş zamanlı istekler
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Tüm cihazlar için future'ları oluştur
        futures = [
            executor.submit(_set_device_settings_single, device, setting_data) 
            for device in devices
        ]
        
        # TÜM future'ların tamamlanmasını bekle
        for future in futures:
            result = future.result()  # Bu satır tüm thread bitene kadar bekler
            merged.append(result)
    
    return merged


def _delete_all_photos_single(device):
    """Tek bir cihazdan tüm fotoğrafları sil (thread için)"""
    try:
        response = requests.delete(
            f"http://{device.ip}/api/delete-all-photos",
        )
        response.raise_for_status()
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "success",
            "response": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "error",
            "error": str(e)
        }


def delete_all_photos(devices):
    """
    Tüm cihazlardan tüm fotoğrafları eş zamanlı olarak siler.
    TÜM istekler bitene kadar bekler.

    Args:
        devices: Device queryset veya list

    Returns:
        list: Her cihazdan gelen response'ların listesi
    """
    merged = []
    
    # ThreadPoolExecutor ile eş zamanlı istekler
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Tüm cihazlar için future'ları oluştur
        futures = [
            executor.submit(_delete_all_photos_single, device) 
            for device in devices
        ]
        
        # TÜM future'ların tamamlanmasını bekle
        for future in futures:
            result = future.result()  # Bu satır tüm thread bitene kadar bekler
            merged.append(result)
    
    return merged


def _reconnect_cameras_single(device):
    """Tek bir cihazda kameraları yeniden bağla (thread için)"""
    try:
        # Önce disconnect, sonra connect
        disconnect_response = requests.get(
            f"http://{device.ip}/api/disconnect-all",
        )
        disconnect_response.raise_for_status()
        
        connect_response = requests.get(
            f"http://{device.ip}/api/connect-all",
        )
        connect_response.raise_for_status()
        
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "success",
            "response": connect_response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "error",
            "error": str(e)
        }


def reconnect_cameras(devices):
    """
    Tüm cihazlarda kameraları eş zamanlı olarak yeniden bağlar.
    TÜM istekler bitene kadar bekler.

    Args:
        devices: Device queryset veya list

    Returns:
        list: Her cihazdan gelen response'ların listesi
    """
    merged = []
    
    # ThreadPoolExecutor ile eş zamanlı istekler
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Tüm cihazlar için future'ları oluştur
        futures = [
            executor.submit(_reconnect_cameras_single, device) 
            for device in devices
        ]
        
        # TÜM future'ların tamamlanmasını bekle
        for future in futures:
            result = future.result()  # Bu satır tüm thread bitene kadar bekler
            merged.append(result)
    
    return merged


def _reset_device_single(device):
    """Tek bir cihazı resetle (thread için)"""
    try:
        response = requests.get(
            f"http://{device.ip}/api/reset-camera",
        )
        response.raise_for_status()
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "success",
            "response": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_ip": device.ip,
            "status": "error",
            "error": str(e)
        }


def reset_devices(devices):
    """Tüm cihazları eş zamanlı olarak resetler. TÜM istekler bitene kadar bekler."""
    merged = []
    
    # ThreadPoolExecutor ile eş zamanlı istekler
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Tüm cihazlar için future'ları oluştur
        futures = [
            executor.submit(_reset_device_single, device) 
            for device in devices
        ]
        
        # TÜM future'ların tamamlanmasını bekle
        for future in futures:
            result = future.result()  # Bu satır tüm thread bitene kadar bekler
            merged.append(result)
    
    return merged