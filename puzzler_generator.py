import cv2

def preview_img(img):
    fraction = 1
    preview = cv2.resize(img, None, fx=fraction, fy=fraction)
    cv2.imshow("preview", preview)
    cv2.waitKey(0)

def save_puzzles(puzzles):
    puzzle_count = len(puzzles)
    print("Saving {} puzzles".format(puzzle_count))

    for idx, puzzle in enumerate(puzzles):
        filename = "Puzzle_{}.png".format(idx)
        cv2.imwrite(filename, puzzle)


def main():
    filename = "elly.jpg"

    img = cv2.imread(filename)
    height, width, _ = img.shape
    print("Image size: {}, {}".format(width, height))
    
    # Apply grid
    grid_vert_count = 2#64
    grid_hori_count = 2#20

    puzzlesize_width = width // grid_hori_count
    puzzlesize_height = height // grid_vert_count

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
