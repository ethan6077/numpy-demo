import pandas as pd
import json
import glob
import os

# Load and merge DynamoDB JSON files
json_files = glob.glob("./input/dynamodb-json-files/*.json")
print(f"Found {len(json_files)} JSON files to process")

all_records = []

for json_file in json_files:
    print(f"Processing: {os.path.basename(json_file)}")
    with open(json_file, "r") as f:
        for line in f:
            # Parse each line as JSON
            item = json.loads(line)

            # Extract data from DynamoDB format (Item.field.S)
            record = {}
            if "Item" in item:
                for key, value in item["Item"].items():
                    # DynamoDB format has type indicators (S for String, N for Number, etc.)
                    if "S" in value:
                        record[key] = value["S"]
                    elif "N" in value:
                        record[key] = value["N"]
                    else:
                        record[key] = str(value)

            all_records.append(record)

# Convert to DataFrame
merged_df = pd.DataFrame(all_records)

print(f"\nTotal records merged: {len(merged_df)}")
print(f"Columns: {list(merged_df.columns)}")
print("\nPreview of merged data:")
print(merged_df.head(10))

# Save to CSV
output_file = "./output/merged_dynamodb_data.csv"
merged_df.to_csv(output_file, index=False)
print(f"\nData saved to: {output_file}")
