# тестовый файл
import requests
import time

game_ids = [570, 730, 578080, 271590]  # Dota 2, CS2, PUBG, GTA V


def get_game_name(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    data = response.json()

    if str(appid) in data and data[str(appid)]["success"]:
        return data[str(appid)]["data"]["name"]
    return "Неизвестная игра"


for appid in game_ids:
    # Проверяем онлайн
    stats_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    stats_response = requests.get(stats_url)
    stats_data = stats_response.json()

    if "player_count" in stats_data["response"]:
        count = stats_data["response"]["player_count"]
        if count > 1000:
            name = get_game_name(appid)
            print(f"{name} (ID: {appid}) — {count:,} игроков онлайн".replace(",", " "))
    time.sleep(1)
