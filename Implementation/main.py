from gui.gui import RegistrationFrame
import wx

if __name__ == "__main__":
    # Start GUI
    app = wx.App()
    frame = RegistrationFrame(True)
    app.MainLoop()