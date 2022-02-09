# Design Documentation
- Architecture Design
<p align="center">
<img height="150" src="https://github.com/amosproj/amos2021ws04-auto-panelist-detection/blob/main/Documentation/Design_pipeline.jpg?raw=true">
</p>

Our architecture consists of 5 different components. The first component is responsible for taking frames from the camera every 10 seconds and it should provide it in a way that it can be processed to the next component. Additionally there should be no quality loss in the process. The second component is responsible for the face detection. We are using the face recognition model provided by Adam Geitgey. The model uses dlib's state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the "Labeled Faces in the Wild" benchmark.

After the detection, the faces will be provided to the third component which will crop the face and processes it to the next component. The fourth component is responsible for extracting further informations from the provided frame such as age, gender, emotion and attentiveness etc. . In our last component these informations will be saved locally in a database and later on, the user information will be sent to Gfk Servers anonymously.

- Code Design

Our project has different components. We use OpenCV for Capture the Frame. And Insightface 0.5 for deep face detection. For the face recognition, we use the model from Adam Geitgey.  At the same time we are looking for more efficient modules, because we want the whole thing to work on a Raspberry Pi 4 with 4GB RAM.

We have designed a Remote module for user login. Firstly, a frame capture is made for further use. OpenCV facilitate the face detection. If the face can be recognized, then the person is logged in. If not, it will be added to the database and the user will be asked to register. We also get the number of people who have been detected and how many were recognized, if they are not recognized, people are asked to register. We are currently in the process of recognizing the age, gender and emotions of the users.

Our Database is assumed to be a CSV File, in which we save Name, Age, Gender, Email and Photo of the users. Another task is we will be to send this information to GFK in encrypted form.
