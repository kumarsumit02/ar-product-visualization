import csv

# Initialize an empty set to store unique objects
unique_objects = set()

# Replace 'your_csv_file.csv' with the actual path to your CSV file
csv_file_path = 'runs/detect/exp10/predictions.csv'

# Open the CSV file and read its content
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    
    # Iterate through the rows in the CSV file
    for row in csv_reader:
        # Assuming the object name is in the 2nd column (index 1)
        object_name = row[1]
        # Add the object name to the set
        unique_objects.add(object_name)

# Print the unique object names
for obj in unique_objects:
    print(obj)
