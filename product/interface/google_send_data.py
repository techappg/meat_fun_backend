
import requests

from backend_roc.utils.google_map import G_MAP

def send_google_text(origins_lat, origins_long, dest_lat, dest_long):
    try:
        text_url = G_MAP
        text_url = text_url.replace('<lat_A>', origins_lat).replace('<long_A>', origins_long).replace('<lat_B>',dest_lat).replace('<long_B>', dest_long)
        print(f"text_url:{text_url}")
        response = requests.request(
           "GET",
           text_url,
        )
        return response
    except:
        return "failed"