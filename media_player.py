import PySimpleGUIQt as sg
import pyaudio
import wave
import time
from pynput import keyboard
import os


def MediaPlayerGUI():
    background = '#F0F0F0'
    paused = False    
    song_index = 0
    defino = 0
    song_list = os.listdir(os.getcwd() + '/output/sound/')
    layout= [[sg.Text('Media File player',size=(17,3), font=("Helvetica", 17),justification='c')],
             [sg.Text(size=(25, 2),font=("Helvetica", 20), key='output',justification='c'),],
             [sg.Button('Previous',size=(100, 30), key='previous'),
              sg.Button('Play',size=(100,30), key='Pause'),
              sg.Button('Next',size=(100,30),key='Next'),],
            ]

    # Open a form, note that context manager can't be used generally speaking for async forms
    window = sg.Window('Media Players', layout,
                       font=("Helvetica", 10),element_justification='c')
    # Our event loop
    wf = wave.open(os.getcwd()+'/output/sound/'+song_list[song_index], 'rb')
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    def on_press(key):
        print (key)
        if key == keyboard.Key.space:
            if stream.is_stopped():     # time to play audio
                print ('play pressed')
                stream.start_stream()
                paused = False
                return False
            elif stream.is_active():   # time to pause audio
                print ('pause pressed')
                stream.stop_stream()
                paused = True
                return False
        return False

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
    while(True):
        event, values = window.read()     
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif event == 'pause':
            while stream.is_active() or paused==True:
                with keyboard.Listener(on_press=on_press) as listener:
                    listener.join()
                time.sleep(0.2)
        elif event == 'Next':
            song_index +=1
            if song_index < len(song_list):
                stream.stop_stream()
                stream.close()
                wf.close()
                p.terminate()
                wf = wave.open(os.getcwd()+'/output/sound/'+song_list[song_index], 'rb')
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
            else:
                song_index-=1
                print("[Info] Song index out of bound max")

        elif event == 'previous':
            song_index -=1
            if song_index > 0:
                stream.stop_stream()
                stream.close()
                wf.close()
                p.terminate()
                wf = wave.open(os.getcwd()+'/output/sound/'+song_list[song_index], 'rb')
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
            else:
                song_index+=1
                print("[Info] Song index out of bound min")

        # If a button was pressed, display it on the GUI by updating the text element
        if event != sg.TIMEOUT_KEY:
            window['output'].update(song_list[song_index])