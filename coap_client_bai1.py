import asyncio
from aiocoap import Context, Message, GET, POST

# Sua hai gia tri nay truoc khi nop bai.
STUDENT_ID = "DIEN_MA_SINH_VIEN"
STUDENT_NAME = "DIEN_HO_TEN"

URI = "coap://localhost/iot/lab/message"


async def main():
    protocol = await Context.create_client_context()
    try:
        print("CoAP Client")
        print("\nSending GET request...")
        print(f"URI: {URI}")
        response = await protocol.request(Message(code=GET, uri=URI)).response
        print("\nResponse:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")

        payload = (
            f"Xin chao tu CoAP Client - {STUDENT_ID} - {STUDENT_NAME}"
        ).encode("utf-8")
        print("\nSending POST request...")
        print(f"Payload: {payload.decode('utf-8')}")
        response = await protocol.request(
            Message(code=POST, uri=URI, payload=payload)
        ).response
        print("\nResponse:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
