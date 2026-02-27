import requests
import json
import traceback

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": "https://www.mangago.me/",
    "Cookie": "_m_superu=1;"
}

session = requests.Session()
session.headers.update(HEADERS)

def test_popular_manga():
    print("Testing Popular Manga...")
    try:
        url = "https://www.mangago.me/genre/all/1/?f=1&o=1&sortby=view&e="
        res = session.get(url)
        print(f"Status Code: {res.status_code}")
        if res.status_code != 200:
            print("Response:", res.text[:500])
    except Exception as e:
        traceback.print_exc()

def test_latest_updates():
    print("Testing Latest Updates...")
    try:
        url = "https://www.mangago.me/genre/all/1/?f=1&o=1&sortby=update_date&e="
        res = session.get(url)
        print(f"Status Code: {res.status_code}")
        if res.status_code != 200:
            print("Response:", res.text[:500])
    except Exception as e:
        traceback.print_exc()

def test_search():
    print("Testing Search...")
    try:
        url = "https://www.mangago.me/r/l_search/?name=action&page=1"
        res = session.get(url)
        print(f"Status Code: {res.status_code}")
        if res.status_code != 200:
            print("Response:", res.text[:500])
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    test_popular_manga()
    print("-" * 40)
    test_latest_updates()
    print("-" * 40)
    test_search()

