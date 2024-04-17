import requests
import pandas as pd
from datetime import datetime, timedelta
from google.colab import files  # Import the files module from google.colab

def check_claim_truthfulness(query, api_key, output_file='claims_data.xlsx'):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    page_token = None
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15*30)  # Approximate 15 months back
    all_claims = []

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
                    for review in claim.get('claimReview', []):
                        claim_info = {
                            'Claim': claim.get('text'),
                            'Claimant': claim.get('claimant'),
                            'Claim Date': claim_date_str,
                            'Reviewed by': review.get('publisher', {}).get('name', 'Unknown publisher'),
                            'Review Date': review.get('reviewDate', 'Unknown date'),
                            'Rating': review.get('textualRating', 'No rating provided')
                        }
                        all_claims.append(claim_info)

            page_token = data.get('nextPageToken')
            if not page_token:
                print("End of results.")
                break
        else:
            print("Failed to fetch fact checks:", response.status_code)
            break

    if all_claims:
        df = pd.DataFrame(all_claims)
        df.to_excel(output_file, index=False)
        print(f"Data saved to {output_file}")
        files.download(output_file)  # Prompt to download the file in Colab
    else:
        print("No claims data to save.")

api_key = "AIzaSyBnD_PD6Q6zs3aZuBBUONA0SQQp7K9j4Qc"  # Replace "YOUR_API_KEY" with your actual Google Fact Check Tools API key
query = "Garlic"
check_claim_truthfulness(query, api_key)
