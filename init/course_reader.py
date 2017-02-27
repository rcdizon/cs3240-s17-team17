import csv


def load_course_database(db_name, csv_filename):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)


if __name__ == "__main__":
    load_course_database(db_name="course1", csv_filename="seas-courses-5years.csv")
