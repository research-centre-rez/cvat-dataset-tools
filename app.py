import argparse
import json
import logging

import imageio.v2 as imageio

import imagestuff.image_ops as imgops


def create_parser(defaults):
    parser = argparse.ArgumentParser(
        description="CLI tool to process images with inversion or thresholding."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Available commands",
    )

    parser_invert = subparsers.add_parser(
        "invert",
        help="Invert the input image.",
    )
    parser_invert.add_argument(
        "--input",
        type=str,
        help="Path to the input image.",
        required=True,
    )
    parser_invert.add_argument(
        "--output",
        type=str,
        help="Path to save the processed image.",
        required=True,
    )

    # Threshold command
    parser_threshold = subparsers.add_parser(
        "threshold",
        help="Apply thresholding to the input image.",
    )
    parser_threshold.add_argument(
        "--input",
        type=str,
        help="Path to the input image.",
        required=True,
    )
    parser_threshold.add_argument(
        "--output",
        type=str,
        help="Path to save the processed image.",
        required=True,
    )

    def_thr = defaults["default_threshold"]
    parser_threshold.add_argument(
        "--threshold",
        type=int or None,
        help=f"Threshold value (0-255). Default: {def_thr}",
        default=def_thr,
        required=False,
    )

    return parser.parse_args()


def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_config(path="config/defaults.json"):
    with open(path) as f:
        return json.load(f)


def command_invert(input_path, output_path):
    img = imageio.imread(input_path)
    inverted = imgops.invert_image(img)
    imageio.imsave(output_path, inverted)


def command_threshold(input_path, output_path, threshold):
    img = imageio.imread(input_path)
    thresholded = imgops.threshold_image(img, threshold)
    imageio.imsave(output_path, thresholded)


def main():
    defaults = load_config()
    args = create_parser(defaults)
    setup_logging(args.debug)
    logging.debug(f"Parsed arguments: {args}")

    if args.command == "invert":
        logging.info("Processing image inversion...")
        command_invert(args.input, args.output)
    elif args.command == "threshold":
        logging.info("Processing image thresholding...")
        command_threshold(args.input, args.output, args.threshold)


if __name__ == "__main__":
    main()
