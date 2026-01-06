"""
USB4751L Digital Output Control - Python Implementation
Java kodundan çevrilmiş bit sıralaması ile uyumlu
"""

import ctypes
import sys
import os
from ctypes import c_int, c_long, c_longlong, c_int64, c_byte, c_char_p, POINTER, byref

# Java'da long 64-bit, Python'da c_long Windows'ta 32-bit olabilir
# Bu yüzden 64-bit handle için c_longlong kullanmalıyız
c_handle = c_longlong  # 64-bit handle

# Error Code değerleri (0 = Success)
ERROR_SUCCESS = 0

# ModuleType enum değerleri
MODULE_TYPE_DAQ_DIO = 5

# AccessMode enum değerleri
ACCESS_MODE_WRITE_WITH_RESET = 2

# Bit manipülasyon sabitleri (Java kodundan)
BIT_CAMERA = 1  # Bit 1: Kamera kontrolü
BIT_FLASH = 2  # Bit 2: Flash kontrolü


class USB4751L_DigitalOutput:
    def __init__(self, device_name=None):
        self.device_handle = c_handle(0)  # 64-bit handle
        self.module_handle = c_handle(0)  # 64-bit handle
        self.current_signal = 0xFF  # Başlangıç: tüm bitler 1
        self.dll = None
        self.device_name = device_name or "USB-4751L"

        # DLL'i yükle
        self._load_dll()

    def _load_dll(self):
        """BDaq DLL'ini yükle"""
        dll_paths = [
            "biodaq.dll",  # En yaygın isim
            "bdaqctrl.dll",
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"),
                         "Advantech", "DAQNavi", "Bin", "biodaq.dll"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
                         "Advantech", "DAQNavi", "Bin", "biodaq.dll"),
            os.path.join(os.environ.get("SystemRoot", "C:\\Windows"),
                         "System32", "biodaq.dll"),
        ]

        for dll_path in dll_paths:
            try:
                self.dll = ctypes.WinDLL(dll_path)
                self._setup_function_signatures()
                return
            except OSError:
                continue

        raise OSError("BDaq DLL bulunamadı. Lütfen Advantech BDaq SDK'yı yükleyin.")

    def _setup_function_signatures(self):
        """C API fonksiyon imzalarını ayarla"""
        # AdxDeviceGetLinkageInfo - cihaz bilgilerini al
        # StringBuffer Java'da char[] olarak geçiliyor, Python'da mutable buffer gerekli
        self.dll.AdxDeviceGetLinkageInfo.argtypes = [
            c_int,  # deviceNumber
            c_int,  # deviceIndex
            POINTER(c_int),  # deviceNumber (out)
            ctypes.c_char_p,  # deviceDesc (out) - StringBuffer
            POINTER(c_int)  # moduleIndex (out)
        ]
        self.dll.AdxDeviceGetLinkageInfo.restype = c_int

        # AdxDeviceOpen - cihazı aç
        # Java: public static native int AdxDeviceOpen(int var0, int var1, LongByRef var2);
        # LongByRef Java'da long için pointer (64-bit)
        self.dll.AdxDeviceOpen.argtypes = [
            c_int,  # deviceNumber
            c_int,  # accessMode
            POINTER(c_handle)  # deviceHandle (out) - 64-bit pointer
        ]
        self.dll.AdxDeviceOpen.restype = c_int

        # AdxDeviceGetModuleHandle - DIO modül handle'ı al
        # Java: public static native int AdxDeviceGetModuleHandle(long var0, int var2, int var3, LongByRef var4);
        # İlk parametre long (64-bit handle)
        try:
            self.dll.AdxDeviceGetModuleHandle.argtypes = [
                c_handle,  # deviceHandle (64-bit)
                c_int,  # moduleType
                c_int,  # moduleIndex
                POINTER(c_handle)  # moduleHandle (out) - 64-bit pointer
            ]
            self.dll.AdxDeviceGetModuleHandle.restype = c_int
        except AttributeError:
            # Alternatif fonksiyon adı olabilir
            pass

        # AdxDoWritePorts - Digital Output port'a yaz
        # Java: public static native int AdxDoWritePorts(long var0, int var2, int var3, byte[] var4);
        # İlk parametre long (64-bit handle), son parametre byte array
        try:
            self.dll.AdxDoWritePorts.argtypes = [
                c_handle,  # moduleHandle (64-bit)
                c_int,  # portStart
                c_int,  # portCount
                POINTER(c_byte)  # data - byte array pointer
            ]
            self.dll.AdxDoWritePorts.restype = c_int
        except AttributeError:
            pass

        # AdxDeviceClose - cihazı kapat
        # Java: public static native int AdxDeviceClose(long var0);
        self.dll.AdxDeviceClose.argtypes = [c_handle]  # 64-bit handle
        self.dll.AdxDeviceClose.restype = c_int

    def list_all_devices(self):
        """Tüm cihazları listele"""
        devices = []
        device_number = c_int(-1)
        device_desc = ctypes.create_string_buffer(256)
        module_index = c_int(0)
        device_index = 0

        while True:
            ret = self.dll.AdxDeviceGetLinkageInfo(
                -1,
                device_index,
                byref(device_number),
                device_desc,
                byref(module_index)
            )

            if device_number.value == -1:
                break

            if ret == ERROR_SUCCESS:
                desc_str = device_desc.value.decode('utf-8', errors='ignore').strip('\x00')
                devices.append((device_number.value, desc_str))

            device_index += 1
            if device_index > 100:  # Güvenlik limiti
                break

        return devices

    def find_device_by_name(self, device_name):
        """Cihaz adına göre cihaz numarasını ve tam adını bul"""
        device_number = c_int(-1)
        device_desc = ctypes.create_string_buffer(256)
        module_index = c_int(0)
        device_index = 0

        # Önce tüm cihazları listele
        all_devices = self.list_all_devices()

        # Tam eşleşme ara (Java kodundaki gibi)
        for dev_num, desc_str in all_devices:
            if device_name == desc_str or device_name in desc_str or desc_str in device_name:
                return dev_num, desc_str

        # Eşleşme bulunamadıysa ilk cihazı dene
        if all_devices:
            dev_num, desc_str = all_devices[0]
            return dev_num, desc_str

        return None, None

    def initialize(self, device_name=None, device_number=None):
        """Cihazı başlat"""
        if device_name:
            self.device_name = device_name

        # Cihaz numarasını bul veya doğrudan kullan
        if device_number is None:
            dev_num, dev_desc = self.find_device_by_name(self.device_name)
            if dev_num is None:
                raise RuntimeError(f"Cihaz bulunamadı: {self.device_name}")
            device_number = dev_num

        # Cihazı aç
        device_handle = c_handle(0)  # 64-bit handle
        ret = self.dll.AdxDeviceOpen(
            device_number,
            ACCESS_MODE_WRITE_WITH_RESET,
            byref(device_handle)
        )

        if ret != ERROR_SUCCESS:
            error_msg = f"Cihaz açılamadı. Hata kodu: {ret} (0x{ret & 0xFFFFFFFF:08X})"
            if ret == -536870896:  # 0xE0000010 - muhtemelen cihaz zaten açık
                error_msg += "\nNot: Cihaz zaten başka bir uygulama tarafından kullanılıyor olabilir."
            raise RuntimeError(error_msg)

        self.device_handle = device_handle

        # DIO modül handle'ını al
        # Java kodunda: deviceRef.Get().GetModule(ModuleType.DaqDio, 0, moduleRef)
        # Bu AdxDeviceGetModuleHandle çağrısı yapıyor

        # Önce modül handle'ı almaya çalış
        module_handle = c_handle(0)  # 64-bit handle
        module_handle_obtained = False

        if hasattr(self.dll, 'AdxDeviceGetModuleHandle'):
            try:
                # Java: BDaqApi.AdxDeviceGetModuleHandle(this.Handle(), type.toInt(), index, moduleHandle);
                # Handle değerini direkt geç (value değil, handle nesnesi)
                ret = self.dll.AdxDeviceGetModuleHandle(
                    self.device_handle,  # Handle nesnesini geç
                    MODULE_TYPE_DAQ_DIO,
                    0,  # moduleIndex
                    byref(module_handle)
                )

                if ret == ERROR_SUCCESS and module_handle.value != 0:
                    self.module_handle = module_handle
                    module_handle_obtained = True
            except Exception as e:
                pass

        # Modül handle alınamadıysa device handle'ı kullan
        if not module_handle_obtained:
            self.module_handle = self.device_handle

        # Başlangıç sinyali gönder (0xFF)
        self.reset_all()

    def write_port(self, port, data):
        """Port 0'a byte değeri yaz (Java: instantDoCtrl.Write(0, signal))"""
        if not hasattr(self, 'module_handle') or self.module_handle.value == 0:
            raise RuntimeError("Cihaz başlatılmamış. initialize() çağrılmalı.")

        # Byte array oluştur (Java'daki gibi: new byte[]{data})
        # Java: byte[] txbuf = new byte[]{data};
        data_array = (c_byte * 1)(data)

        try:
            # Java: AdxDoWritePorts(this.Handle(), port, 1, txbuf)
            # Handle'ı direkt geç (64-bit c_longlong)
            ret = self.dll.AdxDoWritePorts(
                self.module_handle,  # 64-bit handle nesnesini direkt geç
                c_int(port),
                c_int(1),  # portCount
                data_array
            )

            if ret != ERROR_SUCCESS:
                raise RuntimeError(f"Port yazma hatası. Hata kodu: {ret} (0x{ret & 0xFFFFFFFF:08X})")

            return ret

        except OSError as e:
            error_msg = str(e)
            raise RuntimeError(
                f"Port yazma hatası: {error_msg}\n"
                f"Handle: 0x{self.module_handle.value:016X}\n"
                f"Port: {port}, Data: 0x{data:02X}"
            )

    def camera_on(self):
        """Kamera aç: Bit 1'i temizle (Java: signal &= -3 = signal &= 0xFD)"""
        self.current_signal &= 0xFD  # 0b11111101
        self.write_port(0, self.current_signal)
        return self.current_signal

    def camera_off(self):
        """Kamera kapat: Bit 1'i set et (Java: signal |= 2)"""
        self.current_signal |= 0x02  # 0b00000010
        self.write_port(0, self.current_signal)
        return self.current_signal

    def flash_on(self):
        """Flash aç: Bit 2'yi temizle (Java: signal &= -5 = signal &= 0xFB)"""
        self.current_signal &= 0xFB  # 0b11111011
        self.write_port(0, self.current_signal)
        return self.current_signal

    def flash_off(self):
        """Flash kapat: Bit 2'yi set et (Java: signal |= 4)"""
        self.current_signal |= 0x04  # 0b00000100
        self.write_port(0, self.current_signal)
        return self.current_signal

    def reset_all(self):
        """Tüm sinyalleri sıfırla (0xFF) - Java kodundaki başlangıç değeri"""
        self.current_signal = 0xFF
        self.write_port(0, self.current_signal)
        return self.current_signal

    def trigger_flash(self, duration_ms=200):
        """
        Flash tetikle - belirtilen süre boyunca flash'ı aç

        Args:
            duration_ms: Flash'ın açık kalma süresi (milisaniye), varsayılan 200ms
        """
        import time
        self.flash_on()
        time.sleep(duration_ms / 1000.0)
        self.flash_off()

    def trigger_camera_with_flash(self, camera_duration_ms=800, flash_delay_ms=0, flash_duration_ms=200):
        """
        Kamera ve flash'ı senkronize tetikle (Java sendSignal() benzeri)

        Args:
            camera_duration_ms: Kameranın açık kalma süresi (varsayılan 800ms)
            flash_delay_ms: Flash'ın başlama gecikmesi (varsayılan 0ms - kamerayla aynı anda)
            flash_duration_ms: Flash'ın açık kalma süresi (varsayılan 200ms)

        Örnek:
            - t=0ms: Kamera AÇIK
            - t=flash_delay_ms: Flash AÇIK
            - t=flash_delay_ms+flash_duration_ms: Flash KAPALI
            - t=camera_duration_ms: Kamera KAPALI
        """
        import time

        # Kamera aç
        self.camera_on()

        # Flash gecikmesi varsa bekle
        if flash_delay_ms > 0:
            time.sleep(flash_delay_ms / 1000.0)

        # Flash aç
        self.flash_on()

        # Flash süresi kadar bekle
        time.sleep(flash_duration_ms / 1000.0)

        # Flash kapat
        self.flash_off()

        # Kalan kamera süresi varsa bekle
        remaining_camera_time = camera_duration_ms - flash_delay_ms - flash_duration_ms
        if remaining_camera_time > 0:
            time.sleep(remaining_camera_time / 1000.0)

        # Kamera kapat
        self.camera_off()

        # Reset
        self.reset_all()

    def close(self):
        """Cihazı kapat"""
        if hasattr(self, 'device_handle') and self.device_handle.value != 0:
            try:
                self.dll.AdxDeviceClose(self.device_handle)
            except Exception as e:
                pass
            finally:
                self.device_handle = c_handle(0)
                self.module_handle = c_handle(0)


def trigger(delay):
    """Test fonksiyonu - Java kodundaki sendSignal() benzeri"""
    import time

    io = None
    try:
        io = USB4751L_DigitalOutput("USB-4751L")

        try:
            io.initialize()
        except RuntimeError as e:
            raise

        io.camera_on()
        time.sleep(delay / 1000)
        io.flash_on()
        time.sleep(0.2)  # 200ms
        io.flash_off()
        time.sleep(0.8)  # 800ms

        io.camera_off()

    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        if io:
            io.close()

