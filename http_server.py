from contextvars import ContextVar
import os

from aiohttp import web
from aiohttp import streamer

Context = ContextVar("ServerContext")


@streamer
async def file_sender(writer, file_path=None):
    """
    This function will read large file chunk by chunk and send it through HTTP
    without reading them into memory
    """
    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)


async def download_file(request):
    file_name = request.match_info['file_name']  # Could be a HUGE file
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(file_name=file_name)
    }

    file_path = os.path.join('/home/sche/.cache/huggingface/hub', file_name)

    if not os.path.exists(file_path):
        return web.Response(
            body='File <{file_name}> does not exist'.format(
                file_name=file_path),
            status=404
        )

    return web.Response(
        body=file_sender(file_path=file_path),
        headers=headers
    )


async def pong(request):
    # print(f"[SERVER] seq={request.query['seq']}")
    return web.Response(text='pong')


async def alive_peers(request):
    peer_manager = Context.get("peer_manager")
    peers = peer_manager.get_actives()
    return web.json_response(peers)


async def start_server(peer_manager):
    Context.set("peer_manager", peer_manager)

    app = web.Application()

    app.router.add_get('/file/{file_name}', download_file)
    app.router.add_get('/ping', pong)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner=runner, host='0.0.0.0', port=8000)
    await site.start()