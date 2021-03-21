import socket
import time

from core.config import REDIS_HOST, REDIS_PORT

if __name__ == "__main__":
    print("Checking redis readiness: ", end="")
    while True:
        try:
            sock = socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=1)
            sock.send("PING\n".encode())
            resp = sock.recv(1024)
            if resp.decode() == "+PONG\r\n":
                print("✔")
                break
        except OSError:
            pass

        print('.', end='')
        time.sleep(1)
