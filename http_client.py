import random
import time
import aiohttp
import os

import aiohttp
import aiohttp.client_exceptions


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
                    peers = await response.json()
    except aiohttp.client_exceptions.ClientConnectionError:
        print(f"Make sure the HFFS service is up by running: python hffs.py start")
    finally:
        return peers
