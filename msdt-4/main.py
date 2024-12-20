import argparse

import imageprocessor as ip

def parser() -> tuple[str, float, float, str]:
    """
    Parses the image filename, height and width of the image, the name of the directory
    where the modified image will be saved.
    :return: The tuple of parsed data
    """
    some_parser = argparse.ArgumentParser()
    some_parser.add_argument('input_name', type=str, help='input_name')
    some_parser.add_argument('height', type=int, help='height')
    some_parser.add_argument('width', type=int, help='width')
    some_parser.add_argument('output_name', type=str, help='output_name')
    args = some_parser.parse_args()
    return args.input_name, args.height, args.width, args.output_name

def main() -> None:
    try:
        input_file, height, width, output_file = parser()

        img = ip.load_image(input_file)

        ip.print_image_info(img)

        hist = ip.calc_hist(img)
        ip.dis_hist(hist)

        resized = ip.resize(img, width, height)

        ip.display(img, resized)

        ip.save(resized, output_file)

    except Exception as exc:
        print("Error:", exc)

if __name__ == "__main__":
    main()