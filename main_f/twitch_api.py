import json
import aiohttp

async def subscribe(token: str, client_id: str, session_id: str, condition, sub_type: str, version:str = "1", base_url: str = "https://api.twitch.tv/helix"):
    
    data = {
        "type": sub_type,
        "version": version,
        "condition": condition,
        "transport": {
            "method": "websocket",
            "session_id": session_id
            }
        }
    
    url = f'{base_url}/eventsub/subscriptions'
    b = json.dumps(data)
    print(f"request {url}: {b}")
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Client-Id": client_id,
        "Content-Type": "application/json"
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers = headers, data = b) as response:
            body = await response.text()
            print(body)

async def clean_subscriptions(token: str, client_id: str, base_url: str = "https://api.twitch.tv/helix"):
    print("cleanup old subscriptions...")
    
    url = f'{base_url}/eventsub/subscriptions'
    
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Client-Id": client_id,
        "Content-Type": "application/json"
        }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = headers) as response:
            body = await response.json()
            for sub in body['data']:
                if 'disconnected_at' in sub['transport']:
                    #print(sub)
                    del_url = f"{url}?id={sub['id']}"
                    async with session.delete(del_url, headers = headers) as del_response:
                        if del_response.status == 204:
                            print(f"removed subscription with id {sub['id']}")
                        else:
                            print(f"failed to remove subscription with id {sub['id']}")
    
    print("done cleaning up old subscriptions!")