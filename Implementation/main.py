from gui.gui import RegistrationFrame
import api.stats as rest
import api.transmission as mqtt

import wx
import threading

# 'REST' and 'MQTT' are supported
API = 'REST'

if __name__ == "__main__":
    # Start API in new thread
    if API == 'REST':
        threading.Thread(target=rest.start_api).start()
    elif API == 'MQTT':
        threading.Thread(target=mqtt.start_api).start()
    else:
        print('Invalid API entry')

    # Start GUI
    app = wx.App()
    frame = RegistrationFrame(True)
    app.MainLoop()
