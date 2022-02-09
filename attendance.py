#!/usr/bin/python

import json
import CONFIG
import discord_notify as dn
import time

from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options


class Attendance():

    def __init__(self) -> None:
        
        self.log('running attendance file')

        with open('current_week.json', 'r') as f:
            self.timetable = json.load(f)

        self.current_day = self.timetable[datetime.today().weekday()]


        now = datetime.now()
        day_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        seconds = (now - day_start).seconds / 60

        self.time_passed = seconds
        lesson = self.is_in_class()
        if lesson:
            self.log('Lesson found! Starting to mark attendance')
            self.mark_attendance(lesson)
        else:
            self.log('No lesson has been found!')

    def log(self, message):
        with open('logs', 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    
    def wait_for_element(self, id):
        self.log(f"waiting for element '{id}'")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, id)))


    def mark_attendance(self, lesson):
        try:
            options = Options()
            self.log("creating web driver")
            options.headless = True
            self.driver = webdriver.Firefox(options=options, executable_path='/usr/bin/geckodriver')

            self.log("loding login page")
            self.driver.get('https://lum-prod.ec.royalholloway.ac.uk/')
            self.wait_for_element('userNameInput')

            self.log("entering login details")
            # Login
            self.driver.find_element(By.ID, 'userNameInput').send_keys(CONFIG.username + '@live.rhul.ac.uk')
            self.driver.find_element(By.ID, 'passwordInput').send_keys(CONFIG.password)
            self.driver.find_element(By.ID, 'submitButton').click()

            self.log("pressed login")
            self.log("loading attendance page")
            # Load Attendance page
            self.driver.get('https://generalssb-prod.ec.royalholloway.ac.uk/BannerExtensibility/customPage/page/RHUL_Attendance_Student')

            self.log("loaded attendance page")
            # wait for load
            try:
                time.sleep(10)
                self.log(lesson[1])
                self.driver.find_element(By.ID, 'pbid-buttonFoundHappeningNowButtonsHere').click()
                self.log('pressed "Im here" button')
                dn.monitor_attendance(lesson[1])

            except Exception as e:
                self.log("ERROR **************************************")
                self.log(e)
                self.log("********************************************")
                dn.error('error attending class :' + lesson[1])
        except Exception as e:
            self.log(e)

    
    def is_in_class(self) -> object:
        for lesson in self.current_day:
            start_time = lesson[0]
            if self.time_passed > start_time and self.time_passed < start_time + 60:
                return lesson
            

Attendance()
