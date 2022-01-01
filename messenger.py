import npyscreen

class ConversationsList(npyscreen.SelectOne):
    def Update(self):
        #vk = self.parent.parentApp.vk

        #waiting for get permission to work with messages...
        #self.parent.messages = vk.messages.get().items
        #messages = [f"{message.conversation}\n{message.last_message}" for message in self.parent.messages]

        messages = [f"conversation {i}" for i in range(100)]
        self.values=messages

    def when_value_edited(self):
        selcted_conversation = self.get_selected_objects()
        if selcted_conversation!=[]:
            self.parent.conversation.GetConversation(selcted_conversation[0])

        return super().when_value_edited()

class Conversation(npyscreen.BoxTitle):
    def GetConversation(self,userID):
        self.name = str(userID)
        self.values = ["This is right now is unavailable :("]
        self.update()

class Messenger(npyscreen.FormBaseNewWithMenus):
    def create(self):
        SelectSection = self.new_menu(name="Menu")
        SelectSection.addItem(text="Messenger",onSelect=None)
        SelectSection.addItem(text="Friends",onSelect=self.Switch2Friends)
        SelectSection.addItem(text="Settings",onSelect=self.Switch2Options)
        SelectSection.addItem(text="Quit",onSelect=self.parentApp.exit_func)

        maxy, maxx = self.useable_space()

        self.conversations_list = self.add(ConversationsList,max_width=int(maxx/5),name="Conversations")
        self.conversation = self.add(Conversation,relx=int(maxx/5+2),rely=1,name="Nothing selected")

    def Switch2Options(self):
        self.parentApp.switchForm("Settings")

    def Switch2Friends(self):
        self.parentApp.switchForm("Friends")
        self.parentApp.getForm("Friends").friends_list.Update()   
