import os


def capability_select():
    return {"platformName": "Android",
            "platformVersion": "8.1",
            "automationName": "Appium",
            "appPackage": "ru.mail.search.electroscope",
            "appActivity": ".ui.activity.AssistantActivity",
            "app": os.path.abspath(os.path.join(os.path.dirname(__file__), '../apk/Marussia_v1.57.0.apk')),
            "orientation": "PORTRAIT",
            "autoGrantPermissions": True
            }
