from bocadillo import route, websocket_route


@route("/")
async def index(req, res):
    res.text = "OK"


@websocket_route("/echo")
async def echo(ws):
    async for message in ws:
        await ws.send(message)
