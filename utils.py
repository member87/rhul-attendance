import time
import logging
from discord_webhook import DiscordWebhook, DiscordEmbed
from shutil import which
from selenium import webdriver

FIREFOXPATH = which("firefox")
CHROMEPATH = which("chrome") or which("chromium")

def init_logging():
    logging.basicConfig(
            encoding='utf-8', 
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers= [
                logging.FileHandler("logs"),
                logging.StreamHandler()
                ])

def init_webdriver():
    """Simple Function to initialize and configure Webdriver"""
    if FIREFOXPATH != None:
        logging.info(FIREFOXPATH)#cm
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.binary = FIREFOXPATH
        options.add_argument("-headless")
        return webdriver.Firefox(options=options, log_path="geckodriver.log")

    elif CHROMEPATH != None:
        logging.info(CHROMEPATH)#cm
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.binary_location = CHROMEPATH
        options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=options, service_args=['--verbose'], service_log_path="chromedriver.log")


def send_notification(lesson):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/940240657413468230/eLhWgAvnVu0mOdwmp79XFumlChQT8HrrADQtU8InnXR9WveXtvulKdtyYm-MUCnrI8GJ')
    embed = DiscordEmbed(title='✅ Lesson attended', color='339441')
    embed.set_timestamp()
    embed.add_embed_field(name="Lesson", value=lesson, inline=False)


    webhook.add_embed(embed)

    webhook.execute()

def send_error(error):

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/940240657413468230/eLhWgAvnVu0mOdwmp79XFumlChQT8HrrADQtU8InnXR9WveXtvulKdtyYm-MUCnrI8GJ')
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


