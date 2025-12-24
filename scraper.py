# ... (rest of your imports from scraper.py)

def scrape_imdb():
    driver = webdriver.Chrome() 
    driver.get("https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31&sort=num_votes,desc")
    time.sleep(5)

    movies = []
    items = driver.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item")

    for item in items[:50]: 
        try:
            title = item.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.split(". ", 1)[-1]
            rating = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
            votes_text = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.strip('()')
            
            # --- New Genre Logic ---
            # Genres are often located in a specific metadata block in the new layout
            try:
                # This selector finds the metadata row (Year, Duration, etc.)
                metadata = item.find_elements(By.CSS_SELECTOR, ".sc-b189961a-8.kLaxFE.dli-title-metadata-item")
                # Alternatively, search specifically for genre tags if they appear as links
                genre_elements = item.find_elements(By.CSS_SELECTOR, ".ipc-chip__text") 
                genre = ", ".join([g.text for g in genre_elements]) if genre_elements else "Unknown"
            except:
                genre = "Unknown"

            # Vote cleaning
            v = votes_text.replace('K', '000').replace('M', '000000').replace('.', '').replace(',', '')
            
            movies.append({
                "Title": title, 
                "Rating": float(rating), 
                "Votes": int(v) if v.isdigit() else 0,
                "Genre": genre  # Now uses scraped data instead of "Action"
            })
        except Exception as e:
            continue

    driver.quit()
    # ... (rest of the SQL saving logic from your scraper.py)