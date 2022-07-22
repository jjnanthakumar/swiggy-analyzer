import requests
import json
import sys

HEADERS = {
    'Host': 'www.swiggy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.swiggy.com/my-account/orders',
    'Content-Type': 'application/json'
}

GET_ORDERS_URL = 'https://www.swiggy.com/dapi/order/all?order_id='


def getOrders(cookies):
    print("Retrieving orders...")
    spent = 0
    s = requests.Session()
    last_order_id = ''
    num_of_orders = 0
    while True:
        # 10 orders retrieved in each api call
        URL = GET_ORDERS_URL + \
            str(last_order_id).strip() if last_order_id != '' else GET_ORDERS_URL
        r = s.get(URL, headers=HEADERS, cookies=cookies)
        resp = json.loads(r.text)
        if resp['statusCode'] == 1:
            print("Status Code is 1, exiting")
            break

        if len(resp['data']['orders']) == 0:
            print("Reached end of orders")
            break
        for order in resp['data']['orders']:
            order_total = order['order_total']
            # print(order_total)
            spent += order_total
        num_of_orders += len(resp['data']['orders'])

        last_order_id = resp['data']['orders'][-1]['order_id']

    average_spent = spent//num_of_orders
    print()
    print(
        f"Total money spent on swiggy.com : INR {spent:,}")
    print(
        f"Total number of orders placed : {num_of_orders:,}")
    print(
        f"Average money spent on each order : INR {average_spent:,}")


def cookiesToDict():
    print("Getting cookies from cookies.json")
    data = None
    try:
        with open("cookies.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("cookies.json not found in the path")
        print(str(e))
        return None

    try:
        cookies = {e['name']: e['value'] for e in data}
    except Exception as e:
        print("Cookies are not in proper format")
        print(str(e))
        return None

    return cookies


def checkLogin(cookies):
    # First check if logged in
    print("Checking if session is valid")
    r = requests.get(GET_ORDERS_URL, headers=HEADERS, cookies=cookies)
    resp = None
    try:
        resp = json.loads(r.text)
    except Exception as e:
        print("Unexpected Response received")
        return False

    if 'statusCode' not in resp or 'data' not in resp:
        print("Unexpected Response received")
        return False
    if resp['statusCode'] == 1:
        print("Not logged in, check cookies and try again")
        return False

    return True


if __name__ == "__main__":
    print("Started Script..:vampire:")
    cookies = cookiesToDict()
    if cookies is None:
        sys.exit()
    if checkLogin(cookies):
        getOrders(cookies)
