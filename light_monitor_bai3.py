import asyncio
import json
from datetime import datetime
from aiocoap import Context, Message, GET

URI = "coap://localhost/iot/lab/light01/status"


async def main():
    protocol = await Context.create_client_context()
    print("Registering CoAP Observe...")
    request = Message(code=GET, uri=URI)
    request.opt.observe = 0
    observation = protocol.request(request)
    try:
        first = True
        async for response in observation.observation:
            try:
                data = json.loads(response.payload.decode("utf-8"))
                now = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{now}] {'Initial State' if first else 'State Updated'}")
                print(f"Device: {data.get('device_id', 'unknown')}")
                print(f"Status: {data.get('status', 'unknown')}")
                if first:
                    print("Observe registration active; waiting for changes...")
                    first = False
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                print(f"Payload khong hop le: {exc}")
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung Monitoring Client.")
