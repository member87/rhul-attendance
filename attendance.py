#!/usr/bin/python

import json
import CONFIG
import discord_notify as dn

from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options


class Attendance():

    def __init__(self) -> None:
        with open('current_week.json', 'r') as f:
            self.timetable = json.load(f)

        self.current_day = self.timetable[datetime.today().weekday()+1]


        now = datetime.now()
        day_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        seconds = (now - day_start).seconds / 60

        self.time_passed = seconds
        lesson = self.is_in_class()
        if lesson:
            self.mark_attendance(lesson)

    
    def wait_for_element(self, id):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, id)))


    def mark_attendance(self, lesson):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get('https://lum-prod.ec.royalholloway.ac.uk/')
        self.wait_for_element('userNameInput')

        # Login
        self.driver.find_element(By.ID, 'userNameInput').send_keys(CONFIG.username + '@live.rhul.ac.uk')
        self.driver.find_element(By.ID, 'passwordInput').send_keys(CONFIG.password)
        self.driver.find_element(By.ID, 'submitButton').click()

        # Load Attendance page
        self.driver.get('https://generalssb-prod.ec.royalholloway.ac.uk/BannerExtensibility/customPage/page/RHUL_Attendance_Student')

        # wait for load
        self.wait_for_element('content')

        dn.monitor_attendance(lesson[1])

    
    def is_in_class(self) -> object:
        for lesson in self.current_day:
            start_time = lesson[0]
            if self.time_passed > start_time and self.time_passed < start_time + 60:
                return lesson
            

Attendance()
