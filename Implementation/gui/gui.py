from Implementation.detection.logging import Logger
from Implementation.detection.detection import Detection
from Implementation.database import Database

from GazeTracking.gaze_tracking import GazeTracking

import wx
import threading
import cv2
import uuid
import os
import shutil

# Define camera to use (0 if only 1 camera connected)
CAMERA = 1
# Define recognition model to use
RECOGNITION_MODEL = 'vgg_face'


class RegistrationFrame(wx.Frame):
    def __init__(self, from_main=False):
        self.db = Database()
        self.detection = Detection()
        # Setup gaze tracking
        self.gaze = GazeTracking()

        # Setup paths
        if from_main:
            logo_path = "./assets/logo.png"
            self.db_path = './database'
            self.detection.set_env()
            self.db.set_env()
        else:
            logo_path = "../assets/logo.png"
            self.db_path = './../database'

        # Delete old representations
        if os.path.isfile('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL)):
            os.unlink('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL))

        # Create new window
        super().__init__(parent=None, title='Automatic Panelist Detection', size=(480, 480))
        self.panel = wx.Panel(self)

        # Create basic interface structure
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

        wx.StaticBitmap(self, -1, wx.Bitmap(logo_path, wx.BITMAP_TYPE_ANY), pos=(25, 25))
        wx.StaticText(self, label='Current Panelists', style=wx.ALIGN_CENTER_HORIZONTAL, pos=(25, 150), size=(120, 20))

        # Start detection loop in different thread
        self.detection_loop_thread = threading.Thread(target=self.detection_loop)
        self.detection_loop_thread.start()

        # Display window
        self.panel.SetSizerAndFit(self.horizontal_sizer)
        self.Show()

    def detection_loop(self):
        print('Panelist detection started.')
        # Initialize video capture using specified camera
        vid = cv2.VideoCapture(CAMERA)
        # In every iteration faces are detected and processed on 1 captured image
        while True:
            # Capture image
            ret, img = vid.read()
            if not ret:
                raise SystemExit('Error occurred while capturing video')

            # Get number of faces detected, images of these faces, and corresponding facial areas
            num_detected, faces, facial_areas = self.detection.detect_faces_deepface_RF(img)
            print('Number of people detected: {}'.format(num_detected))

            # Get identities, genders, ages, emotions, and false positives as arrays for all faces
            identities = self.detection.recognize_faces(faces)
            genders, ages, emotions = self.detection.analyze_faces(faces)
            false_positives = self.detection.liveness_detector(img, facial_areas)

            # Resets GUI sizers
            self.reset_panelists()

            # For each face: Check if face is found in database and load corresponding data from database
            for i, face in enumerate(faces):
                # Check if face belongs to a real person
                if not false_positives[i]:
                    print('Detected face does not belong to a real person.')
                    continue

                # Predict attentiveness
                # Get gaze of current face
                self.gaze.refresh(face)
                # Uncomment to show positions of the eyes in preview image
                # face = self.gaze.annotated_frame()

                # Person is attentive when eyes are not closed
                attentiveness = 0
                if self.gaze.pupils_located:
                    if not self.gaze.is_blinking():
                        attentiveness = 1

                # If face not recognized: Create new database entry and store image
                if identities[i] == "Unknown":
                    # Generate new random id that is still unused
                    used_ids = self.db.get_ids()
                    while True:
                        id = uuid.uuid4().int % 100
                        if id not in used_ids:
                            break

                    # Name used for the unknown person
                    name = 'Unknown-' + str(id)
                    identities[i] = name
                    # Gender is < 0.5 for men and >= 0.5 for women
                    int_gender = 0 if genders[i] == 'Man' else 1

                    # Add person to the database and save image of the face
                    self.db.add_family_entry(id, name, ages[i], int_gender, fixed=False)
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

                    # Delete old representations
                    if os.path.isfile('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL)):
                        os.unlink('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL))

                else:
                    # Face is recognized
                    # Load person's information from database
                    id, age, gender, it = self.db.get_member(identities[i])
                    name = identities[i]
                    # Gender is < 0.5 for men and >= 0.5 for women
                    int_gender = 0 if genders[i] == 'Man' else 1

                    # it is always 0 if gender and age are fixed by user
                    if it == 0:
                        # Gender is < 0.5 for men and >= 0.5 for women
                        str_gender = 'Man' if gender < 0.5 else 'Woman'
                        # Update age and gender based on the database
                        genders[i] = str_gender
                        # Age estimates are floats -> convert to int
                        ages[i] = int(age)

                    # it != 0 -> gender and age are estimated
                    else:
                        # Update gender age age estimates with average values
                        new_age = (age * it + ages[i]) / (it + 1)
                        new_gender = (gender * it + int_gender) / (it + 1)
                        self.db.update_family_entry(identities[i], new_age, new_gender, fixed=False)

                        # Gender is < 0.5 for men and >= 0.5 for women
                        str_gender = 'Man' if new_gender < 0.5 else 'Woman'
                        # Update age and gender based on the database
                        genders[i] = str_gender
                        # Age estimates are floats -> convert to int
                        ages[i] = int(new_age)

                        # Save image of the face
                        if not os.path.exists(f'{self.db_path}/{name}'):
                            os.mkdir(f'{self.db_path}/{name}')
                        img_ids = []
                        for f in os.listdir(f'{self.db_path}/{name}'):
                            img_ids.append(int(f.split(os.sep)[-1][:-4]))
                        if not img_ids:
                            img_id = 0
                        else:
                            img_id = max(img_ids) + 1
                        if max(img_ids) < 3: # Save images only at the first 3 iteration
                            img_path = f'{self.db_path}/{name}/{img_id}.jpg'
                            cv2.imwrite(img_path, face)
                            # Delete old representations
                            if os.path.isfile('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL)):
                                os.unlink('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL))

                # Log attributes of detected face
                # attentiveness = 0 (not implemented)
                Logger.log(id, genders[i], ages[i], emotions[i], attentiveness)

                # Add new button containing person's name and corresponding attributes to GUI
                self.add_panelist(genders[i], ages[i], emotions[i], identities[i], attentiveness, face)

    def add_panelist(self, gender, age, emotion, name, attentiveness, face):
        # Add new button containing person's name and corresponding attributes to GUI
        panelist_btn = wx.Button(self, label=name+'\n{} | {} | {} | {}'.format(gender, age, emotion, attentiveness), size=(150, 50))
        self.panelists_sizer.Add(panelist_btn, 0, wx.TOP, 10)
        self.panel.SetSizerAndFit(self.horizontal_sizer)
        # Call registration method if button is pressed
        panelist_btn.Bind(wx.EVT_BUTTON, lambda event, gender=gender, age=age, name=name, attentiveness=attentiveness,
                                                face=face: self.registration(gender, age, name, face))

    def reset_panelists(self):
        # Resets GUI sizers
        self.panelists_sizer.Clear(True)
        self.panelists_sizer.AddSpacer(180)
        self.upper_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.image_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_sizer = wx.BoxSizer(wx.VERTICAL)
        self.registration_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.Add(self.image_sizer)
        self.right_sizer.Add(self.upper_horizontal_sizer, 0, wx.TOP, 40)
        self.upper_horizontal_sizer.Add(self.text_sizer, 0, wx.LEFT, 0)
        self.upper_horizontal_sizer.Add(self.registration_sizer, 0, wx.LEFT, 40)
        self.panel.SetSizerAndFit(self.horizontal_sizer)

    def reset_registration(self):
        # Clear registration window
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
        # Clear registration window
        self.reset_registration()

        # Create new registration window
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

        # Save entered registration information in database
        registration_btn.Bind(wx.EVT_BUTTON, lambda event, face=face: self.save_registration_info(face, name))
        self.right_sizer.Add(registration_btn, 0, wx.TOP | wx.CENTER, 30)

        self.panel.SetSizerAndFit(self.horizontal_sizer)

    def save_registration_info(self, face, orig_name):
        # Get entered information
        name = self.name_ctrl.GetValue()
        gender = self.gender_ctrl.GetValue()
        age = self.age_ctrl.GetValue()

        # Generate new random id that is still unused
        used_ids = self.db.get_ids()
        while True:
            rand_id = uuid.uuid4().int % 100
            if rand_id not in used_ids:
                break

        # If name was changed by the user (Can happen if the user was unknown before)
        if name != orig_name:
            # Update name in database
            self.db.update_name(orig_name, name)

            # If photo folder with new name already exits: Move images to this folder
            if os.path.isdir(self.db_path + os.sep + name):
                img_ids = []
                for f in os.listdir(self.db_path + os.sep + name):
                    img_ids.append(int(f.split(os.sep)[-1][:-4]))
                if not img_ids:
                    img_id = 0
                else:
                    img_id = max(img_ids) + 1
                for i, file in enumerate(os.listdir(self.db_path + os.sep + orig_name)):
                    shutil.move(self.db_path + os.sep + orig_name + os.sep + file, self.db_path + os.sep + name +
                                os.sep + str(img_id + i) + '.jpg')
                os.rmdir(self.db_path + os.sep + orig_name)
            # If photo folder with new name does not exits: Rename old folder
            else:
                os.rename(self.db_path + os.sep + orig_name, self.db_path + os.sep + name)

        # Delete old representations
        if os.path.isfile('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL)):
            os.unlink('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL))

        # Gender is < 0.5 for men and >= 0.5 for women
        str_gender = 0 if gender == 'Man' else 1

        # Update information stored in database
        if self.db.check_member_exists(name):
            self.db.update_family_entry(name, age, str_gender)
        else:
            self.db.add_family_entry(rand_id, name, age, str_gender)

        # Save image of the face
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

        # Delete old representations
        if os.path.isfile('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL)):
            os.unlink('{}/representations_{}.pkl'.format(self.db_path, RECOGNITION_MODEL))

        # Clear registration window
        self.reset_registration()


if __name__ == '__main__':
    # Start GUI
    app = wx.App()
    frame = RegistrationFrame()
    app.MainLoop()
