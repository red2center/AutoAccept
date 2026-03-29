import pyautogui
import time
import psutil
import threading
import traceback

# LoL/Riot process isimleri (ihtiyaca göre ekleyebilirsin)
LOL_PROCESS_NAMES = {
    "League of Legends.exe",
    "LeagueClient.exe",
    "RiotClientServices.exe",
}

ACCEPT_IMAGE = "accept.png"
CONFIDENCE = 0.7
THREAD_JOIN_TIMEOUT_SECONDS = 5


def kabul_butonunu_kontrol_et(stop_event: threading.Event):
    print("Kabul butonu aranıyor.")
    while not stop_event.is_set():
        try:
            kabul_butonu_konumu = pyautogui.locateOnScreen(ACCEPT_IMAGE, confidence=CONFIDENCE)
            if kabul_butonu_konumu:
                print("Kabul butonu bulundu!")
                kabul_butonu_merkez = pyautogui.center(kabul_butonu_konumu)
                pyautogui.click(kabul_butonu_merkez)
                print("Kabul butonuna tıklandı.")
                # stop_event.wait kullanımı: hem gecikme sağlar hem de kapatma sinyalinde beklemez
                stop_event.wait(7)
            else:
                stop_event.wait(1)
        except Exception as e:
            print(f"[HATA] kabul_butonunu_kontrol_et: {e}")
            traceback.print_exc()
            stop_event.wait(1)


def league_of_legends_kontrol_et(stop_event: threading.Event):
    print("League/Riot çalışıyor mu kontrol ediliyor.")
    while not stop_event.is_set():
        try:
            for proc in psutil.process_iter(attrs=["name"]):
                name = proc.info.get("name")
                if name in LOL_PROCESS_NAMES:
                    print(f"{name} çalışıyor! Program düzgün şekilde kapatılıyor...")
                    stop_event.set()
                    return
        except Exception as e:
            print(f"[HATA] league_of_legends_kontrol_et: {e}")
            traceback.print_exc()

        stop_event.wait(1)


def main():
    stop_event = threading.Event()

    kabul_butonu_thread = threading.Thread(
        target=kabul_butonunu_kontrol_et, args=(stop_event,)
    )
    lol_kontrol_thread = threading.Thread(
        target=league_of_legends_kontrol_et, args=(stop_event,)
    )

    kabul_butonu_thread.start()
    lol_kontrol_thread.start()

    try:
        # stop_event set olana kadar bekle
        while not stop_event.is_set():
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("CTRL+C algılandı, program kapatılıyor...")
        stop_event.set()
    finally:
        kabul_butonu_thread.join(timeout=THREAD_JOIN_TIMEOUT_SECONDS)
        lol_kontrol_thread.join(timeout=THREAD_JOIN_TIMEOUT_SECONDS)
        print("Program kapandı.")


if __name__ == "__main__":
    main()
