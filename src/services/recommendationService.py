# recommendationService.py
import multiprocessing
from tqdm import tqdm
import src.config.recommendationConfig as recommendationConfig
from src.utils.utils import RecommendationUtils

class RecommendationService:
    def process_id(self, id, results_queue):
        data = RecommendationUtils.scrape_record(id)
        keywords = RecommendationUtils.extract_keywords_from_metadata(data)

        selected_ids = []

        # Using multiprocessing.Pool to process keywords in parallel
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = list(tqdm(pool.imap(RecommendationUtils.search_records_by_keyword, keywords), desc="Processing keywords", total=len(keywords)))
            for result in results:
                if result is not None:
                    selected_ids.extend(result)

        selected_ids = set(sorted(selected_ids, key=lambda x: x[1], reverse=True))
        selected_ids = sorted(selected_ids, key=lambda x: x[1], reverse=True)
        length = int(len(selected_ids) * recommendationConfig.SELECTION_RATE)
        selected_ids = selected_ids[:length]

        results_queue.put(selected_ids)

    def process_user(self, user_doc, results_dict):
        print(f"Processing user: {user_doc.id}")
        recommended = []
        liked = user_doc.to_dict().get('liked', [])
        saved = user_doc.to_dict().get('saved', [])
        ids = liked + saved

        # Using a multiprocessing.Queue to collect results from the process_id function
        user_results_queue = multiprocessing.Queue()

        # Create separate processes for each ID
        processes = []
        for id in ids:
            process = multiprocessing.Process(target=self.process_id, args=(id, user_results_queue))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        # Collect results from the user-specific queue
        while not user_results_queue.empty():
            result = user_results_queue.get()
            recommended.extend(result)

        results_dict[user_doc.id] = recommended
