#!/usr/bin/python3

import sys
import tkinter
import tkinter.messagebox
#import customtkinter
from tkintermapview import TkinterMapView

#customtkinter.set_appearance_mode("Dark")
#customtkinter.set_default_color_theme("dark-blue") 

class MapApp(tkinter.Tk):
    appName = "GeoHawk"
    WIDTH = 800
    HEIGHT = 1000

    def __init__(self, geoCoords, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.appName)
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')

        self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

        self.listbox_button_frame = tkinter.Frame(master=self)
        self.listbox_button_frame.grid(row=2, column=1, sticky="nsew", columnspan=2)

        self.listbox_button_frame.grid_columnconfigure(0, weight=1)

        for geoCoord in geoCoords:
            geoCoord = list(map(float, geoCoord.split(":")))
            self.map_widget.set_position(geoCoord[0], geoCoord[1])

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = MapApp(sys.argv[1:])
    app.start()
