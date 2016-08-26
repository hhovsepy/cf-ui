from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from navigation.navigation import NavigationTree

from time import sleep


class tags():

    web_driver = None
    web_session = None
    nav = None

    def __init__(self, _web_session):
        self.web_session = _web_session
        self.web_driver = _web_session.web_driver
        #self.nav = NavigationTree(self.web_session)


    def waiting_ability(self, xpath, seconds):
        try:
            WebDriverWait(self.web_driver, seconds).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except:
            self.web_session.logger.info(" Given object is not clickable. (waiting_clickability)")
            self.waiting_ability(xpath, seconds-1 )


    def tag_click(self, xpath, seconds):

        click = self.web_driver.find_element_by_xpath(xpath)
        self.waiting_ability(xpath, seconds)
        #click.click()
        try:
            click.click()
            #self.nav.go_up_till_clickable(click)
        except:
            self.web_session.logger.info(" Caught exception. (tag_click)")
            self.tag_click(xpath, seconds-1)


    def click_option(self, option_name, xpath):
        for option in self.web_driver.find_elements_by_xpath( xpath ):
            if option_name in option.text:
                print "Click on option : ", option.text
                self.nav.go_up_till_clickable(option)


    def click_tag_save(self):
        xpath_save = "//button[contains(@title,'Save Changes')]"
        xpath_save_2 = ".//*[@id='buttons_off']/button[1]"
        #sleep(3)

        self.waiting_ability(xpath_save, 7)
        #self.waiting_clickability(xpath_save_2, 7)
        click1 = self.web_driver.find_element_by_xpath(xpath_save)
        click2 = self.web_driver.find_element_by_xpath(xpath_save_2)

        try:
            #sleep(3)
            self.waiting_ability(xpath_save, 7)
            #click1.click()
            #click2.click()
            self.nav.go_up_till_clickable(click1)
            #self.nav.go_up_till_clickable(click2)
        except:
            self.web_session.logger.info(" Caught Exception. ")
            #self.click_tag_save()


    def set_tag(self, tag_name, tag_value, navigation=False):
        if navigation:
            NavigationTree(self.web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags').hold_on(5)

        if tag_value in self.tag_list_ui()[tag_name]:
            print "Already added (set_tag: ", tag_name, "::", tag_value, ")"
            return self

        column_xpath = "//button[@data-toggle='dropdown'][@data-id='{}']"
        option_xpath = "//select[@id='{}']/../div[contains(@class, 'btn-group')]/div/ul/li/a"
        xpath_save = "//button[contains(@title,'Save Changes')]"
        xpath_save_shadow = ".//*[@id='buttons_off']/button[1]"

        self.tag_click(column_xpath.format("tag_cat"), 7)
        self.click_option(tag_name, option_xpath.format("tag_cat"))

        self.tag_click(column_xpath.format('tag_add'), 7)
        self.click_option(tag_value, option_xpath.format("tag_add"))

        #self.click_tag_save()
        self.web_session.logger.info(" Press Save button")
        self.tag_click(xpath_save_shadow, 7)


        return self


    def count_tags_on_page(self):
        return len( self.web_driver.find_elements_by_xpath('.//table/tbody/tr[contains(@id, "_tr")]') )


    def tag_list_ui(self):
        from collections import defaultdict
        xpath = './/table/tbody/tr[contains(@id, "_tr")]/td[not(contains(@title,"Click"))]'
        driver = self.web_driver
        tag_dict = defaultdict(list)
        tags = [ tag.text for tag in driver.find_elements_by_xpath(xpath) ]

        for zz in zip(*[iter(tags)] * 2):
            print zz[0], " -> ", zz[1]
            key = zz[0].encode('ascii', 'ignore')
            val = zz[1].encode('ascii', 'ignore')
            tag_dict[key].append( val )
        return tag_dict

    def _set_tags(self, tags):
        for category in tags.keys():
            for value in tags[category]:
                self.set_tag(category, value)

    def drop_tag(self, tag_name, tag_value):
        driver = self.web_driver

        if self.count_tags_on_page() == 0 or tag_value not in self.tag_list_ui()[tag_name]:
            print "Nothing to delete."
            return self

        magic_xpath = "//td[contains(., '{}')]/../td[contains(., '{}')]/../td[contains(@title, 'to remove this assignment')]".format(tag_name, tag_value)
        magic_button = None
        try:
            magic_button = driver.find_element_by_xpath(magic_xpath)
        except:
            raise ValueError("These tag name or tag value not present on page: {} | {}".format(tag_name, tag_value))

        magic_button.click()
        sleep(2)
        xpath_save = "//div[@id='buttons_on']/button[@title='Save Changes']"
        save_button = driver.find_element_by_xpath(xpath_save)

        save_button.click()
        return self


    def drop_all_tags(self):
        driver = self.web_driver
        self.web_session.logger.info("drop all these tags")

        if self.count_tags_on_page() == 0:
            print "Nothing to delete."
            return self

        magic_xpath = "//td[@title='Click to remove this assignment']"
        tag_list = driver.find_elements_by_xpath(magic_xpath)
        if tag_list == []:
            print "== Nothing to remove. Put some tags before! =="
            return self
        # else
        for _ in tag_list:
            sleep(3)
            x_button = driver.find_element_by_xpath(magic_xpath)
            sleep(1)
            x_button.click()
        sleep(3)
        xpath_save = "//button[@title='Save Changes']"
        save_button = driver.find_element_by_xpath(xpath_save)
        sleep(2)
        save_button.click()
        sleep(3)

        return self
