import time

from fastapi.encoders import jsonable_encoder

import asyncio
import time


def form_output_data(data, error=None):
    data = jsonable_encoder(data)
    return {
        "status": True,
        "message": "success" if not error else "fail",
        "error": error,
        "data": data
    }


async def test():
    for i in range(10):
        print(i)
        time.sleep(1)


