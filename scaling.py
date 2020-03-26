import cv2 as cv
from argparse import ArgumentParser
import os.path


def upscale(img, out_name):
    run = True
    rows, cols, _ = map(int, img.shape)
    img = cv.pyrUp(img, dstsize=(2 * cols, 2 * rows))
    return img, run


def downscale(img, out_name):
    run = True
    rows, cols, _ = map(int, img.shape)
    img = cv.pyrDown(img, dstsize=(cols // 2, rows // 2))
    return img, run


def close(img, out_name):
    run = False
    return img, run


def save(img, out_name):
    run = True
    f_count = 0
    while True:
        filename = '{}_{}.png'.format(out_name, f_count)
        if os.path.isfile(filename):
            f_count += 1
            continue
        cv.imwrite(filename, img)
        print('Image saved to {}'.format(filename))
        break
    return img, run


def main(img_file, out):
    img = cv.imread(img_file)
    if img is None:
        print('Image not found {}'.format(img_file))
        return

    keymap = {ord('q'): close, ord('p'): upscale, ord('o'): downscale, ord('s'): save}

    run = True
    while run:
        cv.imshow('image', img)
        key = cv.waitKey(0)
        if key in keymap:
            img, run = keymap[key](img, out)


def parse_arguments():
    desc = 'Image scaling using pyramids'
    parser = ArgumentParser(description=desc)
    parser.add_argument('-i', '--img', help='Image to up/down scale')
    parser.add_argument('-o', '--out', help='Output image base name')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.img, args.out)
