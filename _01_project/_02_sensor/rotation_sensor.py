from sensors import RotSensor, asyncio, sys

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def main():
        rot_sensor = RotSensor()
        await rot_sensor.start()

    asyncio.run(main())