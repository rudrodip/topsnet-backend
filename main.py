# main.py
from src.controllers.recommendationController import RecommendationController

def main():
    recommendation_controller = RecommendationController()
    recommendation_controller.run_recommendation_engine()

if __name__ == "__main__":
    main()