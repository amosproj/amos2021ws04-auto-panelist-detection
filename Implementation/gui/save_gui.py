from Implementation import add_family_entry as af
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='GUI FOR Registration', size=(720, 480))
        panel = wx.Panel(self)

        my_sizer = wx.BoxSizer(wx.VERTICAL)  # Regelt die Positionen der Widgets

        textctr1 = self.text_ctrl1 = wx.TextCtrl(panel)
        textctr1.AppendText("First Name")
        my_sizer.Add(textctr1, 0, wx.ALL | wx.EXPAND, 5)

        textctr2 = self.text_ctrl2 = wx.TextCtrl(panel)
        textctr2.AppendText("Last Name")
        my_sizer.Add(textctr2, 0, wx.ALL | wx.EXPAND, 5)

        textctr3 = self.text_ctrl3 = wx.TextCtrl(panel)
        textctr3.AppendText("Age")
        my_sizer.Add(textctr3, 0, wx.ALL | wx.EXPAND, 5)

        textctr4 = self.text_ctrl4 = wx.TextCtrl(panel)
        textctr4.AppendText("Gender")
        my_sizer.Add(textctr4, 0, wx.ALL | wx.EXPAND, 5)

        textctr5 = self.text_ctrl5 = wx.TextCtrl(panel)
        textctr5.AppendText("Photo")
        my_sizer.Add(textctr5, 0, wx.ALL | wx.EXPAND, 5)

        statictext1 = self.static_text1 = wx.StaticText(panel)
        my_sizer.Add(statictext1, 0, wx.ALL | wx.EXPAND, 5)

        statictext2 = self.static_text2 = wx.StaticText(panel)
        my_sizer.Add(statictext2, 0, wx.ALL | wx.EXPAND, 5)

        statictext3 = self.static_text3 = wx.StaticText(panel)
        my_sizer.Add(statictext3, 0, wx.ALL | wx.EXPAND, 5)

        statictext4 = self.static_text4 = wx.StaticText(panel)
        my_sizer.Add(statictext4, 0, wx.ALL | wx.EXPAND, 5)

        statictext5 = self.static_text5 = wx.StaticText(panel)
        my_sizer.Add(statictext5, 0, wx.ALL | wx.EXPAND, 5)

        my_btn = wx.Button(panel, label='Save in CSV')
        my_btn.Bind(wx.EVT_BUTTON, self.on_submit)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(my_sizer)
        self.Show()

    def on_submit(self, e):
        value1 = self.text_ctrl1.GetValue()
        self.static_text1.SetLabelText(f'The First Name is: "{value1}"')

        value2 = self.text_ctrl2.GetValue()
        self.static_text2.SetLabelText(f'The Last Name is: "{value2}"')

        value3 = self.text_ctrl3.GetValue()
        self.static_text3.SetLabelText(f'The Age is: "{value3}"')

        value4 = self.text_ctrl4.GetValue()
        self.static_text4.SetLabelText(f'The Gender is: "{value4}"')

        value5 = self.text_ctrl5.GetValue()
        self.static_text5.SetLabelText(f'You can find the Photo in: "{value5}"')

        af.add_family_entry(0, value1, value2, value3, value4)
        # af.add_family_entry(value1, value2, value3, value4, value5)


def main():
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
