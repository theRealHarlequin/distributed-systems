from sensors import PresSensor, asyncio, sys

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def main():
        pres_sensor = PresSensor()
        await pres_sensor.start()

    asyncio.run(main())