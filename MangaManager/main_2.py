import tkinter
from tkinter import Frame, Button
from tkinter.filedialog import askopenfiles

from src.Common.loadedcomicinfo import LoadedComicInfo
from src.MetadataManager.GUI.widgets import ScrolledFrameWidget

selected_frames = []

class ComicFrame(Frame):
    def __init__(self, parent, loaded_cinfo):
        super().__init__(parent)
        # frame = Frame(self)
        # frame.pack()
        self.loaded_cinfo = loaded_cinfo
        self.configure(highlightthickness=6,highlightcolor="grey",highlightbackground="grey")
        # create the first canvas
        frame = self.canvas1_frame = Frame(self, background="grey", highlightcolor="grey",highlightthickness=6)
        frame.pack(side="left")
        canvas1 = self.canvas1 = tk.Canvas(frame)
        canvas1.configure(height='260', width='190')
        canvas1.pack(side="top", expand=False,anchor=tk.CENTER)
        # print the image in the first canvas
        canvas1.create_image(0, 0, image=loaded_cinfo.cached_image, anchor="nw")
        self.print_canvas(frame, loaded_cinfo, "front")

        # create the second canvas
        frame =self.canvas2_frame= Frame(self, background="grey", highlightcolor="grey",highlightthickness=6)
        frame.pack(side="right")
        canvas2 = self.canvas2 = tk.Canvas(frame)
        canvas2.configure(height='260', width='190')
        canvas2.pack(side="top", expand=False,anchor=tk.CENTER)
        # print the image in the second canvas
        canvas2.create_image(0, 0, image=loaded_cinfo.cached_image_last, anchor="nw")
        self.print_canvas(frame, loaded_cinfo, "back")

        # bind the click event to the on_clicked_canvas method
    def on_button_click(self,mode,loaded_cinfo:LoadedComicInfo, front_or_back):
        print("Clicked button.")
        print(f"Is: {front_or_back}")
        print(f"Path: {loaded_cinfo.file_path}")


    def print_canvas(self, frame, loaded_cinfo, front_or_back):
        if front_or_back not in ("front", "back"):
            return
        frame_buttons = self.frame_buttons = Frame(frame)
        frame_buttons.pack(side="bottom", anchor=tk.CENTER,fill="x")
        Button(frame_buttons, text="✎",
               command=lambda item=loaded_cinfo, fb=front_or_back:
               self.on_button_click("edit", loaded_cinfo=item, front_or_back=fb)).pack(side="left",fill="x", expand=True)
        Button(frame_buttons, text="🗑",
               command=lambda item=loaded_cinfo, fb=front_or_back:
               self.on_button_click("delete", loaded_cinfo=item, front_or_back=fb)).pack(side="left",fill="x", expand=True)
        Button(frame_buttons, text="➕",
               command=lambda item=loaded_cinfo, fb=front_or_back:
               self.on_button_click("append", loaded_cinfo=item, front_or_back=fb)).pack(side="left",fill="x", expand=True)


import tkinter as tk

class TopFrame(tk.Toplevel):
    def select_frame(self,event, frame: tkinter.Frame):
        # check if shift is being held
        if event.state & 0x0001:
            # if shift is being held, add the selected frame to the list of selected frames
            if len(self.selected_frames) > 0:
                # get the index of the last selected frame
                last_selected_index = self.scrolled_widget.grid_slaves().index(self.selected_frames[-1])
                # get the index of the current frame
                current_frame_index = self.scrolled_widget.grid_slaves().index(frame)

                # if the current frame is after the last selected frame
                if current_frame_index > last_selected_index:
                    # add all frames between the last selected frame and the current frame to the list of selected frames
                    for i in range(last_selected_index + 1, current_frame_index):
                        self.selected_frames.append(self.scrolled_widget.grid_slaves()[i])
                else:
                    # add all frames between the current frame and the last selected frame to the list of selected frames
                    for i in range(current_frame_index, last_selected_index):
                        self.selected_frames.append(self.scrolled_widget.grid_slaves()[i])
        else:
            # if shift is not being held, clear the list of selected frames and add the selected frame
            self.selected_frames.clear()
            self.selected_frames.append(frame)
        for frame in self.scrolled_widget.grid_slaves():
            if frame in self.selected_frames:
                print("green" if frame in self.selected_frames else "gray")
                frame.canvas1_frame.configure(highlightbackground="green", highlightcolor="green")
                frame.canvas2_frame.configure(highlightbackground="green", highlightcolor="green")
                frame.configure(highlightbackground="green", highlightcolor="green")
                frame.frame_buttons.configure(background="green")
            else:
                frame.canvas1_frame.configure(highlightbackground="grey", highlightcolor="grey")
                frame.canvas2_frame.configure(highlightbackground="grey", highlightcolor="grey")
                frame.configure(highlightbackground="grey", highlightcolor="grey")
                frame.frame_buttons.configure(background="grey")
    # def on_frame_click(self,event):
    #     # Check if the shift key is pressed
    #     shift_pressed = (event.state & 0x1) != 0
    #
    #     # If the shift key is pressed, add all the frames between the
    #     # previously selected frame and the current one to the list
    #     if shift_pressed:
    #         start_index = frames.index(self.selected_frames[-1])
    #         end_index = frames.index(event)
    #         self.selected_frames.extend(frames[min(start_index, end_index):max(start_index, end_index)])
    #     else:
    #         self.selected_frames.clear()
    #         self.selected_frames.append(event)
    #         # Code to clear the list and add the current frame goes here
    #
    #     # Update the background color of the selected frames to indicate that they are selected
    #     for f in frames:
    #         if f in selected_frames:
    #             f.configure(bg='green')
    #         else:
    #             f.configure(bg='white')
    #
    #     print(selected_frames)
    def __init__(self, parent, loaded_cinfo_list):
        super().__init__(parent)
        self.geometry("800x400")
        scrolled_widget = self.scrolled_widget = ScrolledFrameWidget(self).create_frame()
        self.loaded_cinfo_list = loaded_cinfo_list
        self.selected_frames = []
        # iterate over the LoadedComicInfo objects in loaded_cinfo_list

        for i, cinfo in enumerate(loaded_cinfo_list):

            # create a ComicFrame for each LoadedComicInfo object
            comic_frame = ComicFrame(scrolled_widget, cinfo)

            frames.append(comic_frame)
            comic_frame.grid(row=i // 3, column=i % 3,padx=20,pady=20)
            comic_frame.bind("<Button-1>", lambda event, frame=comic_frame: self.select_frame(event, frame))
            comic_frame.canvas1.bind("<Button-1>", lambda event, frame=comic_frame: self.select_frame(event, frame))
            comic_frame.canvas2.bind("<Button-1>", lambda event, frame=comic_frame: self.select_frame(event, frame))
            # comic_frame.pack()

    def redraw_frames(self):
        childrens = self.winfo_children()
        for child in childrens:
            child.grid_forget()
        for i, frame in enumerate(childrens):
            frame.grid(row=i // 3, column=i % 3)
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        files = askopenfiles()
        self.loaded_cinfo_list: list[LoadedComicInfo] = []
        for file in files:
            loaded_cinfo = LoadedComicInfo(path=file.name)
            loaded_cinfo.load_all()
            self.loaded_cinfo_list.append(loaded_cinfo)



        TopFrame(self, self.loaded_cinfo_list)
frames = []

a = App()
# a.mainloop()
import tkinter as tk

# Create the main window
root = tk.Tk()



# Start the main event loop
root.mainloop()

