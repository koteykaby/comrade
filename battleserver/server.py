import asyncio;
from websockets.asyncio.server import serve;
from websockets.exceptions import ConnectionClosed;
import json;
import ssl;

#v2
import zlib
from hexdump import hexdump

with open('config/config.json', 'r') as file:
    cfg = json.load(file);
    cfg_b = cfg["battleserver"];
    cfg_ssl = cfg["ssl"]

ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);
ssl_ctx.load_cert_chain(cfg_ssl["cert"], cfg_ssl["key"]);

queues = {};

async def sender(conn, queue):
    while True:
        data = await queue.get();
        if data == None: break;
        await conn.send(data);

async def ws_handler(conn):
    host, port = conn.local_address;
    peer, pport = conn.remote_address;
    cur_queue = asyncio.Queue();
    queues[port] += [cur_queue];
    asyncio.create_task(sender(conn, cur_queue));
    try:
        while True:
            data = await conn.recv();
            print(f"recv {peer}:{pport} -> {host}:{port}: {data}");
            #v2
            print(hexdump(data))
            zlib_start = data.find(b'\x78\x01')
            if zlib_start != -1:
                try:
                    zlib_data = data[zlib_start:]
                    decompressed = zlib.decompress(zlib_data)
                    print('Packet is compressed! Decompressed view:')
                    print(hexdump(decompressed))
                except zlib.error as e:
                    print(f"error: {e}")
            for q in queues[port]:
                await q.put(data);
    except ConnectionClosed:
        print(f"peer {peer}:{pport} disconnected from {port}");
    # connection closed, shutdown sender
    await cur_queue.put(None);
    queues[port].remove(cur_queue);

async def ws_server(port):
    print(f"Listening at {port}!");
    # holy akatosh, i hate asyncio already, just let me rewrite it with tokio
    async with serve(ws_handler, cfg_b["address"], port, ssl=ssl_ctx) as server:
        await server.serve_forever();

async def main():
    # spawning server for each port
    tasks = [];
    for port in cfg_b["ports"]:
        queues[port] = [];
        tasks.append(asyncio.create_task(ws_server(port)));
    # and awaiting spawned tasks
    for task in tasks:
        await task;

if __name__ == "__main__":
    asyncio.run(main());