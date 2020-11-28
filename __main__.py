import argparse
import pyar

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help="Files to load")
    args = parser.parse_args()
    for filename in args.files:
        with open(filename, 'rb') as f:
            for entry in pyar.load(f).entries:
                print("{} {} - {}".format(entry.name, entry.offset, entry.size))


if __name__ == "__main__":
    main()
