import wx
import threading

from Implementation.detection.logging import Logger
from Implementation.detection import detection
from Implementation import add_family_entry as db

import matplotlib.pyplot as plt
import cv2
import uuid
import os

CAMERA = 1
RECOGNITION_MODEL = 'arcface'


class RegistrationFrame(wx.Frame):
    def __init__(self, from_main=False):
        if from_main:
            logo_path = "./assets/logo.png"
            self.db_path = './database'
            detection.set_env()
            db.set_env()
        else:
            logo_path = "../assets/logo.png"
            self.db_path = './../database'
        super().__init__(parent=None, title='Automatic Panelist Detection', size=(480, 480))
        self.panel = wx.Panel(self)

        self.horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panelists_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.upper_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.image_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_sizer = wx.BoxSizer(wx.VERTICAL)
        self.registration_sizer = wx.BoxSizer(wx.VERTICAL)
        self.horizontal_sizer.Add(self.panelists_sizer, 0, wx.LEFT, 10)
        self.horizontal_sizer.Add(self.right_sizer, 0, wx.LEFT, 50)
        self.right_sizer.Add(self.image_sizer)
        self.right_sizer.Add(self.upper_horizontal_sizer, 0, wx.TOP, 40)
        self.upper_horizontal_sizer.Add(self.text_sizer, 0, wx.LEFT, 0)
        self.upper_horizontal_sizer.Add(self.registration_sizer, 0, wx.LEFT, 40)

        self.detection_loop_thread = threading.Thread(target=self.detection_loop)
        self.detection_loop_thread.start()

        wx.StaticBitmap(self, -1, wx.Bitmap(logo_path, wx.BITMAP_TYPE_ANY), pos=(25, 25))
        wx.StaticText(self, label='Current Panelists', style=wx.ALIGN_CENTER_HORIZONTAL, pos=(25, 150), size=(120, 20))

        self.panel.SetSizerAndFit(self.horizontal_sizer)
        self.Show()

    def detection_loop(self):
        print('Panelist detection started.')
        vid = cv2.VideoCapture(CAMERA)
        while True:
            ret, img = vid.read()
            if not ret:
                raise SystemExit('Error occurred while capturing video')
            num_detected, faces = detection.detect_faces_deepface(img)
            print('Number of people detected: {}'.format(num_detected))
            identities = detection.recognize_faces(faces)
            genders, ages, emotions = detection.analyze_faces(faces)
            self.reset_panelists()
            for i, face in enumerate(faces):
                plt.imshow(face)
                if identities[i] == "Unknown":
                    id = 0
                    identities[i] = "Not Recognized"
                else:
                    id, age, gender = db.get_member(identities[i])
                    genders[i] = gender
                    ages[i] = age
                # attentiveness = 0 (not implemented)
                Logger.log(id, genders[i], ages[i], emotions[i], 0)
                self.add_panelist(genders[i], ages[i], emotions[i], identities[i], face)

    def add_panelist(self, gender, age, emotion, name, face):
        panelist_btn = wx.Button(self, label=name+'\n{} | {} | {}'.format(gender, age, emotion), size=(150, 50))
        self.panelists_sizer.Add(panelist_btn, 0, wx.TOP, 10)
        self.panel.SetSizerAndFit(self.horizontal_sizer)
        panelist_btn.Bind(wx.EVT_BUTTON, lambda event, gender=gender, age=age, name=name, face=face: self.registration(gender, age, name, face))

    def reset_panelists(self):
        self.panelists_sizer.Clear(True)
        self.panelists_sizer.AddSpacer(180)
        self.panel.SetSizerAndFit(self.horizontal_sizer)

    def reset_registration(self):
        self.right_sizer.Clear(True)
        self.upper_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.image_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_sizer = wx.BoxSizer(wx.VERTICAL)
        self.registration_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.Add(self.image_sizer)
        self.right_sizer.Add(self.upper_horizontal_sizer, 0, wx.TOP, 40)
        self.upper_horizontal_sizer.Add(self.text_sizer, 0, wx.LEFT, 0)
        self.upper_horizontal_sizer.Add(self.registration_sizer, 0, wx.LEFT, 40)
        self.panel.SetSizerAndFit(self.horizontal_sizer)

    def registration(self, gender, age, name, face):
        self.reset_registration()

        scale = 200 / face.shape[0]
        width = int(face.shape[1] * scale)
        height = int(face.shape[0] * scale)
        face = cv2.resize(face, (width, height), interpolation = cv2.INTER_AREA)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        img = wx.BitmapFromBuffer(width, height, face)
        img = wx.StaticBitmap(self, -1, img, pos=(200, 25))
        self.image_sizer.Add(img, 0, wx.TOP | wx.CENTER, 10)

        name_label = wx.StaticText(self, label='Name:', style=wx.ALIGN_LEFT)
        self.text_sizer.Add(name_label, 0, wx.TOP, 10)
        gender_label = wx.StaticText(self, label='Gender:', style=wx.ALIGN_LEFT)
        self.text_sizer.Add(gender_label, 0, wx.TOP, 10)
        age_label = wx.StaticText(self, label='Age:', style=wx.ALIGN_LEFT)
        self.text_sizer.Add(age_label, 0, wx.TOP, 10)

        self.name_ctrl = wx.TextCtrl(self, style=wx.ALIGN_LEFT, size=(160, 20))
        self.name_ctrl.AppendText(name)
        self.registration_sizer.Add(self.name_ctrl, 0, wx.TOP, 10)
        self.gender_ctrl = wx.TextCtrl(self, style=wx.ALIGN_LEFT, size=(160, 20))
        self.gender_ctrl.AppendText(gender)
        self.registration_sizer.Add(self.gender_ctrl, 0, wx.TOP, 10)
        self.age_ctrl = wx.TextCtrl(self, style=wx.ALIGN_LEFT, size=(160, 20))
        self.age_ctrl.AppendText(str(age))
        self.registration_sizer.Add(self.age_ctrl, 0, wx.TOP, 10)

        registration_btn = wx.Button(self, label='Save Changes', size=(160, 30))
        registration_btn.Bind(wx.EVT_BUTTON, lambda event, face=face: self.save_registration_info(face))
        self.right_sizer.Add(registration_btn, 0, wx.TOP | wx.CENTER, 30)

        self.panel.SetSizerAndFit(self.horizontal_sizer)

    def save_registration_info(self, face):
        name = self.name_ctrl.GetValue()
        gender = self.gender_ctrl.GetValue()
        age = self.age_ctrl.GetValue()
        # random generated id
        used_ids = db.get_ids()
        while True:
            rand_id = uuid.uuid4().int % 100
            if rand_id not in used_ids:
                break
        if db.check_member_exists(name):
            db.update_family_entry(name, age, gender)
        else:
            db.add_family_entry(rand_id, name, age, gender)
        if not os.path.exists(f'{self.db_path}/{name}'):
            os.mkdir(f'{self.db_path}/{name}')
        img_ids = []
        for f in os.listdir(f'{self.db_path}/{name}'):
            img_ids.append(int(f.split(os.sep)[-1][:-4]))
        if not img_ids:
            img_id = 0
        else:
            img_id = max(img_ids) + 1
        img_path = f'{self.db_path}/{name}/{img_id}.jpg'
        cv2.imwrite(img_path, face)
        if os.path.isfile('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL)):
            os.unlink('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL))
        self.reset_registration()


if __name__ == '__main__':
    app = wx.App()
    frame = RegistrationFrame()
    app.MainLoop()
