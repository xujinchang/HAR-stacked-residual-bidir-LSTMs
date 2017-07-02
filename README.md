# ChaLearn LAP Real Versus Fake Expressed Emotion Challenge @ICCV 2017

# Data Process


Firstly, the videos are preprocessed with the codes in process_video. extract_video.py is used to extract the frame from videos. 

Then the per image is resized using img_resize.m with a radio 1/2. 

After that, we use face detection SDK to detect the face_rect and landmarks in per image and the results are in testcoda_land file and testcoda_rect file. We use the landmark points to align the faces and crop all the faces using corp.py. 

Finally,we just use pro_codatest.py and sort_frame.py to get 128 frames per video.

# Train the model


Firstly, we use a pretrained CNN network vgg16 on fer2013.

Then, the vgg16 is treated as a feature extractor and use the fc7 4096 features.

We use extact_emotion.py to extract the 128 frames per video as the feature of the video.
Before using the lstm to train with all the features, we do a pca and change the final dimensions of features to 1024.

We use train.py to train the lstm network using tensorflow 0.11.0rc0.


# Predict the results


The test.py is used to load the model to predict the test labels.

And the pro_results.py is used to get pkl files.

