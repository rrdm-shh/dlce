# Import Python standard libraries
import argparse
import csv
from tabulate import tabulate
import unicodedata

# Import MPI-SHH libraries
from segments import Profile, Tokenizer


def my_tokenizer(form, tokenizer):
    form = "^" + form + "$"
    form = unicodedata.normalize("NFC", form)

    return tokenizer(form, column="IPA")


def main(args):
    # Initiate tokenizer and profile
    profile = Profile.from_file(args.profile)
    tokenizer = Tokenizer(profile=profile)

    # Open file and check items
    errors = []
    with open(args.wordlist) as handler:
        reader = csv.DictReader(handler, delimiter="\t")
        for count, row in enumerate(reader):
            segments = my_tokenizer(row[args.form], tokenizer)
            reference = row[args.segments]
            if segments != reference:
                errors.append([row["ID"], row[args.form], segments, reference])

            if args.l:
                if count > args.l:
                    break

    # Output
    print(tabulate(errors, headers=["ID", "Form", "Result", "Reference"]))
    print(
        "Errors: %i/%i (%.2f%%)"
        % (len(errors), count + 1, (len(errors) / (count + 1)) * 100)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build dataset.")
    parser.add_argument(
        "wordlist",
        type=str,
        help="Orthographic profile file (default: `orthography.tsv`).",
    )
    parser.add_argument(
        "-l",
        type=int,
        help="Instructs the script to consider only the top `l` lines (default: all)",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default="orthography.tsv",
        help="Orthographic profile file (default: `orthography.tsv`).",
    )
    parser.add_argument(
        "--form",
        type=str,
        default="Form",
        help="Column for the form field (default: `Form`).",
    )
    parser.add_argument(
        "--segments",
        type=str,
        default="Segments",
        help="Column for the segments field (default: `Segments`).",
    )
    ARGS = parser.parse_args()

    main(ARGS)
