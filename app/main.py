# Copyright 2022 Nils Zottmann
# Licensed under the EUPL-1.2-or-later

from postcardscanner import PostcardScanner
from scanner.scanner_v3 import ScannerV3

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import base64
import os


def callback(image):
    print('Received image')
    with open('img.jpg', 'wb') as out:
        out.write(image.read())


scanner = PostcardScanner(scanner=ScannerV3(callback=callback))
scanner.start()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return 'Use routes /last_postcard or /last_postcard_timestamp'


@app.get("/last_postcard")
async def root():
    with open('img.jpg', 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image


@app.get("/last_postcard_timestamp")
async def root():
    return os.path.getctime('img.jpg')


@app.get("/reject_postcard")
async def root():
    scanner.scanner.rejectPostcard()
    return True


@app.get("/accept_postcard")
async def root():
    scanner.scanner.acceptPostcard()
    return True
