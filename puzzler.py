# import cv2
import os 
try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk

MULTISELECT_ACTIVE = False

def extract_files_from_dir(dir_path):
    filenames = []
    if os.path.isdir(dir_path):
        for (dirpath, dirnames, dir_filenames) in os.walk(dir_path):
            filenames.extend(list(map(lambda x: dirpath + "/" + x, dir_filenames)))
            break
    return filenames

class CanvasObject(object):
    def __init__(self, canvas, image_name, xpos, ypos):
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos
 
        self.tk_image = tk.PhotoImage(
            file="{}".format(image_name))
        self.image_obj= canvas.create_image(
            xpos, ypos, image=self.tk_image, anchor="nw")

        canvas.tag_bind(self.image_obj, '<Button-1>', self.press)
        canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)
        self.move_flag = False
         
    def press(self, event):
        global MULTISELECT_ACTIVE
        if MULTISELECT_ACTIVE:
            return

    def move(self, event):
        global MULTISELECT_ACTIVE
        if MULTISELECT_ACTIVE:
            return

        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
             
            x_displacement = new_xpos-self.mouse_xpos
            y_displacement = new_ypos-self.mouse_ypos
            self.canvas.move(self.image_obj,
                x_displacement, y_displacement)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
            self.xpos += x_displacement
            self.ypos += y_displacement
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def move_multi(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
            
            x_displacement = new_xpos-self.mouse_xpos
            y_displacement = new_ypos-self.mouse_ypos
            self.canvas.move(self.image_obj,
                x_displacement, y_displacement)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
            self.xpos += x_displacement
            self.ypos += y_displacement
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
 
    def release(self, event):
        self.move_flag = False

class Puzzler(tk.Frame):
    def __init__(self, master, image_size):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)
 
        self.image_width = image_size[0]
        self.image_height = image_size[1]
        self.puzzles = []
        # self.grid = {} # idx: {puzzle_idx: int, position: [xpos, ypos]}

        self.selection_start = [0, 0] # [x,y]
        self.selection_min = [0, 0] # [x,y]
        self.selection_max = [0, 0] # [x,y]

        self.selected = []
        self.selection_rectangle = []

        self.canvas = tk.Canvas(self, width=self.image_width * 3, height=self.image_height, bg='steelblue',
            highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind('<Button1-Motion>', self.move_selected_puzzles)
        self.canvas.bind('<ButtonRelease-1>', self.move_selected_done)
        self.canvas.bind('<Button-3>', self.select_start)
        self.canvas.bind('<ButtonRelease-3>', self.select_done)
        self.canvas.bind('<Button3-Motion>', self.select_move)

    def __selection_rectangle(self):
        self.canvas.delete(self.selection_rectangle)
        min_x = self.selection_min[0]
        min_y = self.selection_min[1]
        max_x = self.selection_max[0]
        max_y = self.selection_max[1]
        self.selection_rectangle = self.canvas.create_rectangle(min_x, min_y, max_x, max_y)

    def move_selected_puzzles(self, event):
        global MULTISELECT_ACTIVE
        if len(self.selected) > 0:
            for puzzle in self.selected:
                puzzle.move_multi(event)

    def move_selected_done(self, event):
        global MULTISELECT_ACTIVE
        MULTISELECT_ACTIVE = False

        for puzzle in self.selected:
            puzzle.release(event)
        self.selected = []

    def select_move(self, event):
        if event.x > self.selection_start[0]:
            self.selection_max[0] = event.x
            self.selection_min[0] = self.selection_start[0]
        else:
            self.selection_min[0] = event.x
            self.selection_max[0] = self.selection_start[0]

        if event.y > self.selection_start[1]:
            self.selection_max[1] = event.y
            self.selection_min[1] = self.selection_start[1]
        else:
            self.selection_min[1] = event.y
            self.selection_max[1] = self.selection_start[1]

        self.__selection_rectangle()

        self.__find_selected()

        print("{} puzzles selected    ".format(len(self.selected)), end="\r")

    def select_start(self, event):
        global MULTISELECT_ACTIVE
        MULTISELECT_ACTIVE = True
        self.selection_start = [event.x, event.y]
        self.selection_min = [event.x, event.y]
        self.selection_max = [event.x, event.y]

    def select_done(self, event):
        global MULTISELECT_ACTIVE
        
        self.canvas.delete(self.selection_rectangle)
        if len(self.selected) == 0:
            MULTISELECT_ACTIVE = False

    def close(self):
        print("Application-Shutdown")
        self.master.destroy()

    def load_puzzles(self, puzzle_filenames, puzzle_size):
        puzzle_width = puzzle_size[0]
        puzzle_height = puzzle_size[1]
        puzzles_per_row = self.image_width // puzzle_width
        print("puzzles_per_row: {}".format(puzzles_per_row))
        for idx, filename in enumerate(puzzle_filenames):
            ypos = (idx // puzzles_per_row) * puzzle_height
            xpos = (idx % puzzles_per_row) * puzzle_width
            self.puzzles.append(CanvasObject(self.canvas, filename, xpos, ypos))

    def __find_selected(self):
        def in_selection(self, xpos, ypos):
            if xpos >= self.selection_min[0] and xpos < self.selection_max[0] and\
                ypos >= self.selection_min[1] and ypos < self.selection_max[1]:
                return True
            else:
                return False

        self.selected = []
        for puzzle in self.puzzles:
            if in_selection(self, puzzle.xpos, puzzle.ypos):
                self.selected.append(puzzle)

def main():
    dir_path = "./puzzles"
    puzzle_filenames = extract_files_from_dir(dir_path)

    # image_size = [1120, 1984]
    # puzzle_size = [560, 992] # width x height
    # 50% resize, 2x2
    # image_size = [560, 992]
    # puzzle_size = [280, 496] # width x height
    # 50% resize, 16x32
    image_size = [560, 992]
    puzzle_size = [35, 31] # width x height

    puzzles = []

    puzzler_frame = tk.Tk()
    puzzler_frame.title("Puzzler")
    puzzler_frame.geometry("+{}+{}".format(100, 100))
    
    puzzler = Puzzler(puzzler_frame, image_size)
    puzzler.pack(fill="both", expand=True)
    puzzler.load_puzzles(puzzle_filenames, puzzle_size)

    puzzler_frame.mainloop()

if __name__ == "__main__":
    main()
