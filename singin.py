import npyscreen, vk_api, json

class LogInButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.vk_session = vk_api.VkApi(self.parent.login_input.value,self.parent.password_input.actual_value,"8038387")
        try:
            self.parent.parentApp.vk_session.auth()
            self.parent.parentApp.vk = self.parent.parentApp.vk_session.get_api()
            self.parent.parentApp.vk.account.setOnline()
            if self.parent.settings["Save account"] and self.parent.settings["Account"]["login"]=="None":
                self.parent.settings["Account"]={"login":self.parent.login_input.value,"password":self.parent.password_input.actual_value}
                with open("settings.json","w") as settings_file:
                    json.dump(self.parent.settings,settings_file)
                
            self.parent.parentApp.getForm("Messenger").conversations_list.Update()   
            self.parent.parentApp.switchForm("Messenger")

        except Exception as e:
            self.parent.ErrorMessage.value=str(e)
            self.parent.ErrorMessage.hidden=False

class PasswordInput(npyscreen.TitleText):
    def __init__(self, screen, begin_entry_at=16, field_width=None, value="", use_two_lines=None, hidden=False, labelColor='LABEL', allow_override_begin_entry_at=True, hide_password=True, **keywords):
        super().__init__(screen, begin_entry_at=begin_entry_at, field_width=field_width, value=value, use_two_lines=use_two_lines, hidden=hidden, labelColor=labelColor, allow_override_begin_entry_at=allow_override_begin_entry_at, **keywords)

        self.actual_value=self.value
        self.hide_password=hide_password
        if self.hide_password:
            self.value="*"*len(self.actual_value)

    def when_value_edited(self):
        if self.hide_password:
            if len(self.value)>len(self.actual_value):
                self.actual_value+=self.value[-1:]
            elif len(self.value)<len(self.actual_value):
                self.actual_value=self.actual_value[:-1]
            self.value="*"*len(self.actual_value)
        else:
            self.actual_value=self.value

    def ShowPassword(self):
        self.hide_password=False
        self.value=self.actual_value

        return super().when_value_edited()

class SingIn(npyscreen.FormBaseNew): 
    def create(self):
        with open("settings.json","r") as settings_file:
            self.settings=json.load(settings_file)

        maxy, maxx = self.useable_space()

        self.login_input = self.add(npyscreen.TitleText,
                relx=int(maxx/2+1),
                rely=int(maxy/2-4),
                name="Login:",
                use_two_lines=True,
                begin_entry_at=-4,
                field_width=11)
        self.password_input = self.add(PasswordInput,
                relx=int(maxx/2),
                rely=int(maxy/2-2),
                name="Password:",
                use_two_lines=True,
                begin_entry_at=-3,
                field_width=14) 

        self.login_button = self.add(LogInButton,name="Log in",relx=int(maxx/2-1),rely=int(maxy/2))
        self.ErrorMessage=self.add(npyscreen.TitleFixedText,name="Error:",hidden=True)

    def CheckIfHasAccount(self):
        if self.settings["Save account"] and self.settings["Account"]["login"]!="None":
            self.parentApp.vk_session = vk_api.VkApi(self.settings["Account"]["login"],self.settings["Account"]["password"],"8038387")
            self.parentApp.vk_session.auth()
            self.parentApp.vk = self.parentApp.vk_session.get_api()
            self.parentApp.vk.account.setOnline()
            return True
        return False
