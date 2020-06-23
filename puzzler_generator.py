import cv2
import random

def preview_img(img):
    fraction = 0.5
    preview = cv2.resize(img, None, fx=fraction, fy=fraction)
    cv2.imshow("preview", preview)
    cv2.waitKey(0)

def save_puzzles(puzzles):
    puzzle_count = len(puzzles)
    print("Saving {} puzzles".format(puzzle_count))

    image_uid_set = set()
    for puzzle in puzzles:
        new_uid = random.randint(0,puzzle_count * 10)
        # Ensure it is unique
        while new_uid in image_uid_set:
            new_uid = random.randint(0,puzzle_count * 10)

        filename = "puzzles/Puzzle_{}.png".format(new_uid)
        image_uid_set.add(new_uid)
        cv2.imwrite(filename, puzzle)


def main():
    filename = "elly.jpg"

    img = cv2.imread(filename)
    # preview_img(img)
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    height, width, _ = img.shape
    print("Image size: {}, {}".format(width, height))
    
    # Apply grid
    grid_vert_count = 32
    grid_hori_count = 16

    puzzlesize_width = width // grid_hori_count
    puzzlesize_height = height // grid_vert_count
    print("puzzle width x height: {} x {}".format(puzzlesize_width, puzzlesize_height))

    puzzles = []
    for i in range(grid_vert_count):
        for j in range(grid_hori_count):
            y_start = i * puzzlesize_height
            y_end = (i + 1) * puzzlesize_height
            x_start = j * puzzlesize_width
            x_end = (j + 1) * puzzlesize_width
            puzzle = img[y_start:y_end, x_start:x_end]
            puzzles.append(puzzle)
            # preview_img(puzzle)

    save_puzzles(puzzles)
    # preview_img(img)

if __name__ == "__main__":
    main()
