import argparse
import shutil
import sys

import ar


def list_archive(files):
    for filename in files:
        with open(filename, 'rb') as f:
            with ar.Archive(f) as archive:
                for entry in archive:
                    #print("{} {} - {}".format(entry.name, entry.offset, entry.size))
                    print(entry.name)


def cat_archive(archive, files):
    with open(archive, 'rb') as f:
        with ar.Archive(f) as the_archive:
            for filename in files:
                shutil.copyfileobj(
                    the_archive.open(filename),
                    sys.stdout.buffer)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('files', nargs='*', help="Files to load")
    list_parser.set_defaults(action=list_archive)

    cat_parser = subparsers.add_parser("cat")
    cat_parser.add_argument('archive', help="Archive file")
    cat_parser.add_argument('files', nargs='*', help="Filenames inside archive")
    cat_parser.set_defaults(action=cat_archive)

    args = vars(parser.parse_args())
    action = args.pop('action')
    action(**args)


if __name__ == "__main__":
    main()
