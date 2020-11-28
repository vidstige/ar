import argparse

import ar


def list_archive(files):
    for filename in files:
        with open(filename, 'rb') as f:
            for entry in ar.load(f).entries:
                print("{} {} - {}".format(entry.name, entry.offset, entry.size))


def cat_archive():
    pass


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('files', nargs='*', help="Files to load")
    list_parser.set_defaults(action=list_archive)

    cat_parser = subparsers.add_parser("cat")
    cat_parser.add_argument('files', nargs='*', help="Files to load")
    cat_parser.set_defaults(action=list_archive)

    args = vars(parser.parse_args())
    action = args.pop('action')
    action(**args)


if __name__ == "__main__":
    main()
