import npyscreen, os, json
from singin import SingIn
from messenger import  Messenger
from settings import Settings
from friends import Friends

class App(npyscreen.StandardApp):
    def onStart(self):
        if not os.path.isfile("settings.json"):
            self.settings={"Save account":True,"Account":{"login":"None","password":"None"}}

            with open("settings.json","w") as settings_file:
                json.dump(self.settings, settings_file)

        self.addForm("MAIN", SingIn, name="VkArtem")
        self.addForm("Messenger", Messenger, name="VkArtem")
        if self.getForm("MAIN").CheckIfHasAccount():
            self.setNextForm("Messenger")
            self.getForm("Messenger").conversations_list.Update()   
        self.addForm("Settings", Settings, name="VkArtem")
        self.addForm("Friends", Friends, name="VkArtem")
        
        handlers = {
            "^Q": self.exit_func
        }
        self.getForm("MAIN").add_handlers(handlers)
        self.getForm("Messenger").add_handlers(handlers)
        self.getForm("Settings").add_handlers(handlers)
        self.getForm("Friends").add_handlers(handlers)

    def exit_func(self,_input=None):
        self.switchForm(None)
        print(_input)

if "__main__"==__name__:
    App().run()
