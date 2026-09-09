import requests
import time
from supabase import create_client

# Supabase Credentials
SUPABASE_URL = "https://pxptveroxnlmqfvzvols.supabase.co"
SUPABASE_KEY = "sb_publishable_x-19yQUi1dFT5cZnjg0zkg_iqduJuyZ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# API Details
API_URL = "https://6lotteryapi.com/api/webapi/GetTRXNoaverageEmerdList"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,my;q=0.8",
    "ar-origin": "https://6win598.com",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzg4OTM1OTUzIiwibmJmIjoiMTc4ODkzNTk1MyIsImV4cCI6IjE3ODg5Mzc3NTMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI5LzkvMjAyNiAxOjM5OjEzIFBNIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQWNjZXNzX1Rva2VuIiwiVXNlcklkIjoiMTE1MDIyMSIsIlVzZXJOYW1lIjoic29ldGh1dGh1bWcyQGdtYWlsLmNvbSIsIlVzZXJQaG90byI6IjE1IiwiTmlja05hbWUiOiJNZW1iZXJOTkdSSkJYOSIsIkFtb3VudCI6IjUyOTczLjQwIiwiSW50ZWdyYWwiOiIwIiwiTG9naW5NYXJrIjoiSDUiLCJMb2dpblRpbWUiOiI5LzkvMjAyNiAxOjA5OjEzIFBNIiwiTG9naW5JUEFkZHJlc3MiOiI0NS4xOTIuMTQwLjE4MyIsIkRiTnVtYmVyIjoiMCIsIklzdmFsaWRhdG9yIjoiMSIsIktleUNvZGUiOiIxMjciLCJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJQaG9uZVR5cGUiOiIwIiwiVXNlclR5cGUiOiIwIiwiVXNlck5hbWUyIjoiIiwiaXNzIjoiand0SXNzdWVyIiwiYXVkIjoibG90dGVyeVRpY2tldCJ9.YI8rHZVRaFobzAyZU8ysw9FVMfOx3OuDCYwspqAUV6E",
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
