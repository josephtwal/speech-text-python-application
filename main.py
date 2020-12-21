import tkinter as tk
from keyword_spotting_service import Keyword_Spotting_Service
import pdfkit
import sys
import os
import datetime
from os import path
from tkinter import filedialog
from tkinter import messagebox



class MainWindow:
    """ GUI Wrapper """

    # configure root directory path relative to this file
    THIS_FOLDER_G = ""
    if getattr(sys, "frozen", False):
        # frozen
        THIS_FOLDER_G = os.path.dirname(sys.executable)
    else:
        # unfrozen
        THIS_FOLDER_G = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, root):
        self.root = root
        self._pdf = None
        self._file_url = tk.StringVar()
        self._Dist_url = tk.StringVar()
        self._status = tk.StringVar()
        self._status.set("---")


        root.title("Voice2Text")
        root.configure(bg="#eeeeee")

        try:
            icon_img = tk.Image(
                "photo",
                file=self.THIS_FOLDER_G + "/assets/icon.png"
            )
            root.call(
                "wm",
                "iconphoto",
                root._w,
                icon_img
            )
        except Exception:
            pass

        self.menu_bar = tk.Menu(
            root,
            bg="#eeeeee",
            relief=tk.FLAT
        )
        self.menu_bar.add_command(
            label="How To",
            command=self.show_help_callback
        )
        self.menu_bar.add_command(
            label="Quit!",
            command=root.quit
        )

        root.configure(
            menu=self.menu_bar
        )

        self.file_entry_label = tk.Label(
            root,
            text="Enter Audio File Path Or Click SELECT FILE Button",
            bg="#eeeeee",
            anchor=tk.W
        )
        self.file_entry_label.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=0,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.file_entry = tk.Entry(
            root,
            textvariable=self._file_url,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT
        )
        self.file_entry.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=8,
            row=1,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.select_btn = tk.Button(
            root,
            text="SELECT FILE",
            command=self.selectfile_callback,
            width=42,
            bg="#1089ff",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.select_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=2,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.Dist_entry_label = tk.Label(
            root,
            text="Enter destination directory Path Or Click SELECT Directory Button",
            bg="#eeeeee",
            anchor=tk.W
        )
        self.Dist_entry_label.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=3,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.Dist_entry = tk.Entry(
            root,
            textvariable=self._Dist_url,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT
        )
        self.Dist_entry.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=8,
            row=4,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.Dist_btn = tk.Button(
            root,
            text="SELECT Directory",
            command=self.selectdist_callback,
            width=42,
            bg="#1089ff",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.Dist_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=5,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.convert_btn = tk.Button(
            root,
            text="Convert",
            command=self.convert_callback,
            bg="#00bd56",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.convert_btn.grid(
            padx=15,
            pady=(4, 12),
            ipadx=24,
            ipady=6,
            row=7,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )
        self.reset_btn = tk.Button(
            root,
            text="RESET",
            command=self.reset_callback,
            bg="#aaaaaa",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.reset_btn.grid(
            padx=15,
            pady=(4, 12),
            ipadx=24,
            ipady=6,
            row=8,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        self.status_label = tk.Label(
            root,
            textvariable=self._status,
            bg="#eeeeee",
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.FLAT,
            wraplength=350
        )
        self.status_label.grid(
            padx=12,
            pady=(0, 12),
            ipadx=0,
            ipady=1,
            row=9,
            column=0,
            columnspan=4,
            sticky=tk.W + tk.E + tk.N + tk.S
        )

        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 1, weight=1)
        tk.Grid.columnconfigure(root, 2, weight=1)
        tk.Grid.columnconfigure(root, 3, weight=1)

    def selectfile_callback(self):
        try:
            name = filedialog.askopenfile(title='Please select audio file',
                                          filetypes=[('Audio Files', ['.wav'])])
            self._file_url.set(name.name)
            # print(name.name)
        except Exception as e:
            self._status.set(e)
            self.status_label.update()

    def selectdist_callback(self):
        try:
            name = filedialog.askdirectory(title='Please select Destination Directory', )
            self._Dist_url.set(name)
            # print(name.name)
        except Exception as e:
            self._status.set(e)
            self.status_label.update()

    def freeze_controls(self):
        self.file_entry.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.Dist_btn.configure(state="disabled")
        self.convert_btn.configure(state="disabled")
        self.reset_btn.configure(state="disabled")

        self.status_label.update()

    def unfreeze_controls(self):
        self.file_entry.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.Dist_btn.configure(state="normal")
        self.convert_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")
        self.status_label.update()


    def reset_callback(self):
        self._pdf = None
        self._file_url.set("")
        self._Dist_url.set("")
        self._status.set("---")

    def convert_callback(self):
        if not self._file_url.get():
            self._status.set("please choose audio file")
        elif not self._Dist_url.get():
            self._status.set("please choose Destination directory")
        else:
            self._status.set("processing")
            self.freeze_controls()
            AUDIO_FILE = self._file_url.get()
            filename = "game_log_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
            destination = self._Dist_url.get()
            kss = Keyword_Spotting_Service()
            self._pdf = pdfkit.from_string("prediction is: " + kss.predict(AUDIO_FILE),
                                               path.join(destination, filename))
            self._status.set("Log file generated!")
            self.unfreeze_controls()

    def show_help_callback(self):
        messagebox.showinfo(
            "How To",
            """1. Open the App and Click SELECT FILE Button and select your file e.g. "abc.wav".
2. Select where output file should be generated.
3. Click Convert Button to Start the converting. A new PDF file named "match_log_datetime.pdf" will be created in the selected directory.
5. Click RESET Button to reset the input fields and status bar."""
        )


if __name__ == "__main__":
    ROOT = tk.Tk()
    MAIN_WINDOW = MainWindow(ROOT)
    ROOT.mainloop()
