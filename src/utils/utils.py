import requests
import html2text
from rake_nltk import Rake
import src.config.recommendationConfig as recommendationConfig

class RecommendationUtils:
    # Initialize RAKE keyword extractor
    rake = Rake()

    @staticmethod
    def scrape_record(record_id):
        """
        Retrieve metadata for a Zenodo record using its ID.

        Args:
            record_id (str): The ID of the Zenodo record to retrieve.

        Returns:
            dict: A dictionary containing title, description, keywords, and resource type of the record.
        """
        url = f'https://zenodo.org/api/records/{record_id}'
        data = requests.get(url).json()
        if 'metadata' not in data:
            return {}

        metadata = {
            'title': data['metadata']['title'],
            'desc': html2text.html2text(data['metadata']['description']),
            'keywords': ','.join(data['metadata'].get('keywords', [])),
            'type': data['metadata']['resource_type']['type'],
        }
        return metadata

    @staticmethod
    def extract_keywords_from_metadata(metadata):
        """
        Extract important keywords from the metadata of a Zenodo record.

        Args:
            metadata (dict): A dictionary containing record metadata.

        Returns:
            list: A list of ranked keywords from the metadata.
        """
        full_text = '\n'.join(metadata.values())
        RecommendationUtils.rake.extract_keywords_from_text(full_text)

        # Extract ranked keywords with score >= 9
        ranked_keywords = [keyword[1] for keyword in RecommendationUtils.rake.get_ranked_phrases_with_scores() if keyword[0] >= 9]
        return ranked_keywords

    @staticmethod
    def search_records_by_keyword(query):
        """
        Search for Zenodo records containing a specific keyword.

        Args:
            query (str): The keyword to search for.

        Returns:
            list: A list of selected record IDs based on download stats.
        """
        url = f'https://zenodo.org/api/records?q={query}&size={recommendationConfig.SIZE}'
        data = requests.get(url).json()

        ids = []
        if 'hits' in data and 'hits' in data['hits']:
            # Collect record IDs and their download stats
            for hit in data['hits']['hits']:
                record_id = hit['id']
                downloads = hit['stats'].get('downloads', 0)
                ids.append((record_id, downloads))

        # Sort records by download stats and select the top records
        ids.sort(key=lambda x: x[1], reverse=True)
        length = int(recommendationConfig.SELECTION_RATE * len(ids))
        selected_records = ids[:length]
        return selected_records
