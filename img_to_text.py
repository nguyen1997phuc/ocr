import datetime
import logging
import os

import click
import cv2
import numpy as np
import pytesseract
from PIL import Image

DEFAULT_IMG = '/home/nguyen.hong.phucb/Desktop/ocr/ocr/data/test1.png'
src_path = "/home/nguyen.hong.phucb/Desktop/ocr/ocr/data/"
BASIC_CONFIG_LOG = {
    'filename': 'ocr.log',
    'encoding': 'utf-8',
    'level': logging.DEBUG,
}

VALID_EXTEND_FILE = ['.PNG', '.PDF']

logging.basicConfig(
    filename=BASIC_CONFIG_LOG.get('filename'),
    level=BASIC_CONFIG_LOG.get('level')
)


def read_image_with_opencv(image_directory):
    img = cv2.imread(image_directory)
    if not img:
        logging.error('OpenCV can not read a file, maybe it is not a image')
        raise Exception
    return img


def read_image_with_pil(image_directory):
    try:
        img = Image.open(image_directory)
        return img
    except IOError:
        logging.error('PIL can not read a file, maybe it is not a image')
        raise IOError


def validate_file(image_directory):
    logging.info(f'start validate input')

    def _validate_file_exist():
        if not os.path.isfile(image_directory) or not os.access(image_directory, os.R_OK):
            logging.error('file not exists or not readable')
            raise Exception

    def _validate_file_extension():
        _, file_extension = os.path.splitext(image_directory)
        if file_extension.upper() in VALID_EXTEND_FILE:
            logging.info(f'end validate input')
            return file_extension

        logging.error(f'only allow file extend: {VALID_EXTEND_FILE}')
        raise Exception

    _validate_file_exist()
    _validate_file_extension()
    return


def recognize_text_with_tesseract(image_directory):
    try:
        logging.info(f'start recognize text with tesseract')

        # read image and convert it to gray
        img = read_image_with_opencv(image_directory)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # remove noise in image
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        cv2.erode(img, kernel, iterations=1)

        # detect text in image
        image_detect = read_image_with_pil(src_path + "removed_noise.png")
        result = pytesseract.image_to_string(image_detect)

        logging.info(f'end recognize text with tesseract')
        return result
    except Exception as e:
        logging.error(e)



def convert_pdf_to_img():
    pass


@click.command()
@click.option('--image_directory', default=DEFAULT_IMG, help='directory of image')
def get_string(image_directory):
    """Detect text in image"""
    try:
        logging.info(f'start time: {datetime.datetime.now()}')
        logging.info(f'recevice file: {image_directory}')

        type_file = validate_file(image_directory)
        if type_file == VALID_EXTEND_FILE[1]:
            image_directory = convert_pdf_to_img()

        text = recognize_text_with_tesseract(image_directory)
        print(text)
    except Exception as e:
        logging.error(e)
    finally:
        logging.info(f'end time: {datetime.datetime.now()}')


if __name__ == '__main__':
    get_string()
