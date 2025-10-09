import os
import pandas as pd

def save_to_csv(results, category, dir):
    df = pd.DataFrame(results)
    os.makedirs(dir, exist_ok=True) # create directory if it doesn't exist
    filepath = os.path.join(dir, f"{category}.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ Saved {category} data to {filepath}")
    