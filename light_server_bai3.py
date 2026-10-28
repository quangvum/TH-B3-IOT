import asyncio
import json
from aiocoap import Context, Message, resource, CONTENT, CHANGED, BAD_REQUEST
from aiocoap.numbers.contentformat import ContentFormat


class LightStatusResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"

    def payload(self):
        return json.dumps(
            {"device_id": "light01", "status": self.status},
            ensure_ascii=False,
        ).encode("utf-8")

    async def render_get(self, request):
        return Message(
            code=CONTENT,
            payload=self.payload(),
            content_format=ContentFormat(50),  # application/json
        )

    async def render_put(self, request):
        print("\nPUT request received:")
        try:
            data = json.loads(request.payload.decode("utf-8"))
            device_id = data.get("device_id")
            command = str(data.get("command", "")).strip().upper()
        except (UnicodeDecodeError, json.JSONDecodeError):
            return Message(code=BAD_REQUEST, payload=b"Payload JSON khong hop le")

        print(f"Device: {device_id}")
        print(f"Command: {command}")
        if device_id != "light01" or command not in ("ON", "OFF"):
            return Message(
                code=BAD_REQUEST,
                payload=b"Yeu cau khong hop le: can device_id=light01 va command ON/OFF",
            )

        old_status = self.status
        self.status = command
        if old_status != self.status:
            print(f"Light state changed: {old_status} -> {self.status}")
            self.updated_state()
            print(f"Notify observers: {self.status}")
        else:
            print(f"Light state unchanged: {self.status}")

        return Message(
            code=CHANGED,
            payload=self.payload(),
            content_format=ContentFormat(50),
        )


async def main():
    site = resource.Site()
    site.add_resource(["iot", "lab", "light01", "status"], LightStatusResource())
    await Context.create_server_context(site)
    print("CoAP Smart Light Server started on UDP port 5683")
    print("Resource: /iot/lab/light01/status")
    print("Initial state: OFF")
    try:
        await asyncio.get_running_loop().create_future()
    finally:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung Smart Light Server.")
