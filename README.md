# 🎬 Movie Recommender System

A content-based movie recommendation system that suggests movies based on user preferences using machine learning and natural language processing techniques.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rpatel0022/Movie-Recommender-System/blob/main/MovieRecommender.ipynb)
[![Deployed on Heroku](https://img.shields.io/badge/Deployed%20on-Heroku-430098.svg)](https://heroku.com/)

## 📋 Project Overview

This project implements a **content-based movie recommendation system** that analyzes movie characteristics to suggest similar films. Using a dataset of over 5,000 movies from The Movie Database (TMDb), the system processes movie metadata including genres, keywords, cast, crew, and plot overviews to generate personalized recommendations.

### 🎯 Key Features

- **Content-Based Filtering**: Recommends movies based on movie characteristics rather than user behavior
- **Advanced Text Processing**: Utilizes NLP techniques including stemming and vectorization
- **Cosine Similarity Algorithm**: Employs machine learning to calculate movie similarity scores
- **Interactive Interface**: Deployed web application for real-time recommendations
- **Comprehensive Dataset**: Processes 5,000+ movies with rich metadata

## 🛠️ Technologies Used

### **Programming Language**

- **Python 3.x**: Core development language

### **Data Science Libraries**

- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Scikit-learn**: Machine learning algorithms and text vectorization

### **Natural Language Processing**

- **NLTK (Natural Language Toolkit)**: Text preprocessing and stemming
- **CountVectorizer**: Text-to-numerical vector conversion

### **Machine Learning**

- **Cosine Similarity**: Similarity measurement algorithm
- **Feature Engineering**: Custom data transformation functions

### **Development Environment**

- **Jupyter Notebook**: Interactive development and analysis
- **Google Colab**: Cloud-based notebook execution
- **Kaggle**: Dataset source and management

### **Deployment**

- **Heroku**: Cloud application deployment platform

## 🔄 System Architecture

```
Raw Movie Data → Data Preprocessing → Feature Engineering → Text Vectorization → Similarity Calculation → Recommendations
```

## 📊 Dataset

The system uses the **TMDb 5000 Movie Dataset** containing:

- **tmdb_5000_movies.csv**: Movie metadata (genres, keywords, overview, etc.)
- **tmdb_5000_credits.csv**: Cast and crew information

**Dataset Features:**

- 5,000+ movies
- 20+ attributes per movie
- Rich metadata including genres, keywords, cast, crew, and plot summaries

## 🔧 Implementation Details

### **1. Data Preprocessing**

```python
# Merge datasets
movies = movies.merge(credits, on='title')

# Select relevant features
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# Handle missing values
movies.dropna(inplace=True)
```

### **2. Feature Engineering**

- **JSON Parsing**: Extract meaningful data from JSON-like string columns
- **Top Cast Selection**: Limit to top 3 cast members for relevance
- **Director Extraction**: Identify key crew member (director)
- **Text Normalization**: Remove spaces and standardize formatting

### **3. Natural Language Processing**

```python
# Stemming for text normalization
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# Text vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
```

### **4. Similarity Calculation**

```python
# Cosine similarity for movie recommendations
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
```

## 🚀 How It Works

1. **Input**: User selects a movie they enjoyed
2. **Processing**: System finds the movie in the database and retrieves its feature vector
3. **Similarity Calculation**: Computes cosine similarity with all other movies
4. **Ranking**: Sorts movies by similarity score
5. **Output**: Returns top 5 most similar movies

### **Example Usage**

```python
recommend('Batman Begins')
# Output:
# The Dark Knight
# Batman
# The Dark Knight Rises
# Batman Returns
# Batman Forever
```

## 📈 Model Performance

- **Algorithm**: Cosine Similarity
- **Feature Space**: 5,000 most frequent words
- **Processing Time**: Near real-time recommendations
- **Accuracy**: Content-based matching ensures thematically similar suggestions

## 🌐 Deployment

The application is deployed on **Heroku**, providing:

- Web-based interface for movie recommendations
- Real-time processing capabilities
- Scalable cloud infrastructure
- User-friendly experience

## 📁 Project Structure

```
Movie-Recommender-System/
├── MovieRecommender.ipynb    # Main Jupyter notebook with implementation
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies (if applicable)
```

## 🔮 Future Enhancements

- **Hybrid Filtering**: Combine content-based with collaborative filtering
- **User Profiles**: Implement user preference learning
- **Real-time Updates**: Dynamic dataset updates
- **Advanced NLP**: Implement deep learning for text analysis
- **UI/UX Improvements**: Enhanced web interface design

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Rushi Patel**

- GitHub: [@rpatel0022](https://github.com/rpatel0022)
- LinkedIn: [Connect with me](https://linkedin.com/in/your-profile)

---

⭐ **Star this repository if you found it helpful!**
