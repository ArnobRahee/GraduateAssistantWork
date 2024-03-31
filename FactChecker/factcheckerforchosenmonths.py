import requests
from datetime import datetime, timedelta

def check_claim_truthfulness(query, api_key):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    page_token = None
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15*30)  # Approximate 15 months back

    while True:
        params = {
            "query": query,
            "key": api_key,
            "languageCode": "en",
            "pageSize": 10  # Adjust based on API's max pageSize if specified
        }
        if page_token:
            params['pageToken'] = page_token

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('claims', [])
            if not results:
                print("No more claims found.")
                break

            for claim in results:
                claim_date_str = claim.get('claimDate')
                claim_date = datetime.strptime(claim_date_str, "%Y-%m-%dT%H:%M:%SZ") if claim_date_str else None
                if claim_date and start_date <= claim_date <= end_date:
                    print("\nClaim:", claim.get('text'))
                    print("Claimant:", claim.get('claimant'))
                    print("Claim Date:", claim_date_str)
                    for review in claim.get('claimReview', []):
                        publisher = review.get('publisher', {}).get('name', 'Unknown publisher')
                        review_date = review.get('reviewDate', 'Unknown date')
                        rating = review.get('textualRating', 'No rating provided')
                        print(f"Reviewed by: {publisher} on {review_date}, Rating: {rating}")

            page_token = data.get('nextPageToken')
            if not page_token:
                print("End of results.")
                break
        else:
            print("Failed to fetch fact checks:", response.status_code)
            break

api_key = "AIzaSyBnD_PD6Q6zs3aZuBBUONA0SQQp7K9j4Qc"  # Replace YOUR_API_KEY with your actual Google Fact Check Tools API key
query = "Joe Biden"
check_claim_truthfulness(query, api_key)
