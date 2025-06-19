# Setup

```
scoop install pipx
pipx ensurepath
pipx install mpremote
mpremote mip install aiohttp
mpremote mip install github:Vovaman/micropython_async_websocket_client/async_websocket_client/ws.py

scoop bucket add twitch https://github.com/twitchdev/scoop-bucket.git
scoop install twitch-cli

twitch token -u -s "moderator:read:followers channel:read:redemptions"

twitch event websocket start-server --ip "10.0.0.XXX"

```

# Test Twitch Events
```
twitch event trigger channel.channel_points_custom_reward_redemption.add --transport=websocket
```