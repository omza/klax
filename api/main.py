from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import config, logging
from tortoise.contrib.fastapi import register_tortoise



# fastapi routers
from routers import auth, devices, users


# Fast Api
logging.info('----------------------------------------------------------')
logging.info(f'fast api start  ....')
logging.debug(config.DATABASE_URI)

description = """
The KLAX makes the values of modern electricity meters immediately available and thus helps to implement effective energy-saving measures and create transparency. 
For this purpose, the KLAX is attached by magnet to the integrated optical interface of modern measuring devices (mME). The signals from the infrared interface are picked up by the optical head and transmitted via LoRaWAN. 
The determined measured values are available in the LoRaWAN backend shortly after the measurement and can be further processed with suitable software. You can purchase your Klax e.g. via iot-shop.de!

This API offers CRUD Operations for Mobile or Webapps to configure your Klax Device and handle your Energy Data.
"""


app = FastAPI(
    title="MyKlax Api",
    description=description,
    version="0.1.0",
    terms_of_service="https://github.com/omza/klax",
    contact={
        "name": "Oliver Meyer",
        "url": "https://omza.de",
        "email": "oliver@omza.de",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/omza/klax/blob/master/LICENSE",
    },
    docs_url="/",    
    redoc_url=None)


#CORS Support
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Import fastapi Routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(devices.router)



# initialize db 
register_tortoise(
    app, 
    db_url=config.DATABASE_URI,
    modules={'models': ['db.models']},
    generate_schemas=True,
    add_exception_handlers=True
)



