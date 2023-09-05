import re
import pandas as pd
from bs4 import BeautifulSoup

# Helper function to extract tender details from the content
def extract_tender_details(content):
    # Regular expression pattern to extract details
    pattern = r"(\d+\..+?)(\d+-\w+-\d+\s+\d+:\d+\s+[APM]{2})(\d+-\w+-\d+\s+\d+:\d+\s+[APM]{2})"
    matches = re.findall(pattern, content)
    
    # Structuring the extracted data
    structured_data = []
    for match in matches:
        title, closing_date, bid_opening_date = match
        ref_number_match = re.search(r"(\w+/[\w/-]+/\d+)", title)
        ref_number = ref_number_match.group(1) if ref_number_match else None
        title = title.replace(ref_number, "").strip() if ref_number else title.strip()
        structured_data.append({
            "Title": title,
            "Reference Number": ref_number,
            "Closing Date": closing_date,
            "Bid Opening Date": bid_opening_date
        })
    
    return structured_data

# Main execution
if __name__ == "__main__":
    # Reading the HTML content
    with open("Government eProcurement System.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    page_contents = soup.find_all(class_='page_content')
    
    # Extracting tender details from the available content
    tender_data = []
    for content in page_contents:
        tender_data.extend(extract_tender_details(content.get_text(strip=True)))

    # Creating a dataframe from the structured data
    tender_df = pd.DataFrame(tender_data)

    # Saving the structured data to a CSV
    tender_df.to_csv("structured_tenders_new.csv", index=False)

    print("Tender data has been saved to 'structured_tenders_new.csv'")
