import asyncio
from interface import view

loop = asyncio.get_event_loop()
task1 = loop.create_task(view())
loop.run_until_complete(asyncio.wait([task1]))  