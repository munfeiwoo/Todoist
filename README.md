# Setel test-automation-challenge

This is part of test automation challenge posted by Setel. I am using pytest framework and Appium to cover the API and mobile application testing based on Todoist mobile app. I was working on Windows 10 installed with Appium 1.17.1 and python 3.8.

# Machine setup
1. Python 3.8
2. pip
3. pipenv
4. Appium 1.17.1
5. Andriod studio to configure your emulator
6. Preinstall Todoist application in your emulator

# Overview of the test structure or framework
Overall test framework is based on pytest and following page object model concept to improve on maintainability of the UI or codes. You could run both API test and mobile test separately according to your CI/CD setup (please refer to the example command line execution).

Please be noted of the assertions made in the API call to ensure any error being captured or prompted

Each test was scripted as an independent test to ensure the test could be executed as a standalone and representing a user story or feature

There are markers for each test to add flexibility to execute certain test cases

Please be noted the following folders are just to demonstrate potential structure for adding page objects and test automation for web in the future
```
   setel
   |---pages
   |   |-----web"
   |---web      
```

# Cloning the project and install required dependencies
Please execute the following command to clone the project in your working directory
```buildoutcfg
    git clone https://github.com/munfeiwoo/setel.git
```
Execute the following command in the setel project folder to install all dependencies 
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

Please be noted that the configuration is flexible and could change depending on your test setup and you could provide those values on command prompt. Configuration values will be taken from Config.json file if no value provided in command prompt

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

# Example command line text execution

API test

To execute test on API
```
pipenv run python -m pytest c:\setel\API 
```

To test all project releated API
```
pipenv run python -m pytest c:\setel\API -m "Project"
```

To test all task releated API
```
pipenv run python -m pytest c:\setel\API -m "Task"
```

To test all API passing token value in command prompt
```
pipenv run python -m pytest c:\setel\API --apitoken="XXXXXXXX"
```

Mobile APP

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

To test all API passing token value in command prompt
```
pipenv run python -m pytest c:\setel\mobile --apitoken="XXXXXXXX"
```
