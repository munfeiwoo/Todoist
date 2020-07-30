# Todoist test-automation-challenge

This is part of test automation challenge to perform test automation on API and mobile app. I am using pytest framework and Appium to perform API, web, and mobile application testing on Todoist mobile app. I was working on Windows 10 installed with Appium 1.17.1 and Python 3.8. (Please refer to the next section on the setup of my machine)


# Machine setup
    1. Python 3.8
    2. pip 20.1
    3. pipenv 2018.11.26
    4. Appium 1.17.1
    5. Andriod studio 3.6.3 (to configure your emulator). 
    6. Preinstall Todoist application in your emulator
    

Please be noted I have setup my Todoist account manually and I have installed the Todoist app from Google Playstore in the emulator since I was getting page not found error when accessing to http://files.slatestudio.com/sr82 provided in the assignment 

**Emulator Setup**

I have setup 2 emulators with the same configuration to demonstrate execution of test in parallel

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

It is a best practice to ensure each automated test case is independent and self-contained. Each test was scripted as an independent automated test to ensure the test could be executed as a standalone test. You will also noticed that there is a **Setup**, **Body** and **Teardown** section in each automated test. All prerequisites will be run in the Setup section and all data created in a test will be deleted during teardown to ensure the same test could be repeated in a clean state during the next execution cycle.

The test framework will accept test configuration values in command prompt. Together with markers and self-contained automated test, we could run automated tests in parallel in Jenkins (or similar tool) to improve on test execution time to cater for more automated test in the future. (Please refer to the Configuration section and also examples on how to execute test in parallel)

We could have more discussions on the automated test, automation strategy and enhancements during the interview.


# Cloning the project and install required dependencies
Please execute the following command to clone the project in your working directory
```buildoutcfg
    git clone https://github.com/munfeiwoo/Todoist.git
```
Execute the following command in the setel project folder to install all dependencies to run the test 
```buildoutcfg
    pipenv install
```

# Configuration

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
  --udid
```

# Example of command line text execution

Please ensure you are in the project holder (e.g. c:\setel)

#### **API test**

To execute test on API
```
pipenv run python -m pytest .\API 
```

To test all project releated API
```
pipenv run python -m pytest .\API -m "Project" --junitxml .\results\api_results.xml
```

To test all task related API
```
pipenv run python -m pytest .\API -m "Task" --junitxml .\results\api_results.xml
```

To test all API passing token value in command prompt
```
pipenv run python -m pytest .\API --apitoken="XXXXXXXX" --junitxml .\results\api_results.xml
```

##### **Mobile APP**


To execute all mobile app test
```
pipenv run python -m pytest .\mobile --junitxml .\results\web_results.xml
```

To execute task related mobile app test
```
pipenv run python -m pytest .\mobile -m "Task" --junitxml .\results\web_results.xml
```

To execute project related mobile app test
```
pipenv run python -m pytest .\mobile -m "Project" --junitxml .\results\web_results.xml
```

To test all mobile related test through passing token value in command prompt
```
pipenv run python -m pytest .\mobile --token="XXXXXXXX" --junitxml .\results\web_results.xml
```

To test Task and Project related test in parallel on different Appium server and emulator
```
    Please run on different terminal

    pipenv run python -m pytest .\mobile -m "Task" --appiumserver="http://localhost:4724/wd/hub" --udid="emulator-5554" --junitxml .\results\web_results.xml

    pipenv run python -m pytest .\mobile -m "Project" --appiumserver="http://localhost:4723/wd/hub" --udid="emulator-5556" --junitxml .\results\web_results.xml     
```

# Proof of Execution

API
```
https://app.box.com/s/nckb1vdcipc93zefuv3z2i5lxhyqr3fm
```

Mobile
```
https://app.box.com/s/gmaivx28keslm6je8uti3lo9q0t3kjrv
```
