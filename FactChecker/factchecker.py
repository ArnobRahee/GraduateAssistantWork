import requests
from openpyxl import Workbook


def check_claim_truthfulness(query, api_key):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    page_token = None
    wb = Workbook()
    ws = wb.active
    ws.append(["Claim", "Claimant", "Claim Date", "Publisher", "Review Date", "Rating"])

    while True:
        params = {
            "query": query,
            "key": api_key,
            "languageCode": "en",
            "pageSize": 10
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
                claim_text = claim.get('text')
                claimant = claim.get('claimant')
                claim_date = claim.get('claimDate')
                for review in claim.get('claimReview', []):
                    publisher = review.get('publisher', {}).get('name', 'Unknown publisher')
                    review_date = review.get('reviewDate', 'Unknown date')
                    rating = review.get('textualRating', 'No rating provided')
                    ws.append([claim_text, claimant, claim_date, publisher, review_date, rating])

            page_token = data.get('nextPageToken')
            if not page_token:
                print("End of results.")
                break
        else:
            print("Failed to fetch fact checks:", response.status_code)
            break

    wb.save("fact_check_results.xlsx")
    print("Results saved to fact_check_results.xlsx")


api_key = "AIzaSyBnD_PD6Q6zs3aZuBBUONA0SQQp7K9j4Qc"  # Replace YOUR_API_KEY with your actual Google Fact Check Tools API key
query = "covid"
check_claim_truthfulness(query, api_key)
