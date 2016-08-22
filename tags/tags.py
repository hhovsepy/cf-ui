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
        self.nav = NavigationTree(self.web_session)

    def waiting(self, xpath, seconds):
        return WebDriverWait(self.web_driver, seconds).until( EC.element_to_be_clickable((By.XPATH, xpath)) )


    def _power_click(self, clickable):
        driver = self.web_driver
        hover = ActionChains(driver)
        sleep(1)
        if clickable:
            hover.move_to_element(clickable).perform()
            clickable.click()

    def set_tag(self, tag_name, tag_value):
        driver = self.web_driver
        print "Current URL: ", driver.current_url
        #nav = NavigationTree(self.web_session)

        # to check if tag is already set
        if tag_value in self.tag_list_ui()[tag_name]:
            print "Already added (set_tag: ", tag_name, "::", tag_value, ")"
            return self

        self.waiting("//button[@data-toggle='dropdown'][@data-id='tag_cat']", 3)
        click1 = driver.find_element_by_xpath("//button[@data-toggle='dropdown'][@data-id='tag_cat']")
        sleep(1)
        self.nav.power_click(click1)

        all_options = driver.find_elements_by_xpath("//select[@id='tag_cat']/../div[contains(@class, 'btn-group')]/div/ul/li/a")
        for option in all_options:
            if tag_name in option.text:
                print "Tag_name is substring of : ", option.text
                sleep(1)
                self.nav.go_up_till_clickable(option)
        #sleep(3)

        next_xpath = "//button[@data-toggle='dropdown'][@data-id='tag_add']"
        self.waiting(next_xpath, 5)
        click2 = driver.find_element_by_xpath(next_xpath)

        self.nav.power_click(click2)
        sleep(3)

        all_options = driver.find_elements_by_xpath("//select[@id='tag_add']/../div[contains(@class, 'btn-group')]/div/ul/li/a")
        sleep(3)
        for option in all_options:
            if tag_value in option.text:
                print "Tag_value is substring of : ", option.text
                sleep(1)
                self.nav.go_up_till_clickable(option)
        sleep(3)
        #ui_utils(self.web_session).waitForTextOnPage(tag_value, 5)

        xpath_save = "//div[@id='buttons_on']/button[@title='Save Changes']"
        save_button = driver.find_element_by_xpath(xpath_save)
        sleep(3)
        self.nav.power_click(save_button)
        sleep(3)
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

        self.nav.power_click(magic_button)
        sleep(2)
        xpath_save = "//div[@id='buttons_on']/button[@title='Save Changes']"
        save_button = driver.find_element_by_xpath(xpath_save)
        self.nav.power_click(save_button)
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
