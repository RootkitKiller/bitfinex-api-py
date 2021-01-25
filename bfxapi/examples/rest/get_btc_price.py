import os
import sys
import asyncio
import time
sys.path.append('../../../')

from bfxapi import Client

bfx = Client(
  logLevel='DEBUG',
)
out_path = "/Users/leek/code/python/btc_price/btc_price2.txt"
start_time = 1358179200 * 1000 # 2013/01/15, the first date's btc price
step_time = 86400 * 1000
end_time = 1611331200 * 1000 # 2021/01/23, the end date's btc price

def get_write_last_time():
    if not os.path.exists(out_path):
        return ""
    with open(out_path, "r") as read_file:
        last_line = read_file.readlines()[-1]
        if len(last_line) != 0:
            return last_line.split(" ")[0]
        else:
            return ""

async def get_btc_price():
    progress_time = start_time
    write_last_time = get_write_last_time()
    if write_last_time != "":
        progress_time = int(write_last_time)
    with open(out_path, "a") as out_file:
        while True:
            trades = await bfx.rest.get_public_trades("tBTCUSD", progress_time, progress_time + step_time, 1, sort = 1) 
            if len(trades) != 0:
                time_obj = time.localtime(trades[0][1] / 1000)
                log_datetime = time.strftime("%Y%m%d", time_obj)
                write_log = f"{progress_time} {log_datetime} {trades[0][3]}\n"
                print(write_log)
                out_file.write(write_log)
            progress_time = progress_time + step_time
            if progress_time > end_time:
                break

async def run():
    await get_btc_price()

t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)
