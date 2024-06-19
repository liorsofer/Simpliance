import uvicorn
import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import transaction, address
from utils.init_app import init_application

# Allowed origins
origins = ["*"]


class App:
    def __init__(self):
        self.app = FastAPI(title="Simpliance", version="1.0.0")

        # Add CORSMiddleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.include_router(transaction.router)
        self.app.include_router(address.router)

        init_application()


    async def run(self):
        config = uvicorn.Config(
            app=self.app,
            host="127.0.0.1",
            port=5009,
            lifespan="off",
            access_log=False
        )
        server = uvicorn.Server(config=config)
        await server.serve()


if __name__ == "__main__":
    app = App()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())
    loop.close()
