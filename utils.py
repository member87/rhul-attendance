#!/usr/bin/python

import time
import logging
import CONFIG
from discord_webhook import DiscordWebhook, DiscordEmbed
from shutil import which
from selenium import webdriver

FIREFOXPATH = which("firefox")
CHROMEPATH = which("chrome") or which("chromium")

def init_logging():
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers= [
                logging.FileHandler("logs"),
                logging.StreamHandler()
                ])

def init_webdriver():
    """Simple Function to initialize and configure Webdriver"""
    if FIREFOXPATH != None:
        logging.info(FIREFOXPATH)
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.binary = FIREFOXPATH
        options.add_argument("-headless")
        return webdriver.Firefox(options=options, log_path="geckodriver.log")

    elif CHROMEPATH != None:
        logging.info(CHROMEPATH)
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.binary_location = CHROMEPATH
        options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=options, service_args=['--verbose'], service_log_path="chromedriver.log")
    raise Exception("Could not find webdriver path")


def send_notification(lesson):
    webhook = DiscordWebhook(url=CONFIG.webhook)
    embed = DiscordEmbed(title='✅ Lesson attended', color='339441')
    embed.set_timestamp()
    embed.add_embed_field(name="Lesson", value=lesson, inline=False)
    webhook.add_embed(embed)
    webhook.execute()

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
def send_timetable(timetable):
    webhook = DiscordWebhook(url=CONFIG.webhook)
    embed = DiscordEmbed(title='', color='339441')
    for k, v in enumerate(timetable):
        embed.add_embed_field(name=days[k], value=f"{len(v)}", inline=False)
    webhook.add_embed(embed)
    webhook.execute()

def send_error(error):
    webhook = DiscordWebhook(url=CONFIG.webhook)
    embed = DiscordEmbed(title='An error occured', color='ff0000')
    embed.add_embed_field(name='Error', value=error)
    webhook.add_embed(embed)
    webhook.execute()


def driver_time(before, after):
    def decorator(func):
        def inner(*args, **kwargs):
            logging.info(f"{before} '{args[1]}'")
            start = time.perf_counter()
            val = func(*args, **kwargs)
            end = time.perf_counter()
            diff = end - start
            if diff > 0.5:
                logging.warn(f"{after} {diff:.4f} seconds")
            else:
                logging.info(f"{after} {diff:.4f} seconds")
            return val

        return inner
    return decorator


