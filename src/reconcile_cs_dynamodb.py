import pandas as pd

KEY_COLUMN = "my_rea_id"

# ketch_raw_data = pd.read_csv("./input/2025-03-05_2_5_0.csv")
# ketch_raw_data = pd.read_csv("./input/my-items-400-20260121.csv")
# ketch_raw_data = pd.read_csv("./input/my-items-200-20260121.csv")
# ketch_raw_data = pd.read_csv("./input/my-items-post-20260121.csv")
raw_data_cs = pd.read_csv("./input/allow_suggested_disabled_20260408.csv")
raw_data_dynamodb = pd.read_csv("./input/my_rea_ids_dynamodb.csv")

# print("raw_data info: ", raw_data.info())

# print("raw_data shape: ", raw_data.shape)

print("\n raw_data_cs preview: \n", raw_data_cs.head(10))
print("\n raw_data_cs count:", len(raw_data_cs))

print("\n raw_data_dynamodb preview: \n", raw_data_dynamodb.head(10))
print("\n raw_data_dynamodb count:", len(raw_data_dynamodb))

# ==================== COMPARISON ====================
print("\n" + "=" * 60)
print("DATASET COMPARISON")
print("=" * 60)

print("\n📊 Column Information:")
print(f"  CS Dataset column: {KEY_COLUMN}")
print(f"  DynamoDB Dataset column: {KEY_COLUMN}")

cs_values = set(raw_data_cs[KEY_COLUMN].dropna())
dynamodb_values = set(raw_data_dynamodb[KEY_COLUMN].dropna())

only_in_cs = cs_values - dynamodb_values
only_in_dynamodb = dynamodb_values - cs_values
in_both = cs_values & dynamodb_values

print(f"\n🔑 Using '{KEY_COLUMN}' as comparison key")

print("\n" + "-" * 60)
print("📈 Summary Statistics:")
print(f"  Total in CS dataset:       {len(cs_values)}")
print(f"  Total in DynamoDB dataset: {len(dynamodb_values)}")
print(f"  In both datasets:          {len(in_both)}")
print(f"  Only in CS:                {len(only_in_cs)}")
print(f"  Only in DynamoDB:          {len(only_in_dynamodb)}")

print("\n" + "-" * 60)
if only_in_cs:
    print(f"\n❌ {len(only_in_cs)} items ONLY in CS dataset (first 10):")
    for i, item in enumerate(sorted(list(only_in_cs))[:10], 1):
        print(f"  {i:2d}. {item}")
    if len(only_in_cs) > 10:
        print(f"      ... and {len(only_in_cs) - 10} more")
else:
    print("\n✅ No items found only in CS dataset")

if only_in_dynamodb:
    print(f"\n❌ {len(only_in_dynamodb)} items ONLY in DynamoDB dataset (first 10):")
    for i, item in enumerate(sorted(list(only_in_dynamodb))[:10], 1):
        print(f"  {i:2d}. {item}")
    if len(only_in_dynamodb) > 10:
        print(f"      ... and {len(only_in_dynamodb) - 10} more")
else:
    print("\n✅ No items found only in DynamoDB dataset")

if in_both:
    print(f"\n✅ {len(in_both)} items found in BOTH datasets (first 5):")
    for i, item in enumerate(sorted(list(in_both))[:5], 1):
        print(f"  {i:2d}. {item}")
    if len(in_both) > 5:
        print(f"      ... and {len(in_both) - 5} more")

if only_in_cs:
    cs_only_df = raw_data_cs[raw_data_cs[KEY_COLUMN].isin(only_in_cs)]
    cs_only_df.to_csv("./output/only_in_cs.csv", index=False)
    print("\n💾 Saved items only in CS to: output/only_in_cs.csv")

if only_in_dynamodb:
    dynamodb_only_df = raw_data_dynamodb[
        raw_data_dynamodb[KEY_COLUMN].isin(only_in_dynamodb)
    ]
    dynamodb_only_df.to_csv("./output/only_in_dynamodb.csv", index=False)
    print("💾 Saved items only in DynamoDB to: output/only_in_dynamodb.csv")

print("\n" + "=" * 60)
