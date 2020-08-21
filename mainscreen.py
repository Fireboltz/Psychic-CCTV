import PySimpleGUIQt as sg
import os
def create_main_window():

    sg.theme('SandyBeach')   
    layout = [[sg.Text('Upload your video Here')],
            [sg.Input(key='-FILE-',visible=False,enable_events=True),sg.FileBrowse()],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20))],
            [sg.Button('Analysis',enable_events=True),],
            [sg.Button('Exit')]]

    return(sg.Window('Smart CCTV', layout,size=(100,140),auto_size_buttons=True,))

def main():
    window = None
    while True:
        if window is None:
            window = create_main_window()

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Analysis':
            if values["-FILE-"] is None:
                print("No file choosen")
            else:
                print("Well done son")
                print(os.system("python3 yolov5/detect.py --weights yolov5s.pt --source " + values["-FILE-"]))

    window.close()

main()