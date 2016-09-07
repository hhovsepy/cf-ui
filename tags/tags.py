from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navigation.navigation import NavigationTree


class tags():

    web_driver = None
    web_session = None
    nav = None

    def __init__(self, _web_session):
        self.web_session = _web_session
        self.web_driver = _web_session.web_driver
        self.nav = NavigationTree(self.web_session)


    def button_click(self, xpath, seconds):
        driver = self.web_driver
        self.web_session.logger.info(" Exact XPath: {}".format(xpath))
        wait = WebDriverWait(self.web_driver, seconds)

        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        click = driver.find_element_by_xpath(xpath)
        wait.until(EC.visibility_of(click))
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        click.click()


    def click_option(self, option_name, xpath):
        wait = WebDriverWait(self.web_driver, 5)
        print "OPTION NAME: ", option_name

        for option in self.web_driver.find_elements_by_xpath( xpath ):
            print "OPTION - ", option.text
            option_text = "{}".format(option.text)
            if option_name in option.text:
                print "Click on -> ", option_text
                print " '{}' <in> '{}'  (type = {}) (type = {})".format(option_name, option_text, type(option_text), type(option_name))
                #print " option '{}' (type = {})".format(option_name, type(option_name))
                #wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                option.click()
                break


    def get_tag_value_group(self):
        xpath =  ".//*[@id='cat_tags_div']/div/div"
        inner_html = self.web_session.web_driver.find_element_by_xpath(xpath).get_attribute('innerHTML')
        return inner_html


    def values_group_is_updated(self,state_before):
        xpath = '//*[@id="cat_tags_div"]/select[@id="tag_add"]'
        state_now = self.get_tag_value_group()
        return (state_now != state_before) and EC.element_to_be_clickable((By.XPATH, xpath))


    def set_tag(self, tag_name, tag_value):
        driver = self.web_session.web_driver
        logger = self.web_session.logger
        wait = WebDriverWait(self.web_driver, 5)

        existent_tags = self.ui_tags()
        print "Exactly tags: ", existent_tags
        if tag_value in existent_tags[tag_name]:
            print "Already added (set_tag: ", tag_name, "::", tag_value, ")"
            return self

        column_xpath = "//button[@data-toggle='dropdown'][@data-id='{}']"
        xpath_save = "//button[contains(@title,'Save Changes')]"
        print "Tag value: '{}', type: {} ".format(tag_value, type(tag_value))

        original_tag_values = self.get_tag_value_group()
        print "original_tag_values: ", original_tag_values

        tag_button = column_xpath.format("tag_cat")
        self.button_click(tag_button, 7)

        option_button = ".//*[@id='tab_div']/table/thead/tr/th[2]/div/div/ul/li/a/span[@class='text']"
        self.click_option(tag_name, option_button)

        wait.until(
            lambda lamb:
            self.values_group_is_updated(original_tag_values)
        )

        value_button = column_xpath.format("tag_add")
        self.button_click(value_button, 7)

        value_button = ".//*[@id='cat_tags_div']/div/div/ul/li"
        tag_value = "{}".format(tag_value)
        self.click_option(tag_value, value_button)

        save_click = driver.find_element_by_xpath(xpath_save)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_save)))
        save_click.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, flash_caption)))

        if not driver.find_element_by_xpath("//strong[contains(.,'Tag edits were successfully saved')]"):
            raise ValueError("Flasher not found!")

        return self


    def count_tags_on_page(self):
        driver = self.web_driver
        # first_xpath = "(//td[@title='Click to remove this assignment'])[1]"
        #
        wait = WebDriverWait(self.web_driver, 5)
        xpath = './/table/tbody/tr[contains(@id, "_tr")]'

        xpath_0 = ".//*[@id='assignments_div']/table/tbody/tr/td[2]"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_0)))
        determinator = driver.find_element_by_xpath(xpath_0).get_attribute('innerHTML')
        #print "determinator = ", determinator

        if 'No My Company Tags are assigned' in determinator:
            #print "   -->  Number of tags (count_tags_on_page) == 0 "
            return 0


        #WebDriverWait(self.web_driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        num_tags = len( driver.find_elements_by_xpath(xpath) )
        #print "Number of tags (count_tags_on_page): ", num_tags
        return num_tags

    def ui_tags(self):
        wait = WebDriverWait(self.web_driver, 5)
        xpath = "//table/tbody/tr[contains(@id,'_tr')]/td[not(contains(@title,'Click'))]"
        #xpath = "//table/tbody/tr[contains(@id,'_tr')]/td/button/i"
        driver = self.web_driver

        xpath_0 = ".//*[@id='assignments_div']/table/tbody/tr"

        WebDriverWait(self.web_driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_0)))
        WebDriverWait(self.web_driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_0)))

        stick = driver.find_element_by_xpath(xpath_0)

        #WebDriverWait(self.web_driver, 5).until(EC.staleness_of(stick))

        collected_tags = driver.find_elements_by_xpath(xpath)
        tags = [ tag.text for tag in collected_tags ]

        from collections import defaultdict
        tag_dict = defaultdict(list)

        for zz in zip(*[iter(tags)] * 2):
            #print zz[0], " -> ", zz[1]
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
        print "Current page: ", driver.current_url

        if self.count_tags_on_page() == 0 or tag_value not in self.ui_tags()[tag_name]:
            print "Nothing to delete."
            return self

        magic_xpath = "//td[contains(., '{}')]/../td[contains(., '{}')]/../td[contains(@title, 'to remove this assignment')]".format(tag_name, tag_value)
        magic_button = None
        try:
            magic_button = driver.find_element_by_xpath(magic_xpath)
        except:
            raise ValueError("These tag name or tag value not present on page: {} | {}".format(tag_name, tag_value))

        magic_button.click()

        xpath_save = "//div[@id='buttons_on']/button[@title='Save Changes']"
        WebDriverWait(self.web_driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath_save))
            )
        save_button = driver.find_element_by_xpath(xpath_save)
        save_button.click()
        return self

    def drop_first_tag(self):
        driver = self.web_driver
        self.web_session.logger.info(" --| drop first tag")
        magic_xpath = "(//td[@title='Click to remove this assignment'])[1]"

        """
        if self.count_tags_on_page() == 0:
            print "Nothing to delete."
            return self
        """

        WebDriverWait(self.web_driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, magic_xpath))
        )
        tag_list = driver.find_elements_by_xpath(magic_xpath)

        #for x in tag_list:
        x_button = driver.find_element_by_xpath(magic_xpath)
        WebDriverWait(self.web_driver, 7).until(EC.element_to_be_clickable((By.XPATH, magic_xpath)))
        x_button.click()

        xpath_save = "//button[contains(@title,'Save Changes')]"
        save_button = driver.find_element_by_xpath(xpath_save)
        WebDriverWait(self.web_driver, 7).until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        WebDriverWait(self.web_driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, flash_caption))
        )

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert (text_found != None), "Not Found."
        return self


    def drop_all_tags(self):
        driver = self.web_driver
        wait = WebDriverWait(self.web_driver, 15)
        self.web_session.logger.info("drop all these tags")

        first_xpath = "(//td[@title='Click to remove this assignment'])[1]"
        xpath_save = "//button[contains(@title,'Save Changes')]"
        #wait.until(EC.visibility_of_element_located((By.XPATH, first_xpath)))

        num_tags = self.count_tags_on_page()
        print "Number of tags: ", num_tags
        if num_tags == 0:
            print "Nothing to delete."
            return self

        for i in range(0, num_tags):
            #print "(tag = {})".format(i)
            x_button = driver.find_element_by_xpath(first_xpath)
            wait.until(EC.element_to_be_clickable((By.XPATH, first_xpath)))
            x_button.click()
            wait.until(EC.staleness_of(driver.find_element_by_xpath(first_xpath)))
            #continue

        save_button = driver.find_element_by_xpath(xpath_save)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_save)))
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_save)))
        save_button.click()

        flash_caption = "id('flash_text_div')/div/strong[contains(.,'Tag edits were successfully saved')]"
        WebDriverWait(self.web_driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, flash_caption)))

        import re
        src = self.web_driver.page_source
        text_to_search = r'Tag edits were successfully saved'
        text_found = re.search(text_to_search, src)
        assert(text_found != None), "Not Found."

        return self

