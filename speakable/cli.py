"""Command line interface: python3 -m speakable "some text"."""

import argparse
import sys

from speakable.normalizer import explain, normalize


def build_parser():
    parser = argparse.ArgumentParser(
        prog="speakable",
        description="Turn written text into the words a text-to-speech voice should say.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="the text to normalize (if omitted, text is read from stdin)",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="show the before and after of every step",
    )
    parser.add_argument(
        "--system",
        choices=["international", "indian"],
        default="international",
        help="number system: thousand/million/billion or thousand/lakh/crore",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.text:
        text = " ".join(args.text)
    else:
        text = sys.stdin.read().strip()

    if args.explain:
        final = text
        for name, before, after in explain(text, args.system):
            final = after
            print("[" + name + "]")
            if before == after:
                print("  (no change)")
            else:
                print("  before: " + before)
                print("  after:  " + after)
        print("")
        print("Final: " + final)
    else:
        print(normalize(text, args.system))
    return 0

