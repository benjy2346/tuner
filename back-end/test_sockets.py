import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:5000/audio-stream"  # The WebSocket URL of your Flask back-end
    try:
        async with websockets.connect(uri) as websocket:
            # Send a test message
            await websocket.send("Hello from WebSocket client")

            # Wait to receive a message from the server
            response = await websocket.recv()
            print(f"Message from server: {response}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"Failed to connect to WebSocket server: {e}")

# Run the WebSocket test
asyncio.get_event_loop().run_until_complete(test_websocket())
