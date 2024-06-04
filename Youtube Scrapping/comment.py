import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader

def scrape_comments(video_id):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(f"https://www.youtube.com/watch?v={video_id}")
    comment_data = []
    for comment in comments:
        author = comment.get('author', 'Unknown')
        text = comment.get('text', '')
        date = comment.get('time', '')
        comment_data.append({'Author': author, 'Comment': text, 'Date': date})
    return comment_data

if __name__ == "__main__":
    video_id = 'xPUCaZDTiFE'  # Replace this with your video ID
    comments = scrape_comments(video_id)
    
    # Create a DataFrame from the comment data
    df = pd.DataFrame(comments, columns=['Author', 'Comment', 'Date'])
    
    # Save the DataFrame to an Excel file
    output_file = 'comments.xlsx'
    df.to_excel(output_file, index=False)
    
    print(f"Comments saved to {output_file}")
