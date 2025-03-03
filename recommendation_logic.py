import pandas as pd

def get_recommendations(df, brand, processor, min_price, max_price):
    filtered_df = df.copy()

    if brand and brand != "Any":
        filtered_df = filtered_df[filtered_df['Company'].str.lower() == brand.lower()]

    if processor and processor != "Any":
        filtered_df = filtered_df[filtered_df['Processor'].str.lower().str.contains(processor.lower(), na=False)]

    filtered_df = filtered_df[(filtered_df['Price'] >= min_price) & (filtered_df['Price'] <= max_price)]

    return filtered_df.to_dict(orient='records')
