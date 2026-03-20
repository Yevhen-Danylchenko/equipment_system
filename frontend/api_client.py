import requests

BASE_URL = "http://127.0.0.1:8000/equipment"

class ApiClient:
    def get_equipment(self):
        resp = requests.get(BASE_URL)
        return resp.json() if resp.status_code == 200 else []

    def update_status(self, equipment_id, status):
        resp = requests.put(f"{BASE_URL}/{equipment_id}/status", params={"status": status})
        return resp.json() if resp.status_code == 200 else {"error": resp.text}

    def move_equipment(self, equipment_id, to_room):
        resp = requests.put(f"{BASE_URL}/{equipment_id}/move", params={"to_room": to_room})
        return resp.json() if resp.status_code == 200 else {"error": resp.text}

    def get_stats(self):
        resp = requests.get(f"{BASE_URL}/stats")
        return resp.json() if resp.status_code == 200 else {}