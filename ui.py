import wx
import wx.adv
import datetime
import util

from service import save_email
from config import ui_config

class AppFrame(wx.Frame):

    def __init__(self, parent, title):
        super(AppFrame, self).__init__(parent, title=title, size=(800, 600))
        # self.panel = AppPanel(self)

class EmailSchedulerApp(wx.App):

    def OnInit(self):
         self.frame = AppFrame(parent=None, title="Gmail Scheduler")
         self.frame.Show()
         return True