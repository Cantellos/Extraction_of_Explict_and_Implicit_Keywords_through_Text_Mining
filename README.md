# Extraction of Explicit and Implicit Keywords through Text Mining

## Overview

This project aims to extract both **explicit** and **implicit** keywords from textual data using text mining and natural language processing (NLP) techniques. While explicit keywords are directly mentioned in the text, implicit keywords represent underlying or contextually relevant concepts that are not overtly stated. 

The goal is to enhance keyword extraction by uncovering hidden themes and improving downstream tasks such as:
- Information retrieval
- Text summarization
- Document classification
- Topic modeling

## Features

- Extraction of explicit keywords using standard NLP techniques
- Identification of implicit keywords using semantic analysis
- Preprocessing pipeline for raw textual data
- Evaluation metrics for keyword relevance and coverage

## Technologies Used

- Python 3.x  
- NLTK / spaCy  
- Scikit-learn  
- Gensim  
- Word embeddings (e.g., Word2Vec, GloVe)

## Project Structure

```
├── data/                   # Sample text data for testing
├── src/                    # Source code for keyword extraction
│   ├── preprocessing.py    # Text cleaning and preprocessing
│   ├── explicit.py         # Explicit keyword extraction methods
│   ├── implicit.py         # Implicit keyword extraction using semantic similarity
│   └── utils.py            # Helper functions
├── results/                # Output and evaluation results
├── requirements.txt        # List of required Python packages
└── README.md               # Project documentation
```

## Getting Started

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Cantellos/Extraction_of_Explict_and_Implicit_Keywords_through_Text_Mining.git
   cd Extraction_of_Explict_and_Implicit_Keywords_through_Text_Mining
   ```

2. **Install dependencies**  
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the extraction pipeline**  
   Example:
   ```bash
   python src/main.py --input data/sample_text.txt --output results/keywords.json
   ```

## Example Input

```text
Artificial intelligence is transforming industries by automating complex processes and generating insights from large datasets.
```

## Example Output

```json
{
  "explicit_keywords": ["Artificial intelligence", "industries", "automation", "datasets"],
  "implicit_keywords": ["machine learning", "data analysis", "business intelligence"]
}
```

## Contributions

Feel free to fork the repository, open issues, or submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
