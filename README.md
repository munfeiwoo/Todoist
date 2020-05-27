# Setel test-automation-challenge

This is part of test automation challenge posted by Setel to perform test automation on API and mobile app. I am using pytest framework and Appium to perform API and mobile application testing on Todoist mobile app. I was working on Windows 10 installed with Appium 1.17.1 and Python 3.8. (Please refer to the next section on the setup of my machine)


# Machine setup
    1. Python 3.8
    2. pip 20.1
    3. pipenv 2018.11.26
    4. Appium 1.17.1
    5. Andriod studio 3.6.3 (to configure your emulator). 
    6. Preinstall Todoist application in your emulator
    

Please be noted I have setup my Todoist account manually and I have installed the Todoist app from Google Playstore in the emulator since I was getting page not found error when accessing to http://files.slatestudio.com/sr82 provided in the assignment 

**Emulator Setup**
```
    Device Definition: Nexus 5X
    Release: Nougat
    API Level: 25
    ABI: x86
    Target: Android 7.1.1 (Google Play)     
```


# Overview of the test structure or framework

The test framework is based on pytest and I am following page object model concept to improve on maintainability of the test automation codes if there is any UI changes later on. You could run both API test and mobile test separately according to your CI/CD setup (please refer to the example command line execution).

Please be noted that there are assertions made in the API calls to ensure any unexpected error at the API level being captured or prompted

There are markers for each test to add flexibility to execute certain test cases

Please be noted the following folders are just to demonstrate potential structure for adding page objects and test automation for web in the future. 

```
   setel
   |---pages
   |   |-----web
   |---web      
```

The current test structure is just for the purpose of test automation demonstration covering scenarios mentioned in the assignment and there could be further enhancements to framework.

    1. Test “Create Project”
    2. Test “Create Task via mobile phone”
    3. Test “Reopen Task”

It is a best practice to ensure each automated test case is independent and self-contained. As such, I have rework the steps provided in scenario 2 and 3 not to depends on project and task created in earlier test scenario but still achieving the same test objective. Each test was scripted as an independent automated test to ensure the test could be executed as a standalone test. You will also noticed that there is a **Setup**, **Body** and **Teardown** section in each automated test. All prerequisites will be run in the Setup section and all data created in a test will be deleted during teardown to ensure the same test could be repeated in a clean state during the next execution cycle.

We could have more discussions on the automation strategy and enhancements during the interview.


# Cloning the project and install required dependencies
Please execute the following command to clone the project in your working directory
```buildoutcfg
    git clone https://github.com/munfeiwoo/setel.git
```
Execute the following command in the setel project folder to install all dependencies to run the test 
```buildoutcfg
    pipenv install
```

# Config file

You could configure the following values in the config.json file. API and mobile app test will retrieve required setup values from this file

    1. token: API token as provided by Todoist
    2. project_task_url: end point to project task REST api (https://api.todoist.com/rest/v1/tasks)
    3. project_url: end point to project REST api (https://api.todoist.com/rest/v1/tasks)
    4. email: email used for your Todoist account 
    5. password: Todoist password
    6. appium_server: url to appium server
    7. platform_version: platform version of the emulator
    8. platform_name: platform name of the emulator

Please be noted that the configuration of the test is flexible and could be changed depending on your test setup. You could also provide those values in command prompt. Configuration values will be taken from config.json file if no value provided in command prompt

Available configuration for API test in command prompt

```
  --apitoken
  --apiprojecturl
  --apiprojecttaskurl
```

Available configuration for modile test in command prompt

```
  --appiumserver
  --platformname
  --platformversion
  --token
  --projecturl
  --projecttaskurl
  --email
  --password
```

# Example of command line text execution

#### **API test**

To execute test on API
```
pipenv run python -m pytest c:\setel\API 
```

To test all project releated API
```
pipenv run python -m pytest c:\setel\API -m "Project"
```

To test all task related API
```
pipenv run python -m pytest c:\setel\API -m "Task"
```

To test all API passing token value in command prompt
```
pipenv run python -m pytest c:\setel\API --apitoken="XXXXXXXX"
```

##### **Mobile APP**

To execute all mobile app test
```
pipenv run python -m pytest c:\setel\mobile
```

To execute task related mobile app test
```
pipenv run python -m pytest c:\setel\mobile -m "Task"
```

To execute project related mobile app test
```
pipenv run python -m pytest c:\setel\mobile -m "Project"
```

To test all mobile related test through passing token value in command prompt
```
pipenv run python -m pytest c:\setel\mobile --apitoken="XXXXXXXX"
```

To test Task and Project related test in parallel on different Appium server and emulator
```
    Please run on different terminal

    pipenv run python -m pytest c:\setel\Mobile -m "Task" --appiumserver="http://localhost:4724/wd/hub" --devicename="emulator-5554"

    pipenv run python -m pytest c:\setel\Mobile -m "Project" --appiumserver="http://localhost:4723/wd/hub" --devicename="emulator-5556"    
```