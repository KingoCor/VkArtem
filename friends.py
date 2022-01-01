import npyscreen
from datetime import datetime

class FriendsList(npyscreen.SelectOne):
    def Update(self):
        vk = self.parent.parentApp.vk

        self.parent.friends = vk.friends.get(fields="bdate,city,contacts,country,education,last_seen,nickname,online,sex,status,universities")["items"]
        self.values = [f"{friend}) {self.parent.friends[friend]['first_name']} {self.parent.friends[friend]['last_name']}" for friend in range(len(self.parent.friends))]

    def when_value_edited(self):
        selcted_friend = self.get_selected_objects()
        if selcted_friend!=[]:
            self.parent.friend_info.GetInfo(int(selcted_friend[0].split(")")[0]))

        return super().when_value_edited()

class FriendInfo(npyscreen.BoxTitle):
    def GetInfo(self,friend_index):
        friend=self.parent.friends[friend_index]
        if friend["sex"]==2:
            sex="male"
        else:
            sex="female"

        if not 'bdate' in list(friend):
            friend["bdate"]=""
        if not 'mobile_phone' in list(friend):
            friend["mobile_phone"]=""
        if not 'last_seen' in list(friend):
            friend["last_seen"]={"time":0}
        if not 'status' in list(friend):
            friend["status"]=""
        
        self.values = [
                f"Name: {friend['first_name']} {friend['last_name']}",
                f"Last seen: {datetime.utcfromtimestamp(friend['last_seen']['time']).strftime('%Y-%m-%d %H:%M:%S')}",
                f"Status: {friend['status']}",
                f"Sex: {sex}",
                f"Birthday date: {friend['bdate']}",
                f"Mobile phone: {friend['mobile_phone']}"
                ]
        self.update()

class Friends(npyscreen.FormBaseNewWithMenus):
    def create(self):
        SelectSection = self.new_menu(name="Menu")
        SelectSection.addItem(text="Messenger",onSelect=self.Switch2Messenger)
        SelectSection.addItem(text="Friends",onSelect=None)
        SelectSection.addItem(text="Settings",onSelect=self.Switch2Options)
        SelectSection.addItem(text="Quit",onSelect=self.parentApp.exit_func)

        maxy, maxx = self.useable_space()

        self.friends_list = self.add(FriendsList,max_width=int(maxx/4),name="Friends")
        self.friend_info = self.add(FriendInfo,relx=int(maxx/4+2),rely=1)

    def Switch2Options(self):
        self.parentApp.switchForm("Settings")

    def Switch2Messenger(self):
        self.parentApp.switchForm("Messenger")
        self.parentApp.getForm("Messenger").conversations_list.Update()   
