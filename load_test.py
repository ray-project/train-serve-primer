from collections import defaultdict
import aiohttp
import asyncio
import json
import time

with open('token.txt', 'r') as f:
    token = f.read()
    
hostname = "service-demo-xa4v3.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com"
headers = {"Authorization": f"Bearer {token}"}
parallelism = 100

sample_json = '{ "user_input" : "hello", "history":[] }'

async def get(session, i):
    for i in range(3):
        try:
            async with session.post(url=f"https://{hostname}/", headers=headers, json=sample_json) as response:
                return await response.json()
        except Exception:
            await asyncio.sleep(0.5)

async def get_parallel():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(
            *(get(session, i) for i in range(parallelism)), return_exceptions=True
        )
        return result

async def run_iter():
    result = await get_parallel()

    aggregate = defaultdict(lambda: 0)
    aggregate["error"] = 0
    for s in result:
        a = str(s)
        aggregate[a] += 1
    return aggregate

async def main():
    while True:
        await asyncio.sleep(1)
        start = time.time()
        aggregate = await run_iter()
        print(f"actual elapsed {time.time()-start}")
        with open('data.txt', mode='a') as output:
            output.write(json.dumps(aggregate) + "\n")

if __name__ == "__main__":
    asyncio.run(main())
