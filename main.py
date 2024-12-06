from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load the dataset (Adjust the path to your dataset)
DATASET_PATH = "sentiment.csv"
try:
    reviews = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Dataset not found at path: {DATASET_PATH}")

# Ensure the dataset has the necessary 'Review' column
if 'Review' not in reviews.columns:
    raise RuntimeError("The dataset must contain a 'Review' column.")

# Define positive and negative words
positive_words = {
    "amazing", "exceptional", "fantastic", "loved", "great", "recommended", 
    "learned", "insightful", "attend", "speakers", "good", "excellent", 
    "enjoyed", "well", "informative", "interesting", "useful", "helpful", 
    "best", "awesome", "brilliant", "fabulous", "outstanding", "superb", 
    "wonderful", "perfect", "love", "like", "nice", "happy", "exciting", 
    "fun", "positive", "satisfied", "recommend", "inspiring", "motivating", 
    "impressed", "beneficial", "valuable", "productive", "effective", 
    "successful", "satisfactory", "pleased", "glad", "comfortable", 
    "confident", "relaxed", "easy", "smooth", "quick", "clear", "helpful"
}
negative_words = {
    "not", "bad", "average", "could", "better", "worth", "improve", 
    "disappointed", "waste", "poor"
}

# Function to calculate sentiment for a single review
def analyze_sentiment(review):
    review_words = review.lower().split()
    positive_score = sum(1 for word in review_words if word in positive_words)
    negative_score = sum(1 for word in review_words if word in negative_words)
    sentiment_score = positive_score - negative_score
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

# Define the request model
class SentimentRequest(BaseModel):
    reviews: list[str]

# Define the API endpoint for sentiment analysis
@app.post("/sentiment-analysis")
async def sentiment_analysis(request: SentimentRequest):
    results = []
    for review in request.reviews:
        sentiment = analyze_sentiment(review)
        results.append({"review": review, "sentiment": sentiment})
    return {"results": results}
