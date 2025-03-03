import pandas as pd
df = pd.read_csv(r"C:\Users\Preeti\.kaggle\laptop recommendation project\Laptop_Information.csv")
print(df.columns)

print(df['Model'].isnull().sum())
