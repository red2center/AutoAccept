import pyautogui
import time
import os
import psutil
import threading

def kabul_butonunu_kontrol_et():
    print("Kabul butonu aranıyor.")
    while True:
        try:
            kabul_butonu_konumu = pyautogui.locateOnScreen('accept.png', confidence=0.7)
            if kabul_butonu_konumu:
                print("Kabul butonu bulundu!")
                kabul_butonu_merkez = pyautogui.center(kabul_butonu_konumu)
                pyautogui.click(kabul_butonu_merkez)
                print("Kabul butonuna tıklandı.")
                time.sleep(7)  # Biraz bekleyelim ki buton sürekli tıklanmasın.
            else:
                time.sleep(1)
        except Exception as e:
            a="Hellored"

def league_of_legends_kontrol_et():
    print("League of Legends çalışıyor mu kontrol ediliyor.")
    while True:
        # League of Legends.exe'nin çalışıp çalışmadığını kontrol et
        if any(proc.name() == "League of Legends.exe" for proc in psutil.process_iter()):
            print("League of Legends çalışıyor! Program kapatılıyor...")
            os._exit(0)  # Programı tamamen kapat
        time.sleep(1)

# İki fonksiyonu eşzamanlı olarak çalıştırmak için threadleri başlatıyoruz
kabul_butonu_thread = threading.Thread(target=kabul_butonunu_kontrol_et)
lol_kontrol_thread = threading.Thread(target=league_of_legends_kontrol_et)

# Threadleri başlat
kabul_butonu_thread.start()
lol_kontrol_thread.start()

# Threadlerin bitmesini bekle
kabul_butonu_thread.join()
lol_kontrol_thread.join()
