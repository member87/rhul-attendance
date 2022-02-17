#!/usr/bin/python

import json, CONFIG, time, logging, utils
from selenium_controller import SeleniumController
from datetime import datetime
from selenium.webdriver.common.by import By


class Attendance(SeleniumController):

    def __init__(self) -> None:
        SeleniumController.__init__(self)
        logging.info('running attendance file')

        with open('current_week.json', 'r') as f:
            self.timetable = json.load(f)

    def start(self) -> None:
        lesson = self.is_in_class()
        if lesson:
            logging.info('Lesson found! Starting to mark attendance')
            self.mark_attendance(lesson)
        else:
            logging.info('No lesson has been found!')

    def time_since_8(self) -> float:
        now = datetime.now()
        day_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        seconds = (now - day_start).seconds / 60
        return seconds


    def mark_attendance(self, lesson) -> None:
        logging.info("creating web driver")

        logging.info("loding login page")
        self.load_page('https://lum-prod.ec.royalholloway.ac.uk/')
        self.wait_for_element('userNameInput')

        logging.info("entering login details")
        self.send_keys('userNameInput', CONFIG.username + '@live.rhul.ac.uk')
        self.send_keys('passwordInput', CONFIG.password)
        self.click_element('submitButton')

        self.load_page('https://generalssb-prod.ec.royalholloway.ac.uk/BannerExtensibility/customPage/page/RHUL_Attendance_Student')

        logging.info("loaded attendance page")
        time.sleep(60)
        logging.info(lesson[1])

        if "online" in lesson[1].lower():
            self.driver.find_element(By.XPATH, '//*[@id="pbid-buttonFoundHappeningNowButtonsHere"]').click()
            logging.info('signed in (Im Here)')

        else:
            self.driver.find_element(By.XPATH, '//*[@id="pbid-buttonFoundHappeningNowButtonsTwoInPerson"]').click()
            logging.info('signed in (In Person)')

        utils.send_notification(lesson[1])



    
    def is_in_class(self) -> object:
        current_day = self.timetable[datetime.today().weekday()]
        for lesson in current_day:
            start_time = lesson[0]
            time_diff = self.time_since_8()
            if time_diff > start_time and time_diff < start_time + 60:
                return lesson
            
if __name__ == "__main__":
    with Attendance() as a:
        a.start()
