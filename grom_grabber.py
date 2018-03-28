import csv
import sys
import datetime

import requests
import bs4


def churn_through_csv(file_name, date):
    start_time = datetime.datetime.now()
    print("Started: {0}".format(str(start_time)[11:]))
    count = 0

    input_file = open(file_name, 'r')
    output_file = open('juicy-deets-{0}.csv'.format(date), 'w')
    error_file = open('whoops-{0}.csv'.format(date), 'w')

    csv_writer = csv.writer(output_file)
    csv_reader = csv.reader(input_file)
    error_writer = csv.writer(error_file)

    for line in csv_reader:
        count += 1
        ig_url = line[0]
        hash = ig_url[28:]

        r = requests.get(ig_url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        try:
            actual_image_URL = soup.find('meta',
                {'property': 'og:image'})['content']
            description = soup.find('meta',
                {'property': 'og:description'})['content']
            start = description.find('@') + 1
            end = description.find(' ', start)
            user_name = description[start:end]
            user_name = user_name.replace(')', '')
            csv_writer.writerow([hash, date, actual_image_URL, user_name])
        except:
            error_writer.writerow([ig_url, date])

    output_file.close()
    error_file.close()
    input_file.close()

    end_time = datetime.datetime.now()
    print("Ended: {0}".format(str(end_time)[11:]))
    print("Processed: {0}".format(count))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        if sys.argv[1][-3:] == 'csv':
            try:
                datetime.datetime.strptime(sys.argv[2], '%Y%m%d')
            except:
                print("Something looks awry with your date formatting..."
                    "or maybe you didn't even give me a date")
            churn_through_csv(sys.argv[1], sys.argv[2])
        else:
            print("Something looks awry with your file name")
    else:
        print("Wrong number of arguments: gimme a filename,"
            " then a date YYYYMMDD")
