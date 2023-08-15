import requests

def send_sms():
    sid = input("Twilio 계정 SID:")
    token = input("인증 토큰:")
    from_number = input("전송번호:")
    to_number = input("문자받을번호:")
    message = input("전송할 메세지:")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    data = {
        "To": to_number,
        "From": from_number,
        "Body": message
    }
    headers = {
        "Authorization": "Basic " + btoa(sid + ":" + token)
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        print("메시지가 전송되었습니다. 인증확인 버튼을 눌러주십시오.")
    except requests.exceptions.RequestException as err:
        print(f"에러 발생! 오류내용: {err}")

send_sms()