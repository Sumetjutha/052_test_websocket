import asyncio
import websockets
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

chrome_driver_path = 'chromedriver.exe'  

# กำหนด URL ของ WebSocket server
url = "ws://localhost:8080//goldprice"

# เปิดการเชื่อมต่อ WebSocket
async def handle_connection(websocket, path):
    print('WebSocket connected')

    try:
        # เริ่มการ Scraping ข้อมูลจากหน้าเว็บ
        driver = webdriver.Chrome(chrome_driver_path)
        driver.get('https://www.investing.com/currencies/xau-usd')

        while True:
            bid_goldspot = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/main/div/div[1]/div[2]/ul/li[2]/div[2]/span[1]').text
            bid_goldspot = bid_goldspot.replace(",", "")
            bid_goldspot = float(bid_goldspot)

            offer_goldspot = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/main/div/div[1]/div[2]/ul/li[2]/div[2]/span[3]').text
            offer_goldspot = offer_goldspot.replace(",", "")
            offer_goldspot = float(offer_goldspot)

            # สร้าง JSON ที่มีข้อมูลเวลาและข้อมูล bid_goldspot และ offer_goldspot
            data = {
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),  # แปลงเวลาให้อยู่ในรูปแบบที่กำหนด
                "bid_goldspot": bid_goldspot,
                "offer_goldspot": offer_goldspot
            }
            response = json.dumps(data)  # แปลงเป็น JSON ก่อนส่ง

            # ส่งข้อมูลที่ Scraping มาให้กับเบราว์เซอร์ผ่าน WebSocket
            await websocket.send(response)

            await asyncio.sleep(0.5)  # รอรับข้อมูลใหม่ทุก 0.5 วินาที
    except websockets.exceptions.ConnectionClosedOK:
        print('WebSocket closed')
    finally:
        driver.quit()

# สร้าง WebSocket server ที่รอรับเชื่อมต่อที่พอร์ต 8080
start_server = websockets.serve(handle_connection, 'localhost', 8080)

print('WebSocket server is running on port 8080')

# ให้ลูปรอรับการเชื่อมต่อเข้ามา
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
