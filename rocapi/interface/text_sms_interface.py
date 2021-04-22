import requests
from backend_roc.utils.const import OTP_API_URL


def send_text(mobile_no, message):
    try:
        text_url = OTP_API_URL
        text_url = text_url.replace('<mobile_no>', mobile_no).replace('<msg>', message)
        print(f"text_url:{text_url}")
        response = requests.request(
           "GET",
           text_url,
        )
        status_code = response.status_code
        if status_code == 200:
            resp_text = response.text
            print(resp_text)
            return "success"
            # if "SHOOT" in resp_text:
            #     # print("ststus ", resp_text)
            #     return "success"
        return "failed"
    except:
        return "failed"
