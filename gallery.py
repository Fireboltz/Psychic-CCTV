import PySimpleGUIQt as sg
import os
from PIL import Image, ImageTk
import io                        

def displayImages():
    sg.ChangeLookAndFeel('LightGrey')

    folder = sg.popup_get_folder('Image folder to open', title='Choose Folder', default_path='')

    img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

    flist0 = os.listdir(folder)

    fnames = [f for f in flist0 if os.path.isfile(
        os.path.join(folder, f)) and f.lower().endswith(img_types)]

    num_files = len(fnames)                

    del flist0 

    def get_img_data(f, maxsize=(1200, 850), first=False):
        img = Image.open(f)
        img.thumbnail(maxsize)
        if first:                     
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return ImageTk.PhotoImage(img)

    filename = os.path.join(folder, fnames[0])  
    image_elem = sg.Image(data=get_img_data(filename, first=True))
    filename_display_elem = sg.Text(filename, size=(80, 3))
    file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))

    col = [[filename_display_elem],
        [image_elem]]

    col_files = [[sg.Text('List of images')],
                [sg.Listbox(values=fnames, change_submits=True, size=(60, 10), key='listbox')],
                [sg.Button('Next', size=(8, 1)), sg.Button('Prev', size=(8, 1)), file_num_display_elem],
                [sg.Button('Exit', size=(8, 1))]]

    layoutSavedImages = [[sg.Column(col_files), sg.Column(col)]]

    window = sg.Window('Image Browser', layoutSavedImages, return_keyboard_events=True,
                    location=(0, 0), use_default_focus=False)


    i = 0
    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            raise SystemExit()
        elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
            i += 1
            if i >= num_files:
                i -= num_files
            filename = os.path.join(folder, fnames[i])
        elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
            i -= 1
            if i < 0:
                i = num_files + i
            filename = os.path.join(folder, fnames[i])
        elif event == 'listbox':            
            f = values["listbox"][0]            
            filename = os.path.join(folder, f)  
            i = fnames.index(f)                 
        else:
            filename = os.path.join(folder, fnames[i])

        image_elem.update(data=get_img_data(filename, first=True))
        filename_display_elem.update(filename)
        file_num_display_elem.update('File {} of {}'.format(i+1, num_files))

    window.close()