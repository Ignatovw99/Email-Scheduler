import wx
import wx.adv
import datetime
import util

from service import save_email
from config import ui_config

class AppFrame(wx.Frame):

    def __init__(self, parent, title):
        super(AppFrame, self).__init__(parent, title=title, size=(800, 600))
        self.panel = AppPanel(self)

class AppPanel(wx.Panel):

    def __init__(self, parent):
        super(AppPanel, self).__init__(parent)

        self.title_font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.content_font = wx.Font(11, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
      
        panel_content = EmailSchedulerPanelContent(self)
        self.SetSizer(panel_content.vertical_box)

    def handle_schedule_event(self, event):

        recipients_input = self.recipients_control.GetValue()
        recipients = [email_address.strip() for email_address in recipients_input.strip(";").split(";")]
        subject_input = self.subject_control.GetValue()
        content_input = self.content_control.GetValue()
        datetime_input = util.convert_to_python_datetime(self.date_control.GetValue(), self.time_control.GetValue())
        datetime_tolerance = datetime.datetime.now() + datetime.timedelta(minutes = ui_config["min_possible_minutes_tolerance"])
        datetime_tolerance = datetime_tolerance.replace(second=0, microsecond=0)
        
        if util.is_empty(recipients_input):
            self.show_error("Recipients field can not be empty.")
        elif util.are_email_addresses_valid(recipients) == False:
            self.show_error("You have entered wrong email addess/es.")
        elif util.is_empty(subject_input):
            self.show_error("Subject can not be empty.")
        elif len(subject_input) < 2:
            self.show_error("Subject should contain at least 2 characters.")
        elif util.is_empty(content_input):
            self.show_error("Content can not be empty.")
        elif len(content_input) < 10:
            self.show_error("Content should contain at least 10 characters.")
        elif datetime_input < datetime_tolerance:
            self.show_error(f"Input date time should be after: {util.convert_datetime_to_string(datetime_tolerance)}")
        else:
            save_email(subject_input, content_input, recipients, datetime_input)
            self.clear_input_elements()
        
        util.sync_date_pickup_element(wx, self.date_control)
        util.sync_time_pickup_element(wx, self.time_control)


    def show_error(self, message):

        error_dialog = wx.MessageDialog(self, message, "Error", wx.OK|wx.STAY_ON_TOP|wx.CENTRE)
        error_dialog.ShowModal()

    def clear_input_elements(self):
        self.recipients_control.SetValue("")
        self.subject_control.SetValue("")
        self.content_control.SetValue("")


class EmailSchedulerPanelContent():

    def __init__(self, panel):
        self.vertical_box = wx.BoxSizer(wx.VERTICAL)
        flex_grid_sizer = wx.FlexGridSizer(5, 2, 30, 25)
        
        title_label = wx.StaticText(panel, label="Schedule an email")
        title_label.SetFont(panel.title_font)

        self.vertical_box.AddSpacer(30)
        self.vertical_box.Add(title_label, flag = wx.ALIGN_CENTER)

        flex_grid_sizer.AddMany([
            *self.init_text_control_elements(panel),
            *self.init_date_time_elements(panel)
        ])

        flex_grid_sizer.AddGrowableRow(2, 1)
        flex_grid_sizer.AddGrowableCol(1, 1)

        self.vertical_box.Add(flex_grid_sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        
        schedule_btn = wx.Button(panel, label="Schedule", size=(140, 60))
        schedule_btn.SetFont(panel.content_font)
        schedule_btn.Bind(wx.EVT_BUTTON, panel.handle_schedule_event)

        self.vertical_box.Add(schedule_btn, flag=wx.ALIGN_CENTER)
        self.vertical_box.AddSpacer(30)

    def init_text_control_elements(self, panel):

        recipients_label = wx.StaticText(panel, label="Recipients")
        recipients_label.SetFont(panel.content_font)
        subject_label = wx.StaticText(panel, label="Subject")
        subject_label.SetFont(panel.content_font)
        content_label = wx.StaticText(panel, label="Content")
        content_label.SetFont(panel.content_font)

        panel.recipients_control = wx.TextCtrl(panel)
        panel.subject_control = wx.TextCtrl(panel)
        panel.content_control = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        return (
            (recipients_label),
            (panel.recipients_control, 1, wx.EXPAND),
            (subject_label),
            (panel.subject_control, 1, wx.EXPAND),
            (content_label, 1, wx.EXPAND),
            (panel.content_control, 1, wx.EXPAND)
        )

    def init_date_time_elements(self, panel):
        
        date_label = wx.StaticText(panel, label="Date")
        date_label.SetFont(panel.content_font)
        
        time_label = wx.StaticText(panel, label="Time")
        time_label.SetFont(panel.content_font)

        panel.date_control = wx.adv.DatePickerCtrl(panel, size=(120, 30))
        panel.time_control = wx.adv.TimePickerCtrl(panel, size=(120, 30))
        
        util.sync_date_pickup_element(wx, panel.date_control)
        util.sync_time_pickup_element(wx, panel.time_control)

        return (
            (date_label),
            (panel.date_control, 1, wx.ALL),
            (time_label),
            (panel.time_control, 1, wx.ALL)
        )

class EmailSchedulerApp(wx.App):

    def OnInit(self):
         self.frame = AppFrame(parent=None, title="Gmail Scheduler")
         self.frame.Show()
         return True