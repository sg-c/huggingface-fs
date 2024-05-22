import asyncio
import time
import aiohttp
import os

import aiohttp
import aiohttp.client_exceptions

from peer import Peer


async def ping(peer):
    alive = False
    seq = os.urandom(4).hex()

    print("[CLIENT]: probing", peer.ip, peer.port, seq)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{peer.ip}:{peer.port}/ping?seq={seq}") as response:
                if response.status == 200:
                    alive = True
    finally:
        peer.set_alive(alive)
        peer.set_epoch(int(time.time()))

        print(
            f"[CLIENT]: Peer {peer.ip}:{peer.port} (seq:{seq}) is {'alive' if alive else 'dead'}")
        return peer


async def alive_peers():
    peers = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://127.0.0.1:8000/alive_peers") as response:
                if response.status == 200:
                    peer_list = await response.json()
                    peers = [Peer.from_dict(peer) for peer in peer_list]
    except aiohttp.client_exceptions.ClientConnectionError:
        print(f"Make sure the HFFS service is up by running: python hffs.py start")
    finally:
        return peers


async def timeout_coro(coro, timeout, default):
    async def _():
        try:
            return await asyncio.wait_for(coro, timeout)
        except TimeoutError:
            return default
    return _()


async def search_coro(peer, repo_id, revision, file_name):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(f"http://{peer.ip}:{peer.port}/model/{repo_id}/resolve/{revision}/{file_name}") as response:
                if response.status == 200:
                    return True
    except Exception:
        return False


async def search_model(peers, repo_id, revision, file_name):
    if not peers:
        return []

    def gen_coro(peer):
        # for each peer, create a search corotine, and wrap it into
        # timeout corotine, so that they can finish withing 10 sec
        search = search_coro(peer, repo_id, revision, file_name)
        timeout = timeout_coro(search, 10, False)

    coros = [gen_coro(p) for p in peers]
    parallel = asyncio.gather(coros, True)
    task = asyncio.create_task(parallel)

    while not task.done():
        await asyncio.sleep(1)
        print(".", end="")

    results = await task
    return [r for r in results if not isinstance(r, Exception)]
