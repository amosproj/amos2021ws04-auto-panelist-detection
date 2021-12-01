from retinaface import RetinaFace
from Implementation.addfamilyentry import addfamilyentry
import matplotlib.pyplot as plt
import uuid
import cv2


class Register:

    def register(self, vid):
        self.vid = vid
        ret, img = vid.read()
        if not ret:
            raise SystemExit('Registration error: Error occurred while capturing video')
        faces = RetinaFace.extract_faces(img_path=img, align=True)

        for face in faces:
            plt.imshow(face)
            plt.show()
            value = input('Do you want to register this person? Enter y to continue, n to skip to the next person')
            if value.lower() == 'n':
                continue

            while True:
                fname = (input('Please enter the first name: ')).strip()
                if any(i.isdigit() for i in fname) or not fname:
                    print('Names and gender cannot have numerical values!')
                    continue
                lname = (input('Please enter the last name: ')).strip()
                if any(i.isdigit() for i in lname) or not lname:
                    print('Names and gender cannot have numerical values!')
                    continue
                age = (input('Please enter the age: ')).strip()
                if not age or not age.isdigit() or any(not i.isdigit() for i in age) or int(age) < 0:
                    print('Age must have a numerical non negative value!')
                    continue
                gender = (input('Please enter the gender [m]asculine or [f]eminine or [d]ivers :')).strip()
                if gender.lower() not in ['m', 'f', 'd']:
                    print('Gender must have one of the following values: m, f or d')
                    continue
                # random generated id (temporary)
                rand_id = uuid.uuid4().int % 100
                # replaces id with first name
                img_path = f'./database/{fname}/{rand_id}.jpg'
                cv2.imwrite(img_path, face)
                addfamilyentry(rand_id, fname, lname, age, gender)
                print('Person registered successfully\n')
                break
