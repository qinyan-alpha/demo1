#You can find the intiface central development manual here, and here is a simple demo for your reference.
#https://buttplug-developer-guide.docs.buttplug.io/docs/spec/architecture/
#This demo should allow you to test any linear device.(osr2 sr6 handy ssr)
#After establishing a connection with intiface central using the websocket library in any programming language.
#Tell intiface central who is connected to it and start getting available devices.
#Select one of LinearCmd, RotateCmd, or ScalarCmd control method according to the device type.
#Since I only have the LinearCmd device this demo can only be tested like this.



import websocket
import _thread
import threading
import time
import rel
import json

def on_message(ws, message):
    print(f"get message: {message}")

def on_error(ws, error):
    print(f"error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### socket has been closed###")

def on_open(ws):
    print("builded connection")
    def run(*args):
        # Create LinearCmd messages
        handshake_msg = {
            "RequestServerInfo": {
                "Id": 1,
                "ClientName": "Python Test Client",
                "MessageVersion": 1
            }
        }
        ws.send(json.dumps([handshake_msg]))

        requestdevicelist ={
            "RequestDeviceList": {
            "Id": 1
            }
        }
        ws.send(json.dumps([requestdevicelist]))
        startScanning ={
            "StartScanning": {
            "Id": 1
            }
        }     
        ws.send(json.dumps([startScanning]))
        time.sleep(1)
        stopscanning ={
            "StopScanning": {
            "Id": 1
            }
        }
        ws.send(json.dumps([stopscanning]))                
        time.sleep(1)
        linearcmd = {
        "LinearCmd": {
        "Id": 1,
        "DeviceIndex": 0,
        "Vectors": [
            {
            "Index": 0,
            "Duration": 1000,# Just make sure it's an integer greater than 0, in milliseconds.
            "Position": 1,# Percentages are calculated in the range 0-100.
            },
            ]*1
        }
        }
        
        ws.send(json.dumps([linearcmd]))
        ws.close()
        print("线程终止...")

    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:12345",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    #ws.send("")
    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)  # Ctrl+C exit
    rel.dispatch()