from fastapi import FastAPI
from config.config import initialize_settings
from gateway.routes.routers import router
from database.model.setup import create_tables

app = FastAPI()


def main():
    # If there are config variables to be setup, call the setup function here
    initialize_settings()

    # create database tables with sqla
    create_tables()
    # include routes
    app.include_router(router=router)


if __name__ == "__main__":
    main()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
