import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, render_template

# Load dataset
df = pd.read_csv(r"C:\Users\Preeti\.kaggle\laptop recommendation project\Laptop_Information.csv")

# Preprocessing: Convert relevant features to string and combine
df['Processor'] = df['Processor'].astype(str)
df['RAM'] = df['RAM'].astype(str)

# Ensure 'ImgURL' exists to avoid KeyError
if 'ImgURL' not in df.columns:
    df['ImgURL'] = "https://via.placeholder.com/150"  # Placeholder Image

df['combined_features'] = df['Company'] + ' ' + df['Processor'] + ' ' + df['RAM']

# Convert text to numerical representation
vectorizer = TfidfVectorizer(stop_words='english')
feature_matrix = vectorizer.fit_transform(df['combined_features'])

# Compute similarity matrix
similarity_matrix = cosine_similarity(feature_matrix)


def recommend_laptops(laptop_name, top_n=5):
    laptop_name = laptop_name.strip().lower()  # Normalize input
    df['Model_lower'] = df['Model'].str.lower()  # Create lowercase model names

    if laptop_name not in df['Model_lower'].values:
        print(f"Laptop '{laptop_name}' not found in dataset.")  # Debugging
        return []

    idx = df[df['Model_lower'] == laptop_name].index[0]
    scores = list(enumerate(similarity_matrix[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    recommended_laptops = df.iloc[[i[0] for i in sorted_scores]][['Model', 'ImgURL']]
    print("Final Recommendations:", recommended_laptops)  # Debugging
    return recommended_laptops.to_dict(orient='records')


# Flask App
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    error_message = ""

    if request.method == 'POST':
        try:
            laptop_name = request.form.get('laptop_name')
            print("Laptop Name Entered:", laptop_name)  # Debugging

            if laptop_name and laptop_name.strip():
                recommendations = recommend_laptops(laptop_name)
                if not recommendations:
                    error_message = "No similar laptops found. Please enter a valid laptop model."
            else:
                error_message = "Please enter a laptop name."

        except Exception as e:
            error_message = "An error occurred. Please try again."
            print("Error:", e)

    return render_template('index.html', recommendations=recommendations, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)
