import requests
import time
from supabase import create_client

# Supabase Credentials
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# API Details
API_URL = "https://6lotteryapi.com/api/webapi/GetTRXNoaverageEmerdList"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,my;q=0.8",
    "ar-origin": "https://6win598.com",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzg4OTI3NTA0IiwibmJmIjoiMTc4ODkyNzUwNCIsImV4cGlyYXRpb24iOiI5LzkvMjAyNiAxMToxODoyNCBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjExNTAyMjEiLCJVc2VyTmFtZSI6InNvZXRodXRodW1nMkBnbWFpbC5jb20iLCJVc2VyUGhvdG8iOiIxNSIsIk5pY2tOYW1lIjoiTWVtYmVyTk5HUkpCWDkiLCJBbW91bnQiOiI1Mjk3My40MCIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiOS85LzIwMjYgMTA6NDg6MjQgQU0iLCJMb2dpbklQQWRkcmVzcyI6IjQ1LjE5Mi4xNDAuMTgzIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIxIiwia2V5Q29kZSI6IjEyNiIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjAiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.1c03jv2HpKvF5N-GY3Oq9sawngZWJPcYDQuBdBi1gyc",
    "content-type": "application/json;charset=UTF-8",
    "referrer": "https://6win598.com/"
}

PAYLOAD = {
    "pageSize": 10,
    "pageNo": 1,
    "typeId": 13,
    "language": 0,
    "random": "036516a0f4174441960300e3d955f5a1",
    "signature": "839C268CEAF4F7C37C880BF504635245",
    "timestamp": 1788928861
}

def fetch_and_store_data():
    try:
        response = requests.post(API_URL, json=PAYLOAD, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("code") == 0 and "data" in res_json:
                list_data = res_json["data"].get("list", [])
                for item in list_data:
                    period = str(item.get("issueNumber") or item.get("period"))
                    number = int(item.get("number"))
                    result = "B" if number >= 5 else "S"
                    
                    supabase.table("bs_history").upsert({
                        "period": period,
                        "number": number,
                        "result": result
                    }).execute()
                print(f"[Success] Updated {len(list_data)} records into Supabase.")
            else:
                print(f"[API Error] {res_json}")
        else:
            print(f"[HTTP Error] Status Code: {response.status_code}")
    except Exception as e:
        print(f"[Execution Error] {e}")

if __name__ == "__main__":
    fetch_and_store_data()
