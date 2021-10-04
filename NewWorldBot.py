from PIL import Image, ImageGrab
import configparser
import threading
import math, operator
import time
import asyncio
import os
import cv2
#import imutiimls 

from skimage.metrics import structural_similarity as compare_ssim

import discord
()
config = configparser.ConfigParser()
config.read('config.ini')

interval = float(config['GENERAL']['interval'])
TOKEN = config['DISCORD']['token']
USERID = config['DISCORD']['destination']

filepath = 'newworld.png'
filepath_new = 'newworld-new.png'

# Démarrage du client discord
client = discord.Client()

@client.event
async def on_ready():
    print("Connecté à discord")

def get_snapshot():
    screenshot = ImageGrab.grab(bbox =(859, 476, 1690, 959))
    screenshot.save(filepath_new, 'PNG')
    imageA = cv2.imread(filepath)
    imageB = cv2.imread(filepath_new)
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print(score)
    os.replace(filepath_new,filepath)
    print("SSIM: {}".format(score))
    return score

async def queue_watch():
    await asyncio.sleep(10)
    while True:
        user=await client.fetch_user(USERID)
        score = get_snapshot()
        picture = discord.File(filepath)
        print(user)
        if (user != None and score <= 0.992 and score >= 0.85):
            await user.send(file=picture)
        if (user != None and score < 0.85):
            await user.send("Vous avez terminé la file d'attente, le jeu vous attends !")
        # do something
        picture.close()
        await asyncio.sleep(interval)

client.loop.create_task(queue_watch())
client.run(TOKEN)


        
