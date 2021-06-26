from selenium.webdriver.support.ui import Select
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    #########
    def open_manage_projects_page(self):
        wd = self.app.wd
        if not self.is_manage_projects_page():
            wd.get(self.app.base_url + "/manage_proj_page.php")

    def is_manage_projects_page(self):
        wd = self.app.wd
        return wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_xpath(
            "//input[@value='Create New Project']")) > 0

    #########
    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_projects_page()
            self.project_cache = []
            for element in wd.find_elements_by_xpath(
                    "//tr[contains(@class,'row')][not(contains(@class,'category'))][./td/a]"):
                cells = element.find_elements_by_tag_name("td")
                name = cells[0].find_element_by_tag_name("a").text
                id = cells[0].find_element_by_tag_name("a").get_attribute("href").split("=", 1)[1]
                self.project_cache.append(Project(name=name, id=id))
        return self.project_cache

    #########
    def fill_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_dpop_down_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)

    def fill_project_form(self, project):
        self.fill_field("name", project.name)
        self.fill_dpop_down_field("status", project.status)
        self.fill_dpop_down_field("view_state", project.status_view)
        self.fill_field("description", project.description)

    #########

    def create(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.open_manage_projects_page()
        self.project_cache = None

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.select_project_by_id(id)
        self.delete_project()
        self.open_manage_projects_page()
        self.project_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath(
            "//tr[contains(@class,'row')][not(contains(@class,'category'))][./td/a]//a[contains(@href,'project_id=%s')]"
            % id).click()

    def delete_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//div[./hr][./br]")
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
