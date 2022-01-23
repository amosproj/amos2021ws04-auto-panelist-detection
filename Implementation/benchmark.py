from detection import detection
import image.draw as draw

import json
import time
import pandas as pd
import cv2
import os
import numpy as np
import threading
import psutil


DETECTION_LABELS = './test images/detection_benchmark.json'
RECOGNITION_LABELS = './test images/recognition_benchmark_low_res.json'

class Benchmark:

    def __init__(self):
        detection.set_env()
        self.cpu_usage = []
        self.ram_usage = []
        self.detection_ongoing = False


    def get_sys_load(self):
        while self.detection_ongoing:
            self.cpu_usage.append(psutil.cpu_percent())
            self.ram_usage.append(psutil.virtual_memory().percent)
            time.sleep(0.5)


    def run_benchmark_detection(self):
        detection_methods = ['Retina_Face']
        data_detection = {'Path': [], 'Img_Res': [], 'Face_Res': [], 'Method': [], 'Detection_Time': [],
                          'Detection_CPU_Usage': [],
                          'Detection_RAM_Usage': [], 'Faces_Truth': [], 'Faces_Static': [],
                          'Faces_Detected': [], 'Detection_Correct': [], 'Bounding_Boxes': []}
        f_detection = open(DETECTION_LABELS)
        detection_data = json.load(f_detection)
        imgs = []
        total_faces = 0
        total_faces_detected = 0
        times = []
        cpu_ = []
        ram_ = []
        f_detection.close()
        for img in detection_data:
            for method in detection_methods:
                st = time.time()
                self.detection_ongoing = True
                sys_load_thread = threading.Thread(target=self.get_sys_load)
                sys_load_thread.start()
                print('Testing {}'.format('./test images/' + img['path']))
                bb_img = cv2.imread('./test images/' + img['path'])
                img_res = '{} x {}'.format(bb_img.shape[1], bb_img.shape[0])
                if method == 'Retina_Face':
                    number, faces, facial_areas = detection.detect_faces_deepface_RF(bb_img)
                else:
                    raise NotImplementedError
                face_res_height_list = []
                face_res_width_list = []
                for face in faces:
                    face_res_height_list.append(face.shape[0])
                    face_res_width_list.append(face.shape[1])
                face_res = '{:.0f} x {:.0f}'.format(np.mean(face_res_width_list), np.mean(face_res_height_list))
                t = time.time() - st
                times.append(t)
                self.detection_ongoing = False
                cpu_usage_detection = np.mean(self.cpu_usage)
                ram_usage_detection = np.mean(self.ram_usage)
                self.ram_usage = []
                self.cpu_usage = []
                cpu_.append(cpu_usage_detection)
                ram_.append(ram_usage_detection)
                detection_correct = (number == img['number'])
                total_faces += img['number']
                total_faces_detected += number
                for facial_area in facial_areas:
                    bb_img = draw.rectangle(bb_img, facial_area)
                filename = './benchmark/bounding_boxes/{}.jpg'.format(len(data_detection['Method']))
                if not os.path.isdir('./benchmark'):
                    os.mkdir('./benchmark')
                if not os.path.isdir('./benchmark/bounding_boxes'):
                    os.mkdir('./benchmark/bounding_boxes')
                cv2.imwrite(filename, bb_img)
                imgs.append(filename)

                data_detection['Path'].append(img['path'])
                data_detection['Img_Res'].append(img_res)
                data_detection['Face_Res'].append(face_res)
                data_detection['Method'].append(method)
                data_detection['Detection_Time'].append(t)
                data_detection['Detection_CPU_Usage'].append(cpu_usage_detection)
                data_detection['Detection_RAM_Usage'].append(ram_usage_detection)
                data_detection['Faces_Truth'].append(img['number'])
                data_detection['Faces_Static'].append(img['number_static'])
                data_detection['Faces_Detected'].append(number)
                data_detection['Detection_Correct'].append(detection_correct)
                data_detection['Bounding_Boxes'].append(filename)

        df = pd.DataFrame.from_dict(data_detection)
        writer = pd.ExcelWriter('./benchmark/detection_benchmark.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='detection')

        workbook = writer.book
        worksheet = writer.sheets['detection']

        workbook.formats[0].set_align('top')
        format_correct = workbook.add_format({'bg_color': 'green', 'valign': 'top'})
        format_wrong = workbook.add_format({'bg_color': 'red', 'valign': 'top'})
        worksheet.conditional_format(1, 0, df.shape[0], 12,
                                     {'type': 'cell', 'criteria': '==', 'value': True, 'format': format_correct})
        worksheet.conditional_format(1, 0, df.shape[0], 12,
                                     {'type': 'cell', 'criteria': '==', 'value': False, 'format': format_wrong})
        worksheet.set_landscape()
        worksheet.set_margins(left=0., right=0., top=0., bottom=0.)
        worksheet.set_default_row(400)
        worksheet.set_row(0, 20)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:L', 18)
        worksheet.set_column('M:M', 40)

        for i, img in enumerate(imgs):
            height, width = cv2.imread(img).shape[:2]
            scale = 520 / height
            worksheet.insert_image(1 + i, 13, img, {'x_scale': scale, 'y_scale': scale})

        try:
            detection_accuracy = df.Detection_Correct.value_counts()[True] / df.shape[0]
        except KeyError:
            detection_accuracy = 0
        avg_detection_time = np.mean(times)
        avg_cpu_usage = np.mean(cpu_)
        avg_ram_usage = np.mean(ram_)

        summary_format = workbook.add_format()
        summary_format.set_bold()
        summary_format.set_font_size(16)
        worksheet.set_row(df.shape[0] + 1, 20)
        worksheet.write(df.shape[0] + 1, 0, 'Average detection accuracy: {:.0f}%, detection time: {:.3f}s, cpu usage: {:.3f}%, ram usage: {:.3f}%'.format(detection_accuracy * 100, avg_detection_time, avg_cpu_usage, avg_ram_usage), summary_format)

        workbook.close()

        df.to_csv('./benchmark/detection_benchmark.csv', index=False)

    def run_benchmark_recognition(self):
        recognition_methods = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
        data_recognition = {'Path': [], 'Img_Res': [], 'Face_Res': [], 'Recognition_Method': [], 'Recognition_Time': [],
                            'Recognition_Correct': [],
                            'Recognition_CPU_Usage': [], 'Recognition_RAM_Usage': [], 'Gender_Time': [],
                            'Gender_CPU_Usage': [], 'Gender_RAM_Usage': [], 'Gender_Correct': [],
                            'Age_Time': [], 'Age_CPU_Usage': [], 'Age_RAM_Usage': [], 'Age_Correct': [],
                            'Emotion_Time': [], 'Emotion_CPU_Usage': [], 'Emotion_RAM_Usage': [], 'Emotion_Correct': []}
        f_recognition = open(RECOGNITION_LABELS)
        recognition_data = json.load(f_recognition)
        imgs = []
        f_recognition.close()
        for img in recognition_data:
            for method in recognition_methods:
                filename = './test images/' + img['path']
                print('Testing {}'.format(filename))
                imgs.append(filename)
                bb_img = cv2.imread(filename)
                img_res = '{} x {}'.format(bb_img.shape[1], bb_img.shape[0])
                _, faces, _ = detection.detect_faces_deepface_RF(bb_img)
                face_res_height_list = []
                face_res_width_list = []
                for face in faces:
                    face_res_height_list.append(face.shape[0])
                    face_res_width_list.append(face.shape[1])
                face_res = '{:.0f} x {:.0f}'.format(np.mean(face_res_width_list), np.mean(face_res_height_list))

                st_recognition = time.time()
                self.detection_ongoing = True
                sys_load_thread = threading.Thread(target=self.get_sys_load)
                sys_load_thread.start()
                identity = detection.recognize_faces(faces[0], model=method)[0]
                t_recognition = time.time() - st_recognition
                self.detection_ongoing = False
                cpu_usage_recognition = np.mean(self.cpu_usage)
                ram_usage_recognition = np.mean(self.ram_usage)
                self.ram_usage = []
                self.cpu_usage = []
                recognition_correct = (identity == img['name'])

                st_gender = time.time()
                self.detection_ongoing = True
                sys_load_thread = threading.Thread(target=self.get_sys_load)
                sys_load_thread.start()
                gender = detection.detect_gender(faces[0])
                t_gender = time.time() - st_gender
                self.detection_ongoing = False
                cpu_usage_gender = np.mean(self.cpu_usage)
                ram_usage_gender = np.mean(self.ram_usage)
                self.ram_usage = []
                self.cpu_usage = []
                if gender == "Woman":
                    gender = "f"
                elif gender == "Man":
                    gender = "m"
                gender_correct = (gender == img['gender'])

                st_age = time.time()
                self.detection_ongoing = True
                sys_load_thread = threading.Thread(target=self.get_sys_load)
                sys_load_thread.start()
                age = detection.detect_age(faces[0])
                t_age = time.time() - st_age
                self.detection_ongoing = False
                cpu_usage_age = np.mean(self.cpu_usage)
                ram_usage_age = np.mean(self.ram_usage)
                self.ram_usage = []
                self.cpu_usage = []
                age_correct = (age in range(img['age'] - 10, img['age'] + 10))

                st_emotion = time.time()
                self.detection_ongoing = True
                sys_load_thread = threading.Thread(target=self.get_sys_load)
                sys_load_thread.start()
                emotion = detection.detect_emotion(faces[0])
                t_emotion = time.time() - st_emotion
                self.detection_ongoing = False
                cpu_usage_emotion = np.mean(self.cpu_usage)
                ram_usage_emotion = np.mean(self.ram_usage)
                self.ram_usage = []
                self.cpu_usage = []
                emotion_correct = (emotion == img['emotion'])

                data_recognition['Path'].append(img['path'])
                data_recognition['Img_Res'].append(img_res)
                data_recognition['Face_Res'].append(face_res)
                data_recognition['Recognition_Method'].append(method)
                data_recognition['Recognition_Time'].append(t_recognition)
                data_recognition['Recognition_CPU_Usage'].append(cpu_usage_recognition)
                data_recognition['Recognition_RAM_Usage'].append(ram_usage_recognition)
                data_recognition['Recognition_Correct'].append(recognition_correct)
                data_recognition['Gender_Time'].append(t_gender)
                data_recognition['Gender_CPU_Usage'].append(cpu_usage_gender)
                data_recognition['Gender_RAM_Usage'].append(ram_usage_gender)
                data_recognition['Gender_Correct'].append(gender_correct)
                data_recognition['Age_Time'].append(t_age)
                data_recognition['Age_CPU_Usage'].append(cpu_usage_age)
                data_recognition['Age_RAM_Usage'].append(ram_usage_age)
                data_recognition['Age_Correct'].append(age_correct)
                data_recognition['Emotion_Time'].append(t_emotion)
                data_recognition['Emotion_CPU_Usage'].append(cpu_usage_emotion)
                data_recognition['Emotion_RAM_Usage'].append(ram_usage_emotion)
                data_recognition['Emotion_Correct'].append(emotion_correct)

        if not os.path.isdir('./benchmark'):
            os.mkdir('./benchmark')

        df = pd.DataFrame.from_dict(data_recognition)

        writer = pd.ExcelWriter('./benchmark/recognition_benchmark.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='recognition')

        workbook = writer.book
        worksheet = writer.sheets['recognition']

        workbook.formats[0].set_align('top')
        format_correct = workbook.add_format({'bg_color': 'green', 'valign': 'top'})
        format_wrong = workbook.add_format({'bg_color': 'red', 'valign': 'top'})
        worksheet.conditional_format(1, 0, df.shape[0], 20,
                                     {'type': 'cell', 'criteria': '==', 'value': True, 'format': format_correct})
        worksheet.conditional_format(1, 0, df.shape[0], 20,
                                     {'type': 'cell', 'criteria': '==', 'value': False, 'format': format_wrong})
        worksheet.set_landscape()
        worksheet.set_margins(left=0., right=0., top=0., bottom=0.)
        worksheet.set_default_row(400)
        worksheet.set_row(0, 20)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:U', 18)

        for i, img in enumerate(imgs):
            height, width = cv2.imread(img).shape[:2]
            scale = 400 / height
            worksheet.insert_image(1 + i, 21, img, {'x_scale': scale, 'y_scale': scale})

        recognition_accuracy = []
        for recognition_method in recognition_methods:
            try:
                recognition_accuracy.append(df[df['Recognition_Method'] == recognition_method].Recognition_Correct.value_counts()[True] / df[df['Recognition_Method'] == recognition_method].shape[0])
            except KeyError:
                recognition_accuracy.append(0)
        try:
            gender_accuracy = df.Gender_Correct.value_counts()[True] / df.shape[0]
        except KeyError:
            gender_accuracy = 0
        try:
            age_accuracy = df.Age_Correct.value_counts()[True] / df.shape[0]
        except KeyError:
            age_accuracy = 0
        try:
            emotion_accuracy = df.Emotion_Correct.value_counts()[True] / df.shape[0]
        except KeyError:
            emotion_accuracy = 0

        summary_format = workbook.add_format()
        summary_format.set_bold()
        summary_format.set_font_size(16)
        for i, recognition_method in enumerate(recognition_methods):
            worksheet.set_row(df.shape[0] + 1 + i, 20)
            worksheet.write(df.shape[0] + 1 + i, 0,
                            '{}: Average recognition accuracy: {:.0f}%, gender accuracy: {:.0f}s, age accuracy: {:.0f}%, emotion accuracy: {:.0f}%'.format(
                                recognition_method, recognition_accuracy[i] * 100, gender_accuracy * 100, age_accuracy * 100, emotion_accuracy * 100), summary_format)

        workbook.close()

        df.to_csv('./benchmark/recognition_benchmark.csv', index=False)


if __name__ == '__main__':
    bm = Benchmark()
    bm.run_benchmark_detection()
    bm.run_benchmark_recognition()
