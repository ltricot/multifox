import asyncio as aio
from asyncio import subprocess as sp
import json
import ssl

import socketio


URI = 'wss://wsfoxdot-nm5dxx2vwq-ey.a.run.app'
# URI = 'ws://localhost:3000'

async def sclang():
    proc = await sp.create_subprocess_shell(
        'sclang',
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )

    # start foxdot sc extension (udp server)
    proc.stdin.write(b'Quarks.install("FoxDot");\n\x0c')
    proc.stdin.write(b'FoxDot.start();\n\x0c')
    await proc.stdin.drain()

    async def _():  # rid the world of garbage
        while (bts := await proc.stdout.readline()):
            # print(bts.decode().strip())
            ...

    aio.create_task(_())

    return proc

async def foxdot():
    global pfoxdot

    # provides no stdout
    proc = await sp.create_subprocess_shell(
        'python -m FoxDot --pipe',
        stdin=sp.PIPE,
    )

    return proc

async def repl(sio):
    async def handler(reader, writer):
        while True:
            lines = []
            while True:
                line = await reader.readline()

                if not line:
                    return

                if line == b'\n':
                    break

                lines.append(line)

            code = b'\n'.join(l.rstrip(b'\n') for l in lines).decode()
            print(code)

            await sio.emit('code', {"code": code})

    await aio.start_unix_server(handler, path='/tmp/foxdot.sock')

async def main():
    sc = await sclang()
    await aio.sleep(5)
    fox = await foxdot()

    sio = socketio.AsyncClient()
    await sio.connect(URI)

    @sio.on('code')
    async def doeval(msg):
        code = msg['code']
        fox.stdin.write(code.encode() + b'\n' * 3)
        await fox.stdin.drain()

    trepl = aio.create_task(repl(sio))
    teval = aio.create_task(doeval(sio))

    try:
        await aio.sleep(3600)
    except KeyboardInterrupt:
        await trepl.cancel()
        await teval.cancel()
        await sio.disconnect()
    finally:
        return


aio.run(main())
