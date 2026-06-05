import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Target URL
url = "https://books.toscrape.com/"

# 2. Connect to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

titles = []
prices = []
stocks = []

# 3. Navigate the HTML structure
books = soup.find_all('article', class_='product_pod')

for book in books:
    # Get the book title
    title = book.h3.a['title']
    titles.append(title)

    # Get the price and strip out the broken 'Â' character automatically
    raw_price = book.find('p', class_='price_color').text
    clean_price = raw_price.replace('Â', '') # This line deletes the 'Â'
    prices.append(clean_price)

    # Get availability
    stock = book.find('p', class_='instock availability').text.strip()
    stocks.append(stock)

# 4. Create dataset
data = {
    'Book Title': titles,
    'Price': prices,
    'Availability': stocks
}
df = pd.DataFrame(data)

# 5. Save with explicit utf-8-sig encoding (tells Excel to read the Pound sign correctly)
df.to_csv('scraped_books_dataset.csv', index=False, encoding='utf-8-sig')

print(" Success! Cleaned dataset created with correct currency formatting.")
print(df.head())

