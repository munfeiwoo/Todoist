class TodoistProject:

    ADD_TASK_BTN = 'com.todoist:id/fab'
    PROJECT_TASK_TITLE = 'android:id/message'
    PROJECT_TASK_DATE_OPTION = 'com.todoist:id/schedule'
    PROJECT_TASK_DATE_INPUT = 'com.todoist:id/scheduler_input'
    PROJECT_TASK_SCHEDULE_SUBMIT_BTN = 'com.todoist:id/scheduler_submit'
    PROJECT_TASK_SUBMIT_BTN = '//android.widget.ImageView[@content-desc="Add"]'

    def __init__(self, app):
        self.app = app

    def select_add_task(self):
        self.app.find_element_by_id(self.ADD_TASK_BTN).click()

    def add_task_title(self, task_title):
        self.app.find_element_by_id(self.PROJECT_TASK_TITLE).send_keys(task_title)

    def __select_task_date(self):
        self.app.find_element_by_id(self.PROJECT_TASK_DATE_OPTION).click()

    def __select_task_date_time_input(self, task_date):
        self.app.find_element_by_id(self.PROJECT_TASK_DATE_INPUT).send_keys(task_date)

    def submit_schedule(self):
        self.app.find_element_by_id(self.PROJECT_TASK_SCHEDULE_SUBMIT_BTN).click()

    def submit_task_schedule(self, task_date):
        self.__select_task_date()
        self.__select_task_date_time_input(task_date)

    def submit_task(self):
        self.app.find_element_by_xpath(self.PROJECT_TASK_SUBMIT_BTN).click()

    def mark_completed_project_task_by_name(self, task_title):
        complete_checkbox = \
            '//android.widget.TextView[@text="{}"]/preceding-sibling::android.widget.CheckBox'.format(task_title)
        self.app.find_element_by_xpath(complete_checkbox).click()

    def get_project_task_by_name(self, task_title):
        task = '//android.widget.TextView[@text="{}"]'.format(task_title)
        return self.app.find_element_by_xpath(task)