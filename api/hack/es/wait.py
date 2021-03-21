import time

import requests

from core.config import ELASTIC_HOST, ELASTIC_PORT

if __name__ == "__main__":
    print("Checking elasticsearch readiness: ", end="")
    while True:
        try:
            resp = requests.head(f"http://{ELASTIC_HOST}:{ELASTIC_PORT}", timeout=1)
            if resp.status_code == 200:
                print("✔")
                break
        except requests.ConnectionError:
            pass

        print('.', end='')
        time.sleep(1)
