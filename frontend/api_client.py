import requests

BASE_URL = "http://127.0.0.1:8000/equipment"

class ApiClient:
    def get_equipment(self):
        try:
            resp = requests.get(BASE_URL)
            return resp.json() if resp.status_code == 200 else []
        except requests.exceptions.RequestException as e:
            return []

    def update_status(self, equipment_id, status):
        try:
            resp = requests.put(f"{BASE_URL}/{equipment_id}/status", json={"status": status})
            return resp.json() if resp.status_code == 200 else {"error": resp.text}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def move_equipment(self, equipment_id, to_room):
        try:
            resp = requests.put(f"{BASE_URL}/{equipment_id}/move", json={"to_room": to_room})
            return resp.json() if resp.status_code == 200 else {"error": resp.text}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_stats(self):
        try:
            resp = requests.get(f"{BASE_URL}/stats")
            return resp.json() if resp.status_code == 200 else {}
        except requests.exceptions.RequestException:
            return {}