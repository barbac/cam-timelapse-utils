import sys
import os
from datetime import datetime
import pytz
import tzlocal
import cv2
import numpy as np


SKIP_FRAME_THRESHOLD = 0.0008
OUTPUT_QUALITY = 80


def date_string(timestamp):
    return (
        datetime.utcfromtimestamp(timestamp)
        .replace(tzinfo=pytz.utc)
        .astimezone(tzlocal.get_localzone())
        .strftime("%a %d %b %Y  %I:%M:%S %p")
    )


def main(input_dir, output_dir=None):
    image_files = os.listdir(input_dir)
    image_files.sort()
    if output_dir and not os.path.exists(output_dir):
        os.mkdir(output_dir)

    image_a = None
    gray_a = None
    array_size = 0
    frames_count = 0

    for i, image_file in enumerate(image_files):
        print(image_file)

        image_b = cv2.imread(os.path.join(input_dir, image_file))
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.GaussianBlur(gray_b, (21, 21), 0)
        if image_a is None:
            image_a = image_b
            gray_a = gray_b
            array_size = gray_a.size
            print("gray size", array_size, gray_a.shape)
            continue

        frame_delta = cv2.absdiff(gray_a, gray_b)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # frame = cv2.add(gray_a, thresh)
        frame = image_b

        # prepare for next frame
        image_a = image_b
        gray_a = gray_b

        non_zeros = np.count_nonzero(thresh)
        # should look for clusters of changes instead of the whole image.
        if non_zeros / array_size < SKIP_FRAME_THRESHOLD:
            continue

        frames_count += 1

        timestamp = int(image_file[:-4])  # remove .jpg
        time_string = f"{date_string(timestamp)} {array_size} {non_zeros} {non_zeros / array_size} {i} {frames_count}"
        print(time_string)
        x = 70
        y = 50
        thickness = 2
        # black border
        cv2.putText(
            frame,
            time_string,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            thickness + 1,
        )
        # white text
        cv2.putText(
            frame,
            time_string,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            thickness,
        )

        if output_dir:
            cv2.imwrite(
                f"{output_dir}/{timestamp}.webp",
                frame,
                [cv2.IMWRITE_WEBP_QUALITY, OUTPUT_QUALITY],
            )
        else:
            cv2.imshow("image", frame)
            while True:
                key = cv2.waitKey(0)
                q_key = 113
                if key == q_key:
                    cv2.destroyAllWindows()
                    return
                else:
                    # go to next image
                    break
    cv2.destroyAllWindows()
    print(len(image_files), frames_count)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        _, input_dir, output_dir = sys.argv
        main(input_dir, output_dir)
    elif len(sys.argv) == 2:
        _, input_dir = sys.argv
        main(input_dir)
    else:
        print("usage: skipper input_dir [output_dir]")
