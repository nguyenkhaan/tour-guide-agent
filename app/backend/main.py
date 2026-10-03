import asyncio
import sys
import uvicorn

if __name__ == "__main__":
    # Fix for Windows: psycopg async requires SelectorEventLoop, not ProactorEventLoop
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    uvicorn.run("src.app:app", host="0.0.0.0", port=4000, loop="asyncio")