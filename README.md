# TOPSnet Backend

TOPSnet Backend is a Python-based server-side component for the TOPSNET web application. It fetches data from Firebase and other APIs, processes the data, and generates personalized research recommendations for users.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rudrodip/topsnet-backend.git
   cd topsnet-backend
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Obtain the service account key for Firebase and save it as `serviceAccountKey.json` in the same directory as `firebase.py`.

## Usage

To run the backend service, execute the following command:

```bash
python main.py
```

TOPSNET Backend will start processing data from Firebase and external APIs, perform recommendation tasks, and update the database with the results.

## Features

- **Data Fetching**: Fetch data from Firebase and external APIs to obtain research papers and resources.

- **Data Processing**: Process the retrieved data using `html2text` and `Rake` libraries to extract metadata and keywords.

- **Recommendation Generation**: Implement a recommendation engine that analyzes user interactions to generate research recommendations.

- **Data Writing**: Write processed data and recommendation results back to Firebase for integration with the frontend.

## Recommendation Engine

TOPSNET Backend utilizes a recommendation engine based on collaborative filtering techniques. It analyzes user behaviors, such as liked and saved items, to deliver relevant research recommendations.

## Contact

For inquiries or support related to TOPSNET Backend, please contact the developer:

- **Email**: official.rudrodipsarker@gmail.com
- **GitHub**: [rudrodip](https://github.com/rudrodip)
- **Personal Website**: [https://rudrodipsarker.vercel.app](https://rudrodipsarker.vercel.app)

## License

TOPSNET Backend is open-source and licensed under the MIT License.