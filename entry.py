async def app(scope, receive, send):
    """Minimal ASGI app used as a lightweight fallback when dependencies are missing."""
    assert scope["type"] == "http"
    path = scope.get("path", "/")

    if path == "/health":
        body = b'{"status":"healthy","initialized":false}'
        headers = [(b"content-type", b"application/json")]
        await send({"type": "http.response.start", "status": 200, "headers": headers})
        await send({"type": "http.response.body", "body": body})
        return

    # Default response
    body = b'{"message":"Service temporarily limited — backend dependencies not installed."}'
    headers = [(b"content-type", b"application/json")]
    await send({"type": "http.response.start", "status": 200, "headers": headers})
    await send({"type": "http.response.body", "body": body})
