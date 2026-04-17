from app.news.vtomske import process_vtomske
import asyncio

async def main():

    result = await process_vtomske()

    print(result)

async def process_all_site():
    while True:
        
        result = await process_vtomske()

        print(result)

        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(process_all_site())