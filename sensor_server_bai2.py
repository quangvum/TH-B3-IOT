import asyncio
import json
import random
from aiocoap import Context, Message, resource, CONTENT
from aiocoap.numbers.contentformat import ContentFormat

SENSOR_URI = "/iot/lab/sensor01/data"


class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.data = self.generate_data()
        self.task = None

    @staticmethod
    def generate_data():
        return {
            "device_id": "sensor01",
            "temperature": round(random.uniform(20.0, 40.0), 1),
            "humidity": round(random.uniform(30.0, 80.0), 1),
        }

    async def update_loop(self):
        while True:
            await asyncio.sleep(3)
            self.data = self.generate_data()
            print("Sensor updated:", json.dumps(self.data, ensure_ascii=False))

    async def render_get(self, request):
        payload = json.dumps(self.data, ensure_ascii=False).encode("utf-8")
        return Message(
            code=CONTENT,
            payload=payload,
            content_format=ContentFormat(50),  # application/json
        )


async def main():
    site = resource.Site()
    sensor = SensorResource()
    site.add_resource(["iot", "lab", "sensor01", "data"], sensor)
    await Context.create_server_context(site)
    sensor.task = asyncio.create_task(sensor.update_loop())
    print("CoAP Sensor Server started on UDP port 5683")
    print(f"Resource: coap://localhost{SENSOR_URI}")
    print("Cap nhat du lieu moi moi 3 giay. Nhan Ctrl+C de dung.")
    try:
        await asyncio.get_running_loop().create_future()
    finally:
        sensor.task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung Sensor Server.")
