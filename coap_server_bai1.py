import asyncio
from datetime import datetime
from aiocoap import Context, Message, resource, POST, CONTENT, CHANGED, NOT_FOUND

WELCOME = "Xin chao tu CoAP Server"
latest_message = None


class MessageResource(resource.Resource):
    async def render_get(self, request):
        print("GET request received: /iot/lab/message")
        payload = latest_message or WELCOME
        return Message(code=CONTENT, payload=payload.encode("utf-8"))

    async def render_post(self, request):
        global latest_message
        latest_message = request.payload.decode("utf-8", errors="replace")
        print("\nPOST request received:")
        print(f"Payload: {latest_message}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        return Message(code=CHANGED, payload="Server da nhan thong diep".encode("utf-8"))


async def main():
    site = resource.Site()
    site.add_resource(["iot", "lab", "message"], MessageResource())
    await Context.create_server_context(site)
    print("CoAP Server started on UDP port 5683")
    print("Resource: coap://localhost/iot/lab/message")
    print("Nhan Ctrl+C de dung server.")
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung CoAP Server.")
