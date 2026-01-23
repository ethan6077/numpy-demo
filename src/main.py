import math
import collections

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

cookie_val = (
    "reartok=ux0wKRoptqr5MZVShGmVv0A6irXvJ3ToMCg9BwHEkimy0yg1GkrZId2okb9cbzMVumerZ_ZXwvoTJD7TtqhfJbr-KSfiiLwXgAfajOV18f4TppGRmkzymJDX9wLMr3Z-nO9Rpt5T2r06Y6jMV5ArzhgD7kpNr-5ljFGqoizAABrdZoaI97Nuix_TZMZTDTn1BH0TRqPxcaNTdLRy4UXAaUZhaZxcVtD4_hOe-TyPzZlizN-WV6mz5uv6od94uQ6R9zY33Q==; locke_access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktqQXNsNkkzZ2hvRDFTTDRsZE1XSSJ9.eyJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJ2ZXJzaW9uIjoyLCJ1c2VybmFtZSI6ImZjNjlhOGY4LTg0YmItNDhhZi04MTJmLTE5YjA0NzlhZjFmNCIsImlzcyI6Imh0dHBzOi8vaWQucmVhbGVzdGF0ZS5jb20uYXUvIiwic3ViIjoiZW1haWx8NjRlNWFiMjNlNzcxMjBjMWRhNDQwOTFmIiwiYXVkIjpbImRlZmF1bHQiLCJodHRwczovL3Byb2QucmVhLWdyb3VwLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3Njg4ODYwMTEsImV4cCI6MTc2ODg4OTYxMSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBwaG9uZSBvZmZsaW5lX2FjY2VzcyIsImF6cCI6IjJmYjA2ZHFhYjk1aGNpNDZkZ2xkcGgwMzgyIn0.TxyZkJ5C3T_O1rWqwJxLk4eKp9KZdGdc33YhwnpMYZEa64jgiWO-W2BHYyiE0G0l-eF4LiDl2oZeEQfsk0TxH_FTyOJL38ryWauL9pDQBYLSdTiqfz8rkxJEhwU3rtKzD3V3crIrD8nvuWJkNh_K2Lyk4ZokxMlyDAs9Yx2JUl7wJhWiZnTvoCfaX8SHIuLOsqnInEk8dzJ_ywP13meGSrKSpob1GvXLLL1xtxCwflcP3BbFdp4GYp_wW9uyqyHIgTmCAW3oEssvCH_pAWxKL6ltygxJtocVjpfE2v5S29CwR8XgWKzptxUpbsJ-pAaKEKb7OIMXLx_in2HJ6lwVyA; reaidtok=eyJ1aWQiOiIyYzk5YjljOTU4ZmIyY2E5MDE1OTE2NmM5NDE2MDliMSIsImVtYWlsVmVyaWZpZWQiOnRydWUsImV4cGlyeU1pbGxzIjoxNzY4ODg5NjExMjMyfQ==.ckFLRm9xj7i6bpgprhrrh8PMJ9ra1a2pbRwOoIo5YrX7TnIsQ3hHAbFMEaEGoDyQ; reautok=eyJraWQiOiI1ODQzNzNlMy0xMjUxLTExZWEtYWQ3Yi00ZTAwYWMyYTA1MDUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibGlkIjoiZmM2OWE4ZjgtODRiYi00OGFmLTgxMmYtMTliMDQ3OWFmMWY0IiwiaXNzIjoiaHR0cHM6Ly93d3cucmVhbGVzdGF0ZS5jb20uYXUiLCJtZmFfZW5hYmxlZCI6ZmFsc2UsImV4cCI6MTc2ODg4OTYxMSwiaWF0IjoxNzY4ODg2MDExLCJlbWFpbCI6ImV0aGFuNjA3N0BnbWFpbC5jb20iLCJqdGkiOiJsOXdhUm5UT29KMnVPL0pvdjZUMmlacFZ5Nlk9IiwiY2lkIjoiMmM5OWI5Yzk1OGZiMmNhOTAxNTkxNjZjOTQxNjA5YjEifQ.Q38G74jUyM-H1a5jQJscPkplUb5fTtnGKSifGlkJL9K3_QRIuQcmUDZNDSQ9hngJ1go03F8fycKAoyQUmLoi4oe2uWjtXIoYJ0mHi9AWjQjli-eiAErMj46yqiqA3kytXbO_EEVVrWQK6yRWwd5h8b5GDjyl312TTonCiDbPNYR51nV4DCjGUIWbmgwul-V"
    * 5
)
print("cookie_val length: ", len(cookie_val))

byte_size_utf8 = len(cookie_val.encode("utf-8"))
print("cookie_val byte size (UTF-8): ", byte_size_utf8)

print("cookie_val:", cookie_val)
