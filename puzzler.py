# import cv2
import os 
try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk



class CanvasObject(object):
    def __init__(self, canvas, image_name, xpos, ypos):
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos
 
        self.tk_image = tk.PhotoImage(
            file="{}".format(image_name))
        self.image_obj= canvas.create_image(
            xpos, ypos, image=self.tk_image, anchor="nw")
         
        canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)
        self.move_flag = False
         
    def move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
             
            self.canvas.move(self.image_obj,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
 
    def release(self, event):
        self.move_flag = False

def extract_files_from_dir(dir_path):
    filenames = []
    if os.path.isdir(dir_path):
        for (dirpath, dirnames, dir_filenames) in os.walk(dir_path):
            filenames.extend(list(map(lambda x: dirpath + "/" + x, dir_filenames)))
            break
    return filenames

class Puzzler(tk.Frame):
    def __init__(self, master, image_size):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)
 
        self.image_width = image_size[0]
        self.image_height = image_size[1]
        self.puzzles = []

        self.canvas = tk.Canvas(self, width=self.image_width, height=self.image_height, bg='steelblue',
            highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

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
    # for filename in puzzle_filenames:
    #     puzzle = cv2.imread(filename)
    #     puzzles.append(puzzle)
    # print("{} puzzles loaded.".format(len(puzzles)))

    puzzler_frame = tk.Tk()
    puzzler_frame.title("Puzzler")
    puzzler_frame.geometry("+{}+{}".format(100, 100))
    
    puzzler = Puzzler(puzzler_frame, image_size)
    puzzler.pack(fill="both", expand=True)
    puzzler.load_puzzles(puzzle_filenames, puzzle_size)

    puzzler_frame.mainloop()

if __name__ == "__main__":
    main()
