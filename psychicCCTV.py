import numpy as np
import imutils
import time
import cv2
import os
from pathlib import Path
import PySimpleGUIQt as sg

i_vid = r'Enter path to input video'
o_vid = r'Enter path to output video'
yoloModelPath = Path().parent.absolute()
yoloModelPath = str(yoloModelPath) + "/yoloModel/"
sg.ChangeLookAndFeel('LightGrey')
layout1 = [
		[sg.Text('Perform YOLO Object Detection', size=(50,1), font=('Any',18),text_color='#1c86ee' ,justification='left')],
		[sg.Text('Path to input video'), sg.In(i_vid,size=(40,1), key='input'), sg.FileBrowse(size=(75, 30))],
		[sg.Text('Path to output video'), sg.In(o_vid,size=(40,1), key='output'), sg.FileSaveAs(size=(75, 30))],
		[sg.Text('Confidence'), sg.Slider(range=(0,10),orientation='h', resolution=1, default_value=5, size=(15,15), key='confidence'), sg.T('  ', key='_CONF_OUT_')],
		[sg.Text('Threshold'), sg.Slider(range=(0,10), orientation='h', resolution=1, default_value=3, size=(15,15), key='threshold'), sg.T('  ', key='_THRESH_OUT_')],
		[sg.Text(' '*8), sg.Checkbox('Write output video to disk', key='_DISK_')],
		[sg.OK(size=(100, 30)), sg.Stretch()],
	]

layout2 = [[sg.Text('Extract Audio from different sources', size=(50,1), font=('Any',18),text_color='#1c86ee' ,justification='left')]]

layout3 = [[sg.Text('View frames captured by YOLO Object Detection', size=(80,1), font=('Any',18),text_color='#1c86ee' ,justification='left')],
		   [sg.Text('Path to input video'), sg.In(i_vid,size=(40,1), key='input'), sg.FileBrowse(size=(75, 30))],
		   [sg.Text('Path to output sound tracks'), sg.In(o_vid,size=(40,1), key='output'), sg.FileSaveAs(size=(75, 30))],
		   ]

layout = [[sg.Column(layout1, key='-COLYOLO-'), sg.Column(layout2, visible=False, key='-COLSound-'), sg.Column(layout3, visible=False, key='-COLYOLO Saved Frames-')],
		  [sg.Frame(layout=[[sg.Button('YOLO', size=(50, 30)),
		   sg.Button('Sound', size=(60, 30)), 
		   sg.Button('YOLO Saved Frames', size=(200, 30)), 
		   sg.Button('Exit', size=(50, 30))],
		   ], title='Options', title_color='red', relief=sg.RELIEF_SUNKEN)
		   ]]

win = sg.Window('Psychic CCTV',
				default_element_size=(21,1),
				text_justification='right',
				auto_size_text=False).Layout(layout)

layoutVis = 'YOLO'
while True:
	event, values = win.Read()

	if event in 'YOLO Saved Frames Sound':
		win[f'-COL{layoutVis}-'].update(visible=False)
		layoutVis = event
		win[f'-COL{layoutVis}-'].update(visible=True)

	if event is None or event =='Exit':
		exit()

	if event == 'OK':
		write_to_disk = values['_DISK_']
		args = values

		win.Close()


		gui_confidence = args["confidence"]/10
		gui_threshold = args["threshold"]/10

		labelsPath = os.path.sep.join([yoloModelPath, "model.names"])
		LABELS = open(labelsPath).read().strip().split("\n")

		np.random.seed(42)
		COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
			dtype="uint8")

		weightsPath = os.path.sep.join([yoloModelPath, "yolov3.weights"])
		configPath = os.path.sep.join([yoloModelPath, "yolov3.cfg"])

		print("[INFO] loading YOLO from disk...")
		net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

		vs = cv2.VideoCapture(args["input"])
		writer = None
		(W, H) = (None, None)

		try:
			prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
				else cv2.CAP_PROP_FRAME_COUNT
			total = int(vs.get(prop))
			print("[INFO] {} total frames in video".format(total))

		except:
			print("[INFO] could not determine # of frames in video")
			print("[INFO] no approx. completion time can be provided")
			total = -1

		win_started = False

		while True:
			grabbed, frame = vs.read()

			if not grabbed:
				break

			if W is None or H is None:
				(H, W) = frame.shape[:2]

			blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
				swapRB=True, crop=False)
			net.setInput(blob)
			start = time.time()
			layerOutputs = net.forward(ln)
			end = time.time()

			boxes = []
			confidences = []
			classIDs = []

			for output in layerOutputs:
				for detection in output:
					scores = detection[5:]
					classID = np.argmax(scores)
					confidence = scores[classID]

					if confidence > gui_confidence:
						box = detection[0:4] * np.array([W, H, W, H])
						(centerX, centerY, width, height) = box.astype("int")

						x = int(centerX - (width / 2))
						y = int(centerY - (height / 2))

						boxes.append([x, y, int(width), int(height)])
						confidences.append(float(confidence))
						classIDs.append(classID)

			idxs = cv2.dnn.NMSBoxes(boxes, confidences, gui_confidence, gui_threshold)

			if len(idxs) > 0:
				for i in idxs.flatten():
					(x, y) = (boxes[i][0], boxes[i][1])
					(w, h) = (boxes[i][2], boxes[i][3])

					color = [int(c) for c in COLORS[classIDs[i]]]
					cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
					text = "{}: {:.4f}".format(LABELS[classIDs[i]],
						confidences[i])
					cv2.putText(frame, text, (x, y - 5),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
			if write_to_disk:
				if writer is None:
					fourcc = cv2.VideoWriter_fourcc(*"MJPG")
					writer = cv2.VideoWriter(args["output"], fourcc, 30,
						(frame.shape[1], frame.shape[0]), True)

					if total > 0:
						elap = (end - start)
						print("[INFO] single frame took {:.4f} seconds".format(elap))
						print("[INFO] estimated total time to finish: {:.4f}".format(
							elap * total))

				writer.write(frame)
			imgbytes = cv2.imencode('.png', frame)[1].tobytes()  

			if not win_started:
				win_started = True
				layout = [
					[sg.Text('Labelled Video', size=(30,1))],
					[sg.Image(data=imgbytes, key='_IMAGE_')],
					[sg.Text('Confidence'),
					sg.Slider(range=(0, 10), orientation='h', resolution=1, default_value=5, size=(15, 15), key='confidence'),
					sg.Text('Threshold'),
					sg.Slider(range=(0, 10), orientation='h', resolution=1, default_value=3, size=(15, 15), key='threshold')],
					[sg.Exit(size=(50, 30))]
				]
				win = sg.Window('Object Detection Output',
								default_element_size=(14, 1),
								text_justification='right',
								auto_size_text=False).Layout(layout).Finalize()
				image_elem = win.FindElement('_IMAGE_')
			else:
				image_elem.Update(data=imgbytes)

			event, values = win.Read(timeout=0)
			if event is None or event == 'Exit':
				break
			gui_confidence = values['confidence']/10
			gui_threshold = values['threshold']/10


win.Close()

print("[INFO] cleaning up...")
writer.release() if writer is not None else None
vs.release()