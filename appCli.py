import selectors
import socket
import sys
import traceback

import messCli

sel = selectors.DefaultSelector()

def start_connection(host, port, request):
    addr = (host,port)
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors .EVENT_READ | selectors.EVENT_WRITE
    message = messCli.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

try:
    while True:
        events = sel.select(timeout = 1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    f"Main: Error: Exception for {message.addr}"
                    f"{traceback.format_exc()}"
                )
                message.close()
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()