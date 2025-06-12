from sensors import TempSensor, asyncio, sys

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def main():
        temp_sensor = TempSensor()
        await temp_sensor.start()

    asyncio.run(main())