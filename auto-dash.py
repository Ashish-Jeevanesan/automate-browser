from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
import threading
import time

class BrowserAutomation:
    def __init__(self, jira_url, jira_username, jira_password):
        self.is_running = False
        self.thread = None
        self.driver = None
        self.urls = ['https://jira.globusmedical.com/secure/Dashboard.jspa?selectPageId=23954', 'https://jira.globusmedical.com/secure/Dashboard.jspa?selectPageId=27941']
        self.jira_username = jira_username
        self.jira_password = jira_password
        self.jira_login_url = jira_url + "/login.jsp"


    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.driver.quit()

    def run(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.jira_login_url)
        self.driver.execute_script(f"window.open('{self.urls[0]}','_blank');")
        self.driver.execute_script(f"window.open('{self.urls[1]}','_blank');")
        

        # Login to Jira
        # self.driver.get(self.jira_login_url)
        self.driver.switch_to.window(self.driver.window_handles[0])
        if 'login.jsp' in self.driver.current_url:
            username_input = self.driver.find_element("id","login-form-username")
            password_input = self.driver.find_element("id","login-form-password")
            username_input.send_keys(self.jira_username)
            password_input.send_keys(self.jira_password)
            password_input.send_keys(Keys.RETURN)

        self.driver.refresh()
        self.driver.close()
        # Switch back to the dashboard and start refreshing
        self.driver.switch_to.window(self.driver.window_handles[1])

        while self.is_running:
            self.driver.refresh()
            time.sleep(20)

            self.driver.switch_to.window(self.driver.window_handles[1])
            # print('url opening --> ',self.driver.window_handles[0])
            self.driver.refresh()
            time.sleep(20)

            self.driver.switch_to.window(self.driver.window_handles[2])

        self.is_running = False

class App:
    def __init__(self, master):
        self.master = master
        master.title("Browser Automation")

        self.label = Label(master, text="Click 'Start' to begin automation.")
        self.label.pack()

        self.start_button = Button(master, text="Start", command=self.start)
        self.start_button.pack()

        self.stop_button = Button(master, text="Stop", command=self.stop, state=DISABLED)
        self.stop_button.pack()

        self.browser_automation = BrowserAutomation('https://jira.globusmedical.com/','ajeevanesan','Shyla@bony123')

    def start(self):
        self.browser_automation.start()
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.label.config(text="Automation is running. Click 'Stop' to end.")

    def stop(self):
        self.browser_automation.stop()
        self.stop_button.config(state=DISABLED)
        self.start_button.config(state=NORMAL)
        self.label.config(text="Automation stopped. Click 'Start' to begin again.")

root = Tk()
app = App(root)
root.mainloop()