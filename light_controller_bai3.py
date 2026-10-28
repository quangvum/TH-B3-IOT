import asyncio
import json
from aiocoap import Context, Message, GET, PUT

URI = "coap://localhost/iot/lab/light01/status"


async def main():
    protocol = await Context.create_client_context()
    print("=== LIGHT CONTROLLER ===")
    print("Nhap ON de bat den, OFF de tat den, STATUS de xem trang thai, EXIT de thoat.")
    try:
        while True:
            try:
                command = (await asyncio.to_thread(
                    input, "\nNhap lenh (ON/OFF/STATUS/EXIT): "
                )).strip().upper()
            except EOFError:
                break

            if command == "EXIT":
                print("Thoat chuong trinh controller.")
                break
            if command in ("ON", "OFF"):
                payload = json.dumps(
                    {"device_id": "light01", "command": command}
                ).encode("utf-8")
                print("Sending PUT request...")
                try:
                    response = await protocol.request(
                        Message(code=PUT, uri=URI, payload=payload)
                    ).response
                    print(f"Response Code: {response.code}")
                    print(f"Response: {response.payload.decode('utf-8', errors='replace')}")
                    if str(response.code).startswith("2."):
                        print("Da bat den light01" if command == "ON" else "Da tat den light01")
                except (asyncio.TimeoutError, OSError) as exc:
                    print(f"Khong the lien lac voi Server: {exc}")
            elif command == "STATUS":
                print("Sending GET request...")
                try:
                    response = await protocol.request(
                        Message(code=GET, uri=URI)
                    ).response
                    print("Response:")
                    print(response.payload.decode("utf-8", errors="replace"))
                except (asyncio.TimeoutError, OSError) as exc:
                    print(f"Khong the lay trang thai: {exc}")
            else:
                print("Lenh khong hop le. Chi nhap ON, OFF, STATUS hoac EXIT.")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
