import csv

def main():
    with open('regdata.csv', 'r') as csvfile:
        rdr = csv.reader(csvfile)
        for row in rdr:
            print(row)


if __name__ == '__main__':
    main()
