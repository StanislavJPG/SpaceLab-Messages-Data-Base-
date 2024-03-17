import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.controllers import get_and_save_data
from src.router import router

app = FastAPI(title="Project for SpaceLab")

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    if os.path.exists('database.db'):
        ...
    else:
        await get_and_save_data()
        print('Database has been successfully created')


register_tortoise(
    app,
    db_url="sqlite://database.db",
    generate_schemas=True,
    add_exception_handlers=True,
    modules={'modules': ['src.models']}
)
