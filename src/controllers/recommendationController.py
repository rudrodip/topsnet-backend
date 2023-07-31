import multiprocessing
from firebase_admin import firestore
from tqdm import tqdm
from src.config.firebase import db
from src.services.recommendationService import RecommendationService

class RecommendationController:
    @staticmethod
    def array_union_user_recommended_field(user_id, ids):
        # Get the reference to the user document
        user_ref = db.collection('user').document(user_id)

        # Perform the arrayUnion operation on the 'recommended' field
        user_ref.update({
            'recommended': firestore.ArrayUnion(ids)
        })

    @classmethod
    def run_recommendation_engine(cls):
        # Create a dictionary to store results for each user
        manager = multiprocessing.Manager()
        results_dict = manager.dict()

        users_ref = db.collection('user')
        docs = users_ref.get()

        # Create an instance of the RecommendationService
        recommendation_service = RecommendationService()

        processes = []
        for doc in tqdm(docs, desc="Iterating through users"):
            process = multiprocessing.Process(target=recommendation_service.process_user, args=(doc, results_dict))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        # Process the results for each user
        for user_id, recommended in results_dict.items():
            # Process the recommended array as needed
            recommended = [i[0] for i in recommended]
            cls.array_union_user_recommended_field(user_id, recommended)
            print(f'Recommend for user: {user_id}: {recommended}')
