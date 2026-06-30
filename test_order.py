from sentence_transformers import SentenceTransformer

print("SentenceTransformer imported")

import pandas as pd

print("Pandas imported")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Everything works")