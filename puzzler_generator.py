import cv2
import numpy as np

def preview_img(img):
    fraction = 1
    preview = cv2.resize(img, None, fx=fraction, fy=fraction)
    cv2.imshow("preview", preview)
    cv2.waitKey(0)

def main():
    filename = "elly.jpg"

    img = cv2.imread(filename)
    height, width, _ = img.shape
    print("Image size: {}, {}".format(width, height))
    
    # Apply grid
    grid_vert_count = 64
    grid_hori_count = 20

    puzzlesize_width = width // grid_hori_count
    puzzlesize_height = height // grid_vert_count

    for i in range(grid_vert_count):
        for j in range(grid_hori_count):
            y_start = i * puzzlesize_height
            y_end = (i + 1) * puzzlesize_height
            x_start = j * puzzlesize_width
            x_end = (j + 1) * puzzlesize_width
            puzzle = img[y_start:y_end, x_start:x_end]
            preview_img(puzzle)

    # preview_img(img)

if __name__ == "__main__":
    main()
