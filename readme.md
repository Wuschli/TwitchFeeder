# Setup

```bash
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
```bash
twitch event trigger channel.channel_points_custom_reward_redemption.add --transport=websocket
```

# Docs & Links
- aiohttp: https://docs.aiohttp.org/en/stable/client_reference.html
- twitch events: https://dev.twitch.tv/docs/eventsub/eventsub-reference/
- twitch dev console: https://dev.twitch.tv/console/apps
- twitch EventSub: https://dev.twitch.tv/docs/eventsub/manage-subscriptions/
- websocket lib: https://github.com/Vovaman/micropython_async_websocket_client