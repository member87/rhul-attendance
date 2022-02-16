#!/usr/bin/python

import CONFIG, json, logging
from selenium_controller import SeleniumController
from selenium.webdriver.common.by import By

class Timetable(SeleniumController):

    timetable = []

    def __init__(self) -> None:
        SeleniumController.__init__(self)
        

    def get_timetable(self) -> None:
        logging.info("opening login page")
        
        self.load_page(CONFIG.url)


        self.wait_for_element('tUserName')
       
        logging.info("entering login details")
        self.send_keys('tUserName', CONFIG.username)
        self.send_keys('tPassword', CONFIG.password)
        self.click_element('bLogin')

        self.wait_for_element('LinkBtn_studentMyTimetable')

        self.click_element('LinkBtn_studentMyTimetable')

        # Wait for page to load
        self.wait_for_element('lbWeeks')

        logging.info("selecting current week")
        self.select_list_by_index('lbWeeks', 3)

        logging.info("loading timetable page")
        self.click_element('bGetTimetable')


        self.wait_for_element('form1')

        table = self.find_element_xpath('/html/body/table[2]/tbody')
        self.save_timetable(table)

    def save_timetable(self, table) -> None:
        logging.info("running save timetable")
        for i, tr in enumerate(table.find_elements(By.XPATH, './*')[1:]):
            offset = 0
            self.timetable.append([])
            for td in tr.find_elements(By.XPATH, './*')[2 if i == 0 else 1:]:
                colspan = td.get_attribute('colspan')
                if colspan:
                    self.timetable[i].append([offset, td.text])
                    offset = offset + (30 * int(colspan))
                else:
                    offset = offset + 30

        with open('current_week.json', 'w') as f:
            logging.info("saving timetable")
            json.dump(self.timetable, f)



if __name__ == "__main__":
    with Timetable() as t:
        t.get_timetable()
