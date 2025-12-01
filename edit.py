
import csv

input_file = './6000_Largest_Companies_ranked_by_Market_Cap.csv'
output_file = './6000_Largest_Companies_ranked_by_Market_Cap_NEW.csv'
field_to_remove = "Rank"
headers = []
with open(input_file, "r", newline="", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    print(reader.fieldnames)
    headers = [h for h in reader.fieldnames if h != field_to_remove]
    print(headers)
    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()
    
    for row in reader:
        row.pop(field_to_remove, None)
        writer.writerow(row)


# with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    
#     writer = csv.DictWriter(outfile, fieldnames=headers)
#     writer.writeheader()
    
    # for row in reader:
    #     row.pop(field_to_remove, None)
    #     writer.writerow(row)
