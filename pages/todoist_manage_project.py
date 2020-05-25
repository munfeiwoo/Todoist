class TodoistManageProject:

    def __init__(self,app):
        self.app = app

    def check_project_exist_by_project_name(self, project_name):
        project_listing = "//android.widget.TextView[@text = '{}']".format(project_name)
        assert (self.app.find_element_by_xpath(project_listing) is not None)
