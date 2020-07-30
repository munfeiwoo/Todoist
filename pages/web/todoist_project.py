class TodoistProject:

    PROJECT_TITLE = "//h1/span[text() = '{}']"

    def __init__(self, browser):
        self.browser = browser

    def check_project_title_is_displayed(self, project_name):
        title = self.PROJECT_TITLE.format(project_name)
        results = self.browser.find_element_by_xpath(title)
        assert results is not None
