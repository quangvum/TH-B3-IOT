import asyncio
import json
from datetime import datetime
from aiocoap import Context, Message, GET

URI = "coap://localhost/iot/lab/sensor01/data"


async def main():
    protocol = await Context.create_client_context()
    print(f"Monitoring CoAP Client -> {URI}")
    try:
        while True:
            try:
                response = await protocol.request(
                    Message(code=GET, uri=URI)
                ).response
                data = json.loads(response.payload.decode("utf-8"))
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received sensor data")
                print(f"Device: {data['device_id']}")
                print(f"Temperature: {data['temperature']} C")
                print(f"Humidity: {data['humidity']} %")
                warnings = []
                if float(data["temperature"]) > 35:
                    warnings.append("CANH BAO: Nhiet do cao")
                if float(data["humidity"]) < 40:
                    warnings.append("CANH BAO: Do am thap")
                for warning in warnings:
                    print(warning)
                if not warnings:
                    print("Trang thai: Binh thuong")
            except (asyncio.TimeoutError, OSError, ValueError, KeyError) as exc:
                print(f"Loi khi doc du lieu cam bien: {exc}")
            await asyncio.sleep(3)
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung Monitoring Client.")
