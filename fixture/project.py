from selenium.webdriver.common.by import By
from model.project import ProjectData
import time


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element(By.NAME, field_name).click()
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(text)

    def fill_project_data(self,testdata):
        self.change_field_value("name", testdata.name)
        self.change_field_value("description", testdata.description)
        return testdata

    def open_manage_overview_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_overview_page.php"):
            wd.find_element(By.LINK_TEXT, "Manage").click()

    def open_manage_proj_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_create_page.php"):
            wd.find_element(By.LINK_TEXT, "Manage Projects").click()

    def return_manage_page(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "group page").click()


    def open_manage_proj_create_page(self):
        self.open_manage_overview_page()
        self.open_manage_proj_page()
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_create_page.php") and len(
                wd.find_elements(By.CSS_SELECTOR, "input.button")) > 0):
            wd.find_element(By.CSS_SELECTOR, "input[value='Create New Project']").click()

    def add_project(self):
        wd = self.app.wd
        wd.find_element(By.XPATH, "//input[@value='Add Project']").click()
        self.project_cache = None

    project_cache= None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_overview_page()
            self.open_manage_proj_page()
            self.project_cache = []
            table = wd.find_element(By.CSS_SELECTOR, "[class*='width100'][cellspacing='1']")
            time.sleep(1)
            for row in table.find_elements(By.CSS_SELECTOR, "[class*='row']:not(.row-category)"):
                cells = row.find_elements(By.TAG_NAME, "td")
                id = row.find_element( By.XPATH,".//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]").get_attribute("href").split("=")[1]
                name = cells[0].text
                status = cells[1].text
                enabled = cells[2].text
                view_status = cells[3].text
                description = cells[4].text
                self.project_cache.append(ProjectData(id=id, name=name, status=status, enabled=enabled,view_status=view_status,description=description))
            return list(self.project_cache)

    def select_project_by_id(self,id):
        wd = self.app.wd
        wd.find_element( By.XPATH,".//a[@href='manage_proj_edit_page.php?project_id=%s']" % id).click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.select_project_by_id(id)
        wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        self.project_cache = None