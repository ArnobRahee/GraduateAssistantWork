import pyreadstat
import pandas as pd

def clean_special_characters(df):
    """Remove or replace special characters in the DataFrame."""
    return df.applymap(
        lambda x: ''.join(char if char.isprintable() else '' for char in str(x))
        if isinstance(x, str) else x
    )

def read_data_with_error_handling(file_path):
    try:
        # Attempt to read the entire file
        df, meta = pyreadstat.read_dta(file_path)
        print("Successfully read the entire file!")
    except Exception as e:
        print(f"Error: {e}")
        print("Trying to read in chunks to skip problematic rows...")

        # Read in chunks to isolate and collect valid rows
        chunks = []
        try:
            reader = pyreadstat.read_file_in_chunks(pyreadstat.read_dta, file_path, chunksize=1000)
            for chunk, _ in reader:
                chunks.append(chunk)
        except Exception as chunk_error:
            print(f"Error reading chunks: {chunk_error}")

        if chunks:
            # Combine all valid chunks
            df = pd.concat(chunks, ignore_index=True)
            print("Successfully read the file in chunks!")
        else:
            print("No valid data could be read.")
            return None

    # Clean special characters from the DataFrame
    df = clean_special_characters(df)

    # Save to CSV for further processing
    df.to_csv('cleaned_dataset.csv', index=False)
    print("Cleaned dataset saved to 'cleaned_dataset.csv'.")
    return df

# Path to your Stata file
file_path = '1-rahee_thesis_201804-202412_sample.dta'

# Read and clean the data
cleaned_df = read_data_with_error_handling(file_path)
