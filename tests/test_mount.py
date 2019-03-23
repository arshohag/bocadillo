from bocadillo import App


def test_mount_unmount(app: App, client):
    other = App("other")

    @other.route("/foo")
    async def foo(req, res):
        res.text = "OK"

    app.mount("/other", other)

    r = client.get("/other/foo")
    assert r.status_code == 200
    assert r.text == "OK"

    app.unmount("/other")
    r = client.get("/other/foo")
    assert r.status_code == 404


def test_unmount_no_app(app):
    app.unmount("/foo")  # OK
