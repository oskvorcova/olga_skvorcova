CREATE TABLE IF NOT EXISTS webscrapper.searches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query_text VARCHAR(255),
    country VARCHAR(255),
    language_text VARCHAR(255),
    search_engine VARCHAR(255)
);