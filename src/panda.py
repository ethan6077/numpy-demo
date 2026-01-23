import pandas as pd

# ketch_raw_data = pd.read_csv("./input/2025-03-05_2_5_0.csv")
# ketch_raw_data = pd.read_csv("./input/my-items-400-20260121.csv")
# ketch_raw_data = pd.read_csv("./input/my-items-200-20260121.csv")
ketch_raw_data = pd.read_csv("./input/my-items-post-20260121.csv")

print("ketch_raw_data info: ", ketch_raw_data.info())
print("ketch_raw_data shape: ", ketch_raw_data.shape)
# print("ketch_raw_data preview: ", ketch_raw_data.head(8))

# Calculate statistics for req_length column
# print("\n=== My-Items 400 req_length Statistics ===")
# print("\n=== My-Items 200&201 req_length Statistics ===")
print("\n=== My-Items POST req_length Statistics ===")
print(f"Total records: {len(ketch_raw_data)}")
print(f"Min: {ketch_raw_data['req_length'].min()}")
print(f"Max: {ketch_raw_data['req_length'].max()}")
print(f"Mean: {round(ketch_raw_data['req_length'].mean())}")
print(f"Median: {round(ketch_raw_data['req_length'].median())}")

records_less_8000 = ketch_raw_data[ketch_raw_data["req_length"] < 8000]
records_above_equal_8000 = ketch_raw_data[ketch_raw_data["req_length"] >= 8000]

print(
    f"Records with req_length < 8K: {len(records_less_8000)}, percentage: {round((len(records_less_8000) / len(ketch_raw_data)) * 100, 2)}%"
)
print(
    f"Records with req_length >= 8K: {len(records_above_equal_8000)}, percentage: {round((len(records_above_equal_8000) / len(ketch_raw_data)) * 100, 2)}%"
)

# Count records by host
# print("\n=== Records Count by Host ===")
# print(ketch_raw_data["host"].value_counts())
# Count records by req_method
# print("\n=== Records Count by req_method ===")
# print(ketch_raw_data["req_method"].value_counts())
# Count records by req_method
# print("\n=== Records Count by req_method ===")
# print(ketch_raw_data["req_method"].value_counts())
