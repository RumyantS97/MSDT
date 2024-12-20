import argparse
import imageprocessor as ip
from logger_config import main_logger

def parser() -> tuple[str, float, float, str]:
    """
    Parses the image filename, height and width of the image, and the name of the directory
    where the modified image will be saved.
    :return: The tuple of parsed data.
    """
    main_logger.info("Parsing command-line arguments.")
    some_parser = argparse.ArgumentParser()
    some_parser.add_argument('input_name', type=str, help='Input image filename.')
    some_parser.add_argument('height', type=int, help='Height of the resized image.')
    some_parser.add_argument('width', type=int, help='Width of the resized image.')
    some_parser.add_argument('output_name', type=str, help='Output image filename.')
    args = some_parser.parse_args()
    main_logger.info("Arguments parsed: input_name=%s, height=%d, width=%d, output_name=%s",
                     args.input_name, args.height, args.width, args.output_name)
    return args.input_name, args.height, args.width, args.output_name

def main() -> None:
    """
    Main function to handle the image processing flow:
    - Parses command-line arguments.
    - Loads the image.
    - Prints image information.
    - Calculates and displays the histogram.
    - Resizes the image.
    - Saves the modified image.
    """
    try:
        main_logger.info("Program started.")
        input_file, height, width, output_file = parser()

        img = ip.load_image(input_file)
        ip.print_image_info(img)

        hist = ip.calc_hist(img)
        ip.dis_hist(hist)

        resized = ip.resize(img, width, height)
        ip.display(img, resized)
        ip.save(resized, output_file)

        main_logger.info("Program finished successfully.")
    except Exception as exc:
        main_logger.error("An error occurred: %s", exc)

if __name__ == "__main__":
    main()
