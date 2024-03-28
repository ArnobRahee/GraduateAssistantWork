import requests
from datetime import datetime, timedelta

def check_claim_truthfulness(query, api_key):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": query,
        "key": api_key,
        "languageCode": "en"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('claims', [])
        if not results:
            print("The following is not claimed by trusted sources be careful with this news.")
            return

        # Calculate the date 15 months ago
        fifteen_months_ago = datetime.now() - timedelta(days=15*30)

        # Filter claims within the last 15 months
       # Filter claims within the last 15 months
        recent_claims = [claim for claim in results if datetime.strptime(claim.get('claimDate', '1970-01-01T00:00:00Z'), '%Y-%m-%dT%H:%M:%SZ') > fifteen_months_ago]


        print(f"Number of new claims in the last 15 months: {len(recent_claims)}")

        for claim in recent_claims:
            print("\nClaim:", claim.get('text'))
            print("Claimant:", claim.get('claimant'))
            print("Claim Date:", claim.get('claimDate'))
            for review in claim.get('claimReview', []):
                publisher = review.get('publisher', {}).get('name', 'Unknown publisher')
                review_date = review.get('reviewDate', 'Unknown date')
                rating = review.get('textualRating', 'No rating provided')
                print(f"Reviewed by: {publisher} on {review_date}, Rating: {rating}")
    else:
        print("Failed to fetch fact checks:", response.status_code)

# Replace YOUR_API_KEY with your actual Google Fact Check Tools API key
api_key = "AIzaSyBnD_PD6Q6zs3aZuBBUONA0SQQp7K9j4Qc"
# Replace this with the claim you want to check
query = "Tipu Sultan"
check_claim_truthfulness(query, api_key)
