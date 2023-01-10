from data_processor import DataProcessor

if __name__ == "__main__":
    data = DataProcessor('../uk_news_scraping/data', ['headline', 'subheading', 'text'], 'guardian_*.csv')
    data_df = data.read_and_concat_data_files()
    print(data_df.head)