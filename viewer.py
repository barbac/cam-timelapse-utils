import sys
import os
import cv2

q_KEY = 113
SPACE_KEY = 32
w_KEY = 119
a_KEY = 97
s_KEY = 115
d_KEY = 100
p_KEY = 112


def main(input_dir, image_index=0):
    image_files = os.listdir(input_dir)
    image_files.sort()
    files_total = len(image_files)
    start_interval = 100
    # interval = start_interval
    interval = 0
    print(f"Files: {files_total}.\nMins to watch: {files_total*start_interval/1000/60}")

    image_index = int(image_index)
    while True:
        image_file = image_files[image_index]
        image = cv2.imread(os.path.join(input_dir, image_file))
        print(
            f"{image_file}\t\t\tcurrent: {image_index}/{files_total}",
            end="\r",
            flush=True,
        )
        cv2.imshow("image", image)

        # while True:
        key = cv2.waitKey(interval)
        if key == q_KEY:
            cv2.destroyAllWindows()
            return
        elif key == SPACE_KEY:
            interval = 0 if interval else start_interval
        elif key == a_KEY or key == s_KEY:
            image_index = max(image_index - 1, 0)
        elif key == d_KEY or key == w_KEY:
            image_index = min(image_index + 1, files_total)  # -1
        elif key == p_KEY:
            print(f"{input_dir}/{image_file}               ")
        elif key == -1:
            image_index = min(image_index + 1, files_total)  # -1
        else:
            pass
            # print(key)
            # go to next image
            # break


from time import sleep

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])
