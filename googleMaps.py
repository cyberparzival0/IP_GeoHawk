from tkinter import *
import tkintermapview

root = Tk()
root.title('GeoHawk')
root.geometry("900x800")

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=700, corner_radius=0)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

for ipCoord in sys.argv[1:]:
    ipCoord = ipCoord.split("=")
    map_widget.set_marker(float(ipCoord[1]), float(ipCoord[2]), text=ipCoord[0])

map_widget.set_zoom(0)


map_widget.pack()

root.mainloop()
