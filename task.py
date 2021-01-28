# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import asyncio
import time
import sys
from fastapi.encoders import jsonable_encoder

from db import SessionLocal
from deps import get_db
from databases import Database

from models import Process
from settings import settings
db = SessionLocal()


async def sleep(val):
    await asyncio.sleep(val)


def logger(func):
    def wrapper(instance, db):
        start = time.time()
        result = func(instance, db)
        end = time.time()
        print(f'{func.__name__} is completed in time: {end - start:.2f} sec for id {instance.id}\n')
        return result
    return wrapper


@logger
async def add(instance, db):
    await sleep(4)
    vals = list(map(int, instance.func_params.split(",")))
    instance.output = str(sum(vals))
    instance.status = 'completed'
    db.commit()


@logger
async def diff(instance, db):
    await sleep(4)
    vals = list(map(int, instance.func_params.split(",")))
    instance.output = str(abs(vals[1]-vals[0]))
    instance.status = 'completed'
    db.commit()


@logger
async def multiply(instance, db):
    await sleep(4)
    vals = list(map(int, instance.func_params.split(",")))
    val = 1
    for key in vals:
        val *= key
    instance.output = str(val)
    instance.status = 'completed'
    db.commit()


def main(db):
    result_qs = Process.get_queryset(db=db).filter((Process.status == 'queued') | (Process.status == 'in_progress'))
    result_with_order_by = result_qs.order_by(Process.priority)
    result = list(result_with_order_by)
    print(f"Total {len(result)} Tasks Received.\n")
    start = time.time()

    if result:
        result_qs.update({"status": "in_progress"})
        db.commit()
        tasks = []
        loop = asyncio.get_event_loop()
        for instance in result:
            if instance.func_name == 'sum':
                tasks.append(loop.create_task(add(instance, db)))
            elif instance.func_name == 'diff':
                tasks.append(loop.create_task(diff(instance, db)))
            elif instance.func_name == 'multiply':
                tasks.append(loop.create_task(multiply(instance, db)))
            else:
                instance.output = "Func not found"
                instance.status = "failed"

        if tasks:
            loop.run_until_complete(asyncio.wait(tasks))
            # loop.close()

        db.commit()
    end = time.time()
    print(f'Completed Time: {end - start:.2f} sec\n\n')


if __name__ == '__main__':
    if sys.argv and sys.argv[1] == 'start-queue':
        while True:
            main(db)
            time.sleep(5)
