from ws import AsyncWebsocketClient
import network as net
import asyncio as a
import gc
import json
import aiohttp

from .twitch_api import subscribe, clean_subscriptions

print("Trying to load config...")

f = open("../config.json")
text = f.read()
f.close()
config = json.loads(text)
del text

print("Create WS instance...")
ws = AsyncWebsocketClient(config['socket_delay_ms'])

session_id: str = None

async def wifi_connect(SSID: str, pwd: str, attempts: int = 3, delay_in_ms: int = 200) -> net.WLAN:
    
    wifi = net.WLAN(net.STA_IF)
    wifi.active(1)
    count = 1
    
    while not wifi.isconnected() and count <= attempts:
        print("WiFi connectint. Attempts {}.".format(count))
        if wifi.status() != net.STAT_CONNECTING:
            wifi.connect(SSID, pwd)
        await a.sleep_ms(delay_in_ms)
        count += 1
        
    if wifi.isconnected():
        print("ifconfig: {}".format(wifi.ifconfig()))
    else:
        print("WiFi not connected!")
    
    return wifi
        
async def twitch_loop():
    wifi = await wifi_connect(config["wifi"]["SSID"], config["wifi"]["password"])
    
    while True:
        gc.collect()
        
        if not wifi.isconnected():
            wifi = await wifi_connect(config["wifi"]["SSID"], config["wifi"]["password"])
            if not wifi.isconnected():
                await a.sleep_ms(config["wifi"]["SSID"], config["wifi"]["delay_in_ms"])
                continue
            
        try:
            await clean_subscriptions(config['twitch']['access_token'], config['twitch']['client_id'], config['twitch']['base_url'])
        except Exception as ex:
            print("Failed to cleanup subscriptions: {}".format(ex))
            
        
        try:
            print("Handshaking...")
            
            kw = {}
            if config["server"].startswith("wss"):
                ssl = config.get("ssl", {})
                kw["keyfile"] = ssl.get("key")
                kw["certfile"] = ssl.get("cert")
                kw["cafile"] = ssl.get("ca")
                kw["cert_reqs"] = ssl.get("cert_reqs")
            
            if not await ws.handshake(config["server"], **kw):
                raise Exception("Handshake error.")
            print("... handshaked.")
            
            while await ws.open():
                data = await ws.recv()
                
                if data is not None:
                    msg = json.loads(data)
                    print(msg)
                    await handle_message(msg);
                
                await a.sleep_ms(config['socket_delay_ms'])
                
        except Exception as ex:
            print("Exception: {}".format(ex))
            await a.sleep(1)
            
async def handle_message(msg):
    msg_type = msg['metadata']['message_type']
    if msg_type == "session_welcome":
        session_id = msg['payload']['session']['id']
        print(session_id)
        
        access_token = config['twitch']['access_token']
        client_id = config['twitch']['client_id']
        base_url = config['twitch']['base_url']
        
        condition = {"broadcaster_user_id": config['twitch']['broadcaster_user_id'], "moderator_user_id": config['twitch']['moderator_user_id']}
        await subscribe(access_token, client_id, session_id, condition, "channel.follow", "2", base_url)
        
        condition = {"broadcaster_user_id": config['twitch']['broadcaster_user_id']}
        await subscribe(access_token, client_id, session_id, condition, "channel.channel_points_custom_reward_redemption.add", "1", base_url)
        