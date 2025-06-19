import asyncio as a
from main_f import twitch_loop

async def main():
    
    tasks = [twitch_loop()]
    await a.gather(*tasks)

a.run(main())