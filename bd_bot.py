# тестовый файл
import atexit
import requests
import time
from data import db_session
from data.Game import Game
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

db_lock = threading.Lock()

last_appid = 0
last_appid_lock = threading.Lock()


def get_game_name(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data is not None:
            if str(appid) in data and data[str(appid)]["success"]:
                return data[str(appid)]["data"]["name"]
        return ""
    except:
        return ""


def process_appid(appid):
    global last_appid

    print(appid)

    stats_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    try:
        stats_response = requests.get(stats_url, timeout=10)
        stats_data = stats_response.json()

        if "response" in stats_data and "player_count" in stats_data["response"]:
            count = stats_data["response"]["player_count"]
            if count > 1000:
                name = get_game_name(appid)
                if name:
                    game = Game()
                    game.name = name
                    game.steam_id = appid

                    db_sess = db_session.create_session()
                    db_sess.add(game)
                    db_sess.commit()
                    print(f"Added game: {name}, appid: {appid}")

    except Exception as e:
        print(f"Error processing appid {appid}: {e}")

    time.sleep(1)
    return appid


def main():
    db_session.global_init("db/nebalatro.db")

    num_threads = 3

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_appid, appid) for appid in range(1171425, 2000000)]

        for future in as_completed(futures):
            try:
                appid = future.result()
            except Exception as e:
                print(f"Error in future: {e}")


if __name__ == "__main__":
    main()
