import csv
import sys
import datetime

"""
Takes in a large CSV file and splits it into several smaller files according to the set limit (see LINE_LIMIT). After reaching that many lines, a new file is created.
"""

### CONFIG ###
LINE_LIMIT = 999999 # 1000000 lines including header
NEW_FILE_DATE_PREFIX = "{}"
NEW_FILE_PART = "_part{}of{}"
NEW_FILE_FORMAT_SUFFIX = ".csv"
##############

parts_total = 1
parts_index = 0
date = datetime.datetime.now().strftime("%y-%m-%d")

def rename_files(parts_index, parts_total):
    name = NEW_FILE_DATE_PREFIX.format(date)
    if parts_total > 1:
        name += NEW_FILE_PART.format(parts_index, parts_total)
    name += NEW_FILE_FORMAT_SUFFIX

    return name

def write_csv(data, path):
    with open(path, "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

def recycle_part(part, header):
    part.clear()
    part.append(header)
    return part

files = []
file_part = []

if (len(sys.argv) == 1):
    print("\nPlease use the originial csv file name as the argument for this script.\n")
    quit()
else:
    original_file_name = sys.argv[1]

print("Reading source file: " + original_file_name, end="... ")
with open(original_file_name, "r", encoding="utf-8") as csvFile:
    reader = csv.reader(csvFile)


    line_count = 0 # to compare against LINE_LIMIT
    for row in reader:
        # save header line to prepend to new file parts
        if reader.line_num == 1:
            header = row

        file_part.append(row)

        if line_count == LINE_LIMIT:
            files.append(file_part.copy())
            file_part = recycle_part(file_part, header)
            line_count = 0

        line_count += 1

    files.append(file_part.copy())
    print("Done.")

part_count = 1
for part in files:
    filename = rename_files(part_count, len(files))
    print("Writing: " + filename, end="... ")
    write_csv(part, filename)
    print("Done.")

    part_count += 1
print("Finished!")
