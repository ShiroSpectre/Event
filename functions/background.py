import db
import time
import discord
import asyncio
import tracemalloc

class BackgroundTasks():
    def __init__(self):
        self.alert_time = db.alert_time

    async def initialize(self):
        print('backgroundtasks...')
        # run functions
        await BackgroundTasks().alert_before_event()
        await BackgroundTasks().track_ram_usage()
        
        await asyncio.sleep(60)
        await BackgroundTasks().initialize()

    async def alert_before_event(self):
        events = db.event_dates
        for i in range(len(events)):
            event_time = time.mktime(events[i].timetuple())
            if int(event_time - time.time()) < self.alert_time:
                present_users = db.present_users
                users = present_users[i]
                for user in users:
                    await user.send('Upcoming event in 15min')
                    await asyncio.sleep(5)
                del events[i]
                del present_users[i]
                db.event_dates = events
                db.present_users = present_users

    async def track_ram_usage(self):
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")


