import npyscreen
import json

class ResetSettings(npyscreen.ButtonPress):
    def whenPressed(self):
        self.settings={"Save account":True,"Account":{"login":"None","password":"None"}}

        with open("settings.json","w") as settings_file:
            json.dump(self.settings, settings_file)

        self.parent.UpdateSettings()
        return super().whenPressed()

class SaveSettings(npyscreen.ButtonPress):
    def whenPressed(self):
        with open("settings.json","r") as settings_file:
            self.parent.settings = json.load(settings_file)

        if self.parent.save_account.value=="Y":
            self.parent.settings["Save account"]=True
        else:
            self.parent.settings["Save account"]=False
            self.parent.settings["Account"]={"login":"None","password":"None"}

        with open("settings.json","w") as settings_file:
            json.dump(self.parent.settings, settings_file)

        self.parent.UpdateSettings()

        return super().whenPressed()

class Settings(npyscreen.FormBaseNewWithMenus):
    def create(self):
        SelectSection = self.new_menu(name="Menu")
        SelectSection.addItem(text="Messenger",onSelect=self.Switch2Messenger)
        SelectSection.addItem(text="Friends",onSelect=self.Switch2Friends)
        SelectSection.addItem(text="Settings",onSelect=None)
        SelectSection.addItem(text="Quit",onSelect=self.parentApp.exit_func)

        self.save_account = self.add(npyscreen.TitleText,
                name="Save account after exiting [Y/N]:", 
                value="Y",
                use_two_lines=False,
                begin_entry_at=38)

        self.add(SaveSettings,name="Save Settings")
        self.add(ResetSettings,name="Reset Settings")

        try:
            self.UpdateSettings()
        except:
            self.settings={"Save account":True,"Account":{"login":"None","password":"None"}}

            with open("settings.json","w") as settings_file:
                json.dump(self.settings, settings_file)

    def UpdateSettings(self):
        with open("settings.json","r") as settings_file:
            self.settings = json.load(settings_file)

        if self.settings["Save account"]:
            self.save_account.value="Y"
        else:
            self.save_account.value="N"

    def Switch2Messenger(self):
        self.parentApp.switchForm("Messenger")
        self.parentApp.getForm("Messenger").conversations_list.Update()   

    def Switch2Friends(self):
        self.parentApp.switchForm("Friends")
        self.parentApp.getForm("Friends").friends_list.Update()   
