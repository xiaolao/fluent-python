# coding: utf-8

import asyncio
import datetime
import random


async def display_date(num, loop):
    end_time = loop.time() + 10.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(2)


async def produce(queue, n):
    for x in range(n):
        print('producing {}/{}'.format(x, n))
        await asyncio.sleep(random.random())
        item = str(x)
        await queue.put(item)


async def consume(queue):
    while True:
        item = await queue.get()
        print('consuming {}...'.format(item))
        await asyncio.sleep(random.random())
        queue.task_done()


async def run(n):
    queue = asyncio.Queue()
    consumer = asyncio.ensure_future(consume(queue))
    await produce(queue, n)
    await queue.join()
    consumer.cancel()
