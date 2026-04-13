import math
import collections
import json
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from_list = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("from_list shape: ", from_list.shape)
print("from_list dtype: ", from_list.dtype)

zero_1d = np.zeros(8)
print("zero_1d: ", zero_1d)

zero_2d = np.zeros((8, 8), np.int32)
# print("zero_2d: ", zero_2d)
print("zero_2d ndim: ", zero_2d.ndim)

linear = np.linspace(0, 100, 11)
print("linear: ", linear)
# plt.plot(linear, "o")
# plt.show()

nd_arranged = np.arange(10)
print("nd_arranged: ", nd_arranged)

spaced = np.arange(0, 100, 10)
print(f"spaced: {spaced} with the size: {spaced.size}")

rand_2d = np.random.random(size=(10, 10))
# print("rand_2d: ", rand_2d)
randn_2d = np.random.randn(10, 10)
# print("randn_2d: ", randn_2d)
randint_2d = np.random.randint(0, 100, size=(10, 10))
# print("randint_2d: ", randint_2d)
# np.savetxt("./output/randint_2d.csv", randint_2d, delimiter=",", fmt="%d")
# np.savetxt("./output/randint_2d.txt", randint_2d, fmt="%d")

json_size_to_be_estimated = {
    "locke_id": "ethan-123",
    "suburbs": [
        {
            "name": "Ringwood",
            "score": 5,
            "updated_at": "2026-03-08T11:00:00",
            "agent_id": "agent_123",
            "conversation_id": "convo_123",
        },
        {
            "name": "Croydon",
            "score": 3,
            "updated_at": "2026-02-08T18:00:00",
            "conversation_id": "convo_222",
        },
    ],
    "budget": {
        "value": 900000,
        "updated_at": "2026-01-09T13:00:00",
        "conversation_id": "convo_333",
    },
    "construction_type": {
        "value": "New Home",
        "updated_at": "2026-01-09T13:00:00",
        "conversation_id": "convo_333",
    },
    "property_type": {
        "value": "house",
        "updated_at": "2026-01-09T13:00:00",
        "conversation_id": "convo_333",
    },
    "bedrooms": {
        "value": 4,
        "updated_at": "2026-01-09T13:00:00",
        "conversation_id": "convo_444",
    },
    "bathrooms": {},
    "land_size": {},
    "amenities": {},
    "other": "Looking for options in Melbourne",
}

# Print the size of json_size_to_be_estimated
print("\n" + "=" * 60)
print("JSON SIZE ANALYSIS")
print("=" * 60)

# 1. Size when serialized as JSON (with minimal whitespace)
json_string = json.dumps(json_size_to_be_estimated, separators=(",", ":"))
json_size_bytes = len(json_string.encode("utf-8"))
print(f"\n📏 JSON String Size (minified):     {json_size_bytes:,} bytes")

# 2. Size when serialized as pretty JSON
json_pretty = json.dumps(json_size_to_be_estimated, indent=2)
json_pretty_bytes = len(json_pretty.encode("utf-8"))
print(f"📏 JSON String Size (pretty):       {json_pretty_bytes:,} bytes")

# 3. Python object memory size (approximate)
python_size = sys.getsizeof(json_size_to_be_estimated)
print(f"💾 Python Object Size (shallow):   {python_size:,} bytes")


# 4. Deep size (recursively calculate all nested objects)
def get_deep_size(obj, seen=None):
    """Recursively calculate the size of an object and all its contents"""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(
            get_deep_size(k, seen) + get_deep_size(v, seen) for k, v in obj.items()
        )
    elif isinstance(obj, (list, tuple, set)):
        size += sum(get_deep_size(item, seen) for item in obj)

    return size


deep_size = get_deep_size(json_size_to_be_estimated)
print(f"💾 Python Object Size (deep):      {deep_size:,} bytes")


# 5. Structure information
def count_keys(obj):
    """Count all keys in nested dictionary"""
    count = 0
    if isinstance(obj, dict):
        count += len(obj)
        for v in obj.values():
            count += count_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            count += count_keys(item)
    return count


total_keys = count_keys(json_size_to_be_estimated)
print(f"\n🔑 Total Keys (all levels):         {total_keys}")
print(f"🔑 Top-level Keys:                  {len(json_size_to_be_estimated)}")

# 6. Show the JSON structure
print(f"\n📋 JSON Structure Preview:")
print("-" * 60)
print(json.dumps(json_size_to_be_estimated, indent=2)[:500] + "...")
print("-" * 60)

print("\n" + "=" * 60)
