from types import SimpleNamespace

import pytest
from tests.modules import router

NAMESPACE = SimpleNamespace(index=router.index, echo=router.echo)


@pytest.mark.parametrize("source", (router, NAMESPACE))
def test_discover_routes(app, client, source):
    app.discover_routes(source, prefix="/items")

    r = client.get("/items")
    assert r.status_code == 200
    assert r.text == "OK"

    with client.websocket_connect("/items/echo") as ws:
        ws.send_text("hello")
        assert ws.receive_text() == "hello"
