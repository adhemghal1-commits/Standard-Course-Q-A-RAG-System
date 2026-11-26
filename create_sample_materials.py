"""
Generate sample course materials in CSV, DOCX, and TXT formats.
Run once to create the files in the 'Course files' directory.
"""
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.join(BASE_DIR, "Course files")
os.makedirs(COURSE_DIR, exist_ok=True)

# =====================================================================
# COURSE 2: Data Science with Python  (CSV + TXT)
# =====================================================================

DS_CSV_DATA = [
    ["Topic", "Concept", "Description", "Example"],
    ["Introduction", "What is Data Science?",
     "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data. It combines domain expertise, programming skills, and knowledge of statistics and mathematics to analyze and interpret complex data.",
     "Analyzing customer purchase patterns to predict future buying behavior."],
    ["Introduction", "Data Science Workflow",
     "The data science workflow consists of several steps: 1) Define the problem, 2) Collect data, 3) Clean and preprocess data, 4) Explore data with EDA, 5) Feature engineering, 6) Model building, 7) Model evaluation, 8) Deployment. Each step is crucial for building a successful data-driven solution.",
     "A workflow to predict house prices: collect real estate data, clean missing values, explore features, build a regression model, evaluate with RMSE."],
    ["Pandas", "DataFrames",
     "A DataFrame is a two-dimensional, size-mutable, and potentially heterogeneous tabular data structure with labeled axes (rows and columns). It is the primary Pandas data structure. You can create DataFrames from dictionaries, CSV files, databases, and many other sources.",
     "df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})"],
    ["Pandas", "Handling Missing Data",
     "Missing data is common in real-world datasets. Pandas provides several methods: df.isnull() to detect missing values, df.dropna() to remove rows or columns with missing values, df.fillna(value) to fill missing values with a specified value or method like forward fill (ffill) or backward fill (bfill).",
     "df['age'].fillna(df['age'].mean(), inplace=True) fills missing ages with the mean age."],
    ["Pandas", "GroupBy Operations",
     "The groupby operation involves splitting the data into groups based on some criteria, applying a function to each group independently, and combining the results. This is known as the split-apply-combine strategy. It is very powerful for aggregating and summarizing data.",
     "df.groupby('department')['salary'].mean() computes average salary per department."],
    ["Pandas", "Merging and Joining",
     "Pandas supports SQL-style merging and joining of DataFrames using merge() and join() methods. You can perform inner, outer, left, and right joins. The merge function aligns data based on one or more keys, similar to SQL JOIN operations.",
     "pd.merge(df1, df2, on='customer_id', how='left') joins two DataFrames on customer_id."],
    ["Visualization", "Matplotlib Basics",
     "Matplotlib is the foundational plotting library in Python. It provides a MATLAB-like interface for creating static, animated, and interactive visualizations. The pyplot module (plt) is the most commonly used interface. Common plots include line plots, bar charts, histograms, and scatter plots.",
     "plt.plot(x, y); plt.xlabel('X'); plt.ylabel('Y'); plt.title('My Plot'); plt.show()"],
    ["Visualization", "Seaborn for Statistical Plots",
     "Seaborn is built on top of Matplotlib and provides a high-level interface for drawing attractive statistical graphics. It integrates well with Pandas DataFrames and supports complex visualizations like heatmaps, violin plots, pair plots, and categorical plots with minimal code.",
     "sns.heatmap(df.corr(), annot=True, cmap='coolwarm') creates a correlation heatmap."],
    ["Statistics", "Descriptive Statistics",
     "Descriptive statistics summarize and describe the main features of a dataset. Key measures include: mean (average), median (middle value), mode (most frequent), standard deviation (spread), variance, range, quartiles, and percentiles. Pandas provides describe() for quick summaries.",
     "df.describe() returns count, mean, std, min, 25%, 50%, 75%, max for numeric columns."],
    ["Statistics", "Hypothesis Testing",
     "Hypothesis testing is a statistical method used to make decisions based on data. The null hypothesis (H0) assumes no effect or difference, while the alternative hypothesis (H1) assumes there is an effect. Common tests include t-tests, chi-square tests, and ANOVA. The p-value helps determine statistical significance.",
     "A p-value < 0.05 typically leads to rejecting the null hypothesis."],
    ["Data Cleaning", "Handling Outliers",
     "Outliers are data points that differ significantly from other observations. Detection methods include IQR (Interquartile Range), Z-score, and visual methods like box plots. Treatment options include removal, capping (winsorizing), or transformation. The choice depends on whether outliers are errors or genuine extreme values.",
     "Q1 = df['value'].quantile(0.25); Q3 = df['value'].quantile(0.75); IQR = Q3 - Q1; outliers = df[(df['value'] < Q1 - 1.5*IQR) | (df['value'] > Q3 + 1.5*IQR)]"],
    ["Feature Engineering", "Feature Scaling",
     "Feature scaling normalizes the range of independent variables. Common methods: StandardScaler (z-score normalization, mean=0, std=1), MinMaxScaler (scales to [0,1] range), and RobustScaler (uses median and IQR, robust to outliers). Scaling is essential for algorithms sensitive to feature magnitudes like SVM, KNN, and neural networks.",
     "from sklearn.preprocessing import StandardScaler; scaler = StandardScaler(); X_scaled = scaler.fit_transform(X)"],
]

csv_path = os.path.join(COURSE_DIR, "DS_Python_course_materials.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(DS_CSV_DATA)
print(f"Created: {csv_path}")


DS_TXT_CONTENT = """=============================================================
DATA SCIENCE WITH PYTHON – COMPREHENSIVE COURSE NOTES
=============================================================

Chapter 1: Introduction to Data Science
-----------------------------------------
Data science is a multidisciplinary field that combines statistics,
computer science, and domain expertise to extract meaningful insights
from data. The goal of data science is to transform raw data into
actionable knowledge.

Key Components of Data Science:
1. Data Collection: Gathering data from various sources (databases,
   APIs, web scraping, sensors, surveys).
2. Data Cleaning: Handling missing values, removing duplicates,
   fixing inconsistencies, and dealing with outliers.
3. Exploratory Data Analysis (EDA): Understanding data distributions,
   relationships, and patterns through visualizations and statistics.
4. Feature Engineering: Creating new features from existing data to
   improve model performance.
5. Machine Learning: Building predictive models using algorithms.
6. Communication: Presenting findings through reports and dashboards.

Chapter 2: Python for Data Science
-----------------------------------------
Python is the most popular language for data science due to its
simplicity, extensive library ecosystem, and strong community support.

Essential Libraries:
- NumPy: Numerical computing with N-dimensional arrays. Provides
  efficient mathematical operations on arrays and matrices.
  Example: np.array([1,2,3]), np.mean(), np.std()

- Pandas: Data manipulation and analysis. The DataFrame is the
  central data structure.
  Example: pd.read_csv('data.csv'), df.head(), df.describe()

- Matplotlib: Basic plotting and visualization.
  Example: plt.plot(x, y), plt.bar(), plt.hist()

- Seaborn: Statistical data visualization built on Matplotlib.
  Example: sns.boxplot(), sns.heatmap(), sns.pairplot()

- Scikit-learn: Machine learning library with tools for
  classification, regression, clustering, and preprocessing.
  Example: from sklearn.linear_model import LinearRegression

Chapter 3: Data Cleaning Techniques
-----------------------------------------
Data cleaning is often the most time-consuming step, taking up
60-80% of a data scientist's time.

Handling Missing Data:
- Detection: df.isnull().sum() shows count of missing values
- Deletion: df.dropna() removes rows; df.dropna(axis=1) removes columns
- Imputation: df.fillna(value) fills with constant; df.fillna(method='ffill')
  forward fills; df.interpolate() uses interpolation

Handling Duplicates:
- Detection: df.duplicated().sum()
- Removal: df.drop_duplicates(subset=['col1', 'col2'])

Data Type Conversion:
- df['date'] = pd.to_datetime(df['date'])
- df['category'] = df['category'].astype('category')
- pd.to_numeric(df['price'], errors='coerce')

String Cleaning:
- df['name'] = df['name'].str.strip().str.lower()
- df['text'] = df['text'].str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)

Chapter 4: Exploratory Data Analysis
-----------------------------------------
EDA is the process of analyzing datasets to summarize their main
characteristics, often using visual methods.

Steps in EDA:
1. Understand the shape: df.shape, df.info(), df.dtypes
2. Summary statistics: df.describe(), df.value_counts()
3. Distribution analysis: histograms, density plots, box plots
4. Correlation analysis: df.corr(), heatmaps
5. Outlier detection: box plots, scatter plots, IQR method
6. Feature relationships: pair plots, scatter matrices

Chapter 5: Feature Engineering
-----------------------------------------
Feature engineering is the process of creating new features from raw
data to improve model performance.

Techniques:
- One-Hot Encoding: Convert categorical variables to binary columns
  pd.get_dummies(df, columns=['color'])
- Label Encoding: Assign numeric labels to categories
  from sklearn.preprocessing import LabelEncoder
- Binning: Convert continuous to categorical
  pd.cut(df['age'], bins=[0, 18, 35, 50, 100], labels=['child','young','middle','senior'])
- Log Transformation: Reduce skewness
  df['log_income'] = np.log1p(df['income'])
- Polynomial Features: Create interaction terms
  from sklearn.preprocessing import PolynomialFeatures
"""

txt_path = os.path.join(COURSE_DIR, "DS_Python_notes.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(DS_TXT_CONTENT)
print(f"Created: {txt_path}")


# =====================================================================
# COURSE 3: Natural Language Processing  (DOCX + TXT + CSV)
# =====================================================================

try:
    from docx import Document

    doc = Document()
    doc.add_heading("Natural Language Processing – Course Materials", level=0)

    sections = [
        ("Chapter 1: Introduction to NLP", [
            "Natural Language Processing (NLP) is a subfield of artificial intelligence and computational linguistics concerned with the interactions between computers and human (natural) languages. The goal is to enable computers to understand, interpret, and generate human language in a meaningful and useful way.",
            "Key NLP Tasks include: Text Classification (categorizing text into predefined classes like spam detection), Named Entity Recognition (identifying entities like persons, organizations, locations), Sentiment Analysis (determining the emotional tone of text), Machine Translation (translating text from one language to another), Question Answering (automatically answering questions posed in natural language), Text Summarization (creating concise summaries of longer documents), and Language Generation (producing human-like text).",
            "Applications of NLP are everywhere: virtual assistants (Siri, Alexa), email spam filters, autocomplete and autocorrect, search engines, chatbots, language translation services, and content recommendation systems.",
        ]),
        ("Chapter 2: Text Preprocessing", [
            "Text preprocessing is a crucial step in any NLP pipeline. Raw text data is noisy and unstructured, requiring several cleaning and normalization steps before it can be used for analysis or model training.",
            "Tokenization is the process of breaking text into individual tokens (words, subwords, or characters). Word tokenization splits on whitespace and punctuation. Subword tokenization (like BPE or WordPiece) breaks words into smaller units, handling out-of-vocabulary words effectively.",
            "Stop Word Removal eliminates common words that carry little semantic meaning (like 'the', 'is', 'at', 'and'). While useful for some tasks like information retrieval, stop words can be important for tasks like sentiment analysis where words like 'not' change meaning.",
            "Stemming reduces words to their root form by removing suffixes. The Porter Stemmer is the most common: 'running' becomes 'run', 'better' becomes 'better'. Lemmatization is more sophisticated, using vocabulary and morphological analysis to return the base dictionary form (lemma): 'better' becomes 'good', 'went' becomes 'go'.",
            "Text normalization includes lowercasing, removing special characters, expanding contractions ('don't' to 'do not'), and handling numbers and dates consistently.",
        ]),
        ("Chapter 3: Word Embeddings", [
            "Word embeddings are dense vector representations of words that capture semantic meaning. Unlike one-hot encoding (sparse, high-dimensional, no semantic information), word embeddings map words to low-dimensional continuous vectors where semantically similar words are close together.",
            "Word2Vec (by Google, 2013) learns word embeddings using neural networks. It has two architectures: CBOW (Continuous Bag of Words) predicts a target word from context words, and Skip-gram predicts context words from a target word. Skip-gram works better for small datasets and rare words.",
            "GloVe (Global Vectors for Word Representation, by Stanford) combines global matrix factorization with local context window methods. It constructs a co-occurrence matrix and factorizes it to produce word vectors that capture both global statistical information and local context.",
            "FastText (by Facebook) extends Word2Vec by representing each word as a bag of character n-grams. This allows it to generate embeddings for out-of-vocabulary words and capture morphological information. For example, 'unhappiness' shares n-grams with 'happy' and 'unhappy'.",
        ]),
        ("Chapter 4: Transformer Architecture", [
            "The Transformer architecture, introduced in the paper 'Attention Is All You Need' (Vaswani et al., 2017), revolutionized NLP by replacing recurrent layers with self-attention mechanisms. This allows for much better parallelization during training and captures long-range dependencies more effectively.",
            "Self-Attention Mechanism: The core innovation of Transformers. For each position in the input sequence, self-attention computes attention weights for all other positions, creating a weighted sum. This is done through Query (Q), Key (K), and Value (V) matrices: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k))V.",
            "Multi-Head Attention runs multiple attention operations in parallel (each called a 'head'), allowing the model to attend to information from different representation subspaces at different positions. The outputs are concatenated and linearly transformed.",
            "Positional Encoding: Since Transformers process all positions simultaneously (unlike RNNs which process sequentially), they need a way to encode position information. Sinusoidal positional encodings are added to input embeddings to provide information about token positions.",
            "The Transformer consists of an Encoder (processes the input sequence) and a Decoder (generates the output sequence). The encoder has self-attention and feed-forward layers. The decoder adds cross-attention over encoder outputs.",
        ]),
        ("Chapter 5: BERT and GPT", [
            "BERT (Bidirectional Encoder Representations from Transformers) by Google (2018) is a pre-trained language model that uses only the encoder part of the Transformer. It is trained bidirectionally, meaning it considers context from both left and right simultaneously. BERT uses Masked Language Modeling (MLM) where random tokens are masked and the model predicts them, and Next Sentence Prediction (NSP) to understand sentence relationships.",
            "GPT (Generative Pre-trained Transformer) by OpenAI uses only the decoder part of the Transformer. It is trained autoregressively (left-to-right), predicting the next token given all previous tokens. GPT-2 (1.5B parameters), GPT-3 (175B parameters), and GPT-4 showed that scaling up model size leads to emergent capabilities.",
            "Key Differences: BERT is bidirectional and better for understanding tasks (classification, NER, QA extraction). GPT is unidirectional (autoregressive) and better for generation tasks (text completion, summarization, translation). BERT uses encoder-only architecture; GPT uses decoder-only.",
            "Fine-tuning: Both BERT and GPT can be fine-tuned on downstream tasks with relatively small datasets. For BERT, you add a task-specific head (e.g., classification layer) on top. For GPT, you can use prompt engineering or instruction tuning.",
            "T5 (Text-to-Text Transfer Transformer) by Google treats every NLP task as a text-to-text problem. Input: 'translate English to German: Hello' Output: 'Hallo'. This unified framework simplifies multi-task learning.",
        ]),
        ("Chapter 6: Attention Mechanisms and Variants", [
            "Scaled Dot-Product Attention computes attention scores as the dot product of queries and keys, scaled by the square root of the key dimension, then applies softmax to get weights, and finally computes a weighted sum of values.",
            "Additive Attention (Bahdanau Attention) uses a feed-forward network to compute attention scores. It was introduced for sequence-to-sequence models in machine translation before the Transformer.",
            "Cross-Attention is used in the decoder to attend to encoder outputs, allowing the decoder to focus on relevant parts of the input when generating each output token.",
            "Sparse Attention patterns (like in Longformer, BigBird) reduce the quadratic complexity of self-attention by restricting which positions each token can attend to, using local windows, global tokens, and random connections.",
        ]),
    ]

    for title, paragraphs in sections:
        doc.add_heading(title, level=1)
        for para in paragraphs:
            doc.add_paragraph(para)

    docx_path = os.path.join(COURSE_DIR, "NLP_course_materials.docx")
    doc.save(docx_path)
    print(f"Created: {docx_path}")

except ImportError:
    print("python-docx not installed – skipping DOCX creation")


NLP_CSV_DATA = [
    ["Topic", "Term", "Definition", "Example"],
    ["Basics", "Tokenization",
     "The process of splitting text into individual tokens such as words, subwords, or characters. It is the first step in most NLP pipelines.",
     "Input: 'Hello world!' Tokens: ['Hello', 'world', '!']"],
    ["Basics", "Bag of Words",
     "A text representation model that describes the occurrence of words within a document. It creates a vocabulary of all unique words and represents each document as a vector of word counts.",
     "Doc: 'the cat sat' Vector: [1, 1, 1, 0, 0] (for vocab [the, cat, sat, dog, ran])"],
    ["Basics", "TF-IDF",
     "Term Frequency-Inverse Document Frequency is a numerical statistic that reflects how important a word is to a document in a corpus. TF measures how frequently a term occurs in a document. IDF measures how rare or common a word is across all documents.",
     "A word appearing in every document has low IDF; a word appearing in few documents has high IDF."],
    ["Models", "Seq2Seq",
     "Sequence-to-sequence models use an encoder to process the input sequence into a context vector and a decoder to generate the output sequence. Used in machine translation, summarization, and dialogue systems.",
     "English to French: Encoder processes 'I love cats' Decoder generates 'J'aime les chats'"],
    ["Models", "Attention Mechanism",
     "A mechanism that allows the model to focus on relevant parts of the input when producing each part of the output. Instead of compressing the entire input into one vector, attention creates a weighted combination of all encoder hidden states.",
     "When translating 'the black cat', generating 'noir' attends most to 'black'."],
    ["Models", "BERT",
     "Bidirectional Encoder Representations from Transformers. A pre-trained model that reads text bidirectionally to understand context. It uses masked language modeling and next sentence prediction during pre-training.",
     "BERT can be fine-tuned for classification: input '[CLS] This movie is great [SEP]' output: 'positive'."],
    ["Evaluation", "BLEU Score",
     "Bilingual Evaluation Understudy measures the quality of machine-translated text by comparing n-gram overlap between generated and reference translations. Scores range from 0 to 1, with 1 being a perfect match.",
     "A BLEU score of 0.4 means 40% n-gram overlap with reference translations."],
    ["Evaluation", "Perplexity",
     "A measurement of how well a probability distribution predicts a sample. Lower perplexity indicates the model is better at predicting the text. It is calculated as the exponentiated average negative log-likelihood of the test set.",
     "A language model with perplexity 20 means it is as uncertain as choosing uniformly among 20 options."],
]

nlp_csv_path = os.path.join(COURSE_DIR, "NLP_glossary.csv")
with open(nlp_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(NLP_CSV_DATA)
print(f"Created: {nlp_csv_path}")


NLP_TXT_CONTENT = """=============================================================
NATURAL LANGUAGE PROCESSING – QUICK REFERENCE NOTES
=============================================================

1. Text Preprocessing Pipeline
-------------------------------
Raw Text -> Lowercase -> Remove Punctuation -> Tokenize ->
Remove Stop Words -> Stemming/Lemmatization -> Vectorization

Common Libraries:
- NLTK: Natural Language Toolkit - comprehensive NLP library
  nltk.word_tokenize(), nltk.sent_tokenize()
  PorterStemmer(), WordNetLemmatizer()
- spaCy: Industrial-strength NLP library
  nlp = spacy.load('en_core_web_sm'); doc = nlp(text)
  Token attributes: token.text, token.lemma_, token.pos_, token.dep_

2. Text Representation Methods
-------------------------------
One-Hot Encoding: Binary vector, one dimension per word in vocabulary.
Sparse and high-dimensional. No semantic relationships captured.

Bag of Words (BoW): Count of each word in document. Simple but loses
word order. Can use binary (presence/absence) or frequency counts.

TF-IDF: Weights words by their importance. High TF-IDF means the word
is frequent in the document but rare across the corpus.

Word Embeddings: Dense, low-dimensional vectors (50-300 dimensions).
Capture semantic relationships: king - man + woman = queen.

3. Named Entity Recognition (NER)
-------------------------------
NER identifies and classifies named entities in text into predefined
categories: PERSON, ORGANIZATION, LOCATION, DATE, MONEY, etc.

Approaches:
- Rule-based: Regular expressions and dictionaries
- Statistical: CRF (Conditional Random Fields), HMM
- Deep Learning: BiLSTM-CRF, Transformer-based (BERT)

4. Sentiment Analysis
-------------------------------
Sentiment analysis determines the emotional tone of text.

Approaches:
- Lexicon-based: Use sentiment dictionaries (VADER, SentiWordNet)
- Machine Learning: Train classifiers (SVM, Naive Bayes) on labeled data
- Deep Learning: Use pre-trained models (BERT) fine-tuned for sentiment

Challenges: Sarcasm, negation, context-dependent sentiment,
multi-aspect sentiment (a restaurant review may be positive about
food but negative about service).

5. Language Models
-------------------------------
A language model assigns probabilities to sequences of words.

N-gram Models: P(w_n | w_1...w_{n-1}) approximated as P(w_n | w_{n-k}...w_{n-1})
Unigram (k=0), Bigram (k=1), Trigram (k=2)

Neural Language Models:
- RNN/LSTM: Process sequences token by token, maintaining hidden state
- Transformer: Self-attention mechanism, processes all tokens in parallel
- GPT family: Autoregressive, predict next token
- BERT family: Bidirectional, predict masked tokens
"""

nlp_txt_path = os.path.join(COURSE_DIR, "NLP_reference_notes.txt")
with open(nlp_txt_path, "w", encoding="utf-8") as f:
    f.write(NLP_TXT_CONTENT)
print(f"Created: {nlp_txt_path}")


# =====================================================================
# Additional ML TXT (Course 1 already has PDFs, add supplementary TXT)
# =====================================================================

ML_TXT_CONTENT = """=============================================================
MACHINE LEARNING FUNDAMENTALS – SUPPLEMENTARY NOTES
=============================================================

Chapter 1: What is Machine Learning?
-----------------------------------------
Machine Learning (ML) is a subset of artificial intelligence that
enables systems to learn and improve from experience without being
explicitly programmed. The key idea is that machines can identify
patterns in data and make decisions with minimal human intervention.

Types of Machine Learning:
1. Supervised Learning: The algorithm learns from labeled training data.
   - Classification: Predict categorical labels (spam/not spam, cat/dog)
   - Regression: Predict continuous values (house prices, temperature)
   Common algorithms: Linear Regression, Logistic Regression, Decision
   Trees, Random Forest, Support Vector Machines (SVM), K-Nearest
   Neighbors (KNN), Neural Networks.

2. Unsupervised Learning: The algorithm finds hidden patterns in
   unlabeled data.
   - Clustering: Group similar data points (K-Means, DBSCAN, Hierarchical)
   - Dimensionality Reduction: Reduce features while preserving information
     (PCA, t-SNE, UMAP)
   - Association Rules: Find relationships between variables (Apriori)

3. Reinforcement Learning: The agent learns by interacting with an
   environment and receiving rewards or penalties.
   - Applications: Game playing, robotics, autonomous vehicles
   - Key concepts: State, Action, Reward, Policy, Value Function

Chapter 2: Model Evaluation
-----------------------------------------
Overfitting occurs when a model learns the training data too well,
including noise and outliers, and fails to generalize to new data.
Signs: High training accuracy, low test accuracy.

Underfitting occurs when a model is too simple to capture the
underlying patterns in the data.
Signs: Low training accuracy, low test accuracy.

The Bias-Variance Tradeoff:
- Bias: Error from erroneous assumptions in the learning algorithm.
  High bias means the model is too simple (underfitting).
- Variance: Error from sensitivity to small fluctuations in training data.
  High variance means the model is too complex (overfitting).
- The goal is to find the sweet spot that minimizes total error.

Evaluation Metrics:
- Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC,
  Confusion Matrix
- Regression: MSE, RMSE, MAE, R-squared (R2), Adjusted R2

Cross-Validation:
- K-Fold: Split data into K folds, train on K-1, test on 1, rotate
- Stratified K-Fold: Maintains class distribution in each fold
- Leave-One-Out: K = number of samples (expensive but thorough)

Chapter 3: Ensemble Methods
-----------------------------------------
Ensemble methods combine multiple models to produce better predictive
performance than any single model alone.

Bagging (Bootstrap Aggregating):
- Train multiple models on random subsets of data (with replacement)
- Combine predictions by voting (classification) or averaging (regression)
- Example: Random Forest (bagging with decision trees)
- Reduces variance, helps with overfitting

Boosting:
- Train models sequentially, each focusing on errors of previous models
- Examples: AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost
- Reduces bias, can overfit if not regularized

Stacking:
- Train multiple diverse models (base learners)
- Use another model (meta-learner) to combine their predictions
- Can capture complex patterns from different model types

Chapter 4: Regularization Techniques
-----------------------------------------
Regularization prevents overfitting by adding a penalty term to the
loss function that discourages complex models.

L1 Regularization (Lasso):
- Adds absolute value of coefficients as penalty
- Can reduce coefficients to exactly zero (feature selection)
- Loss = Original Loss + lambda * sum(|w_i|)

L2 Regularization (Ridge):
- Adds squared coefficients as penalty
- Shrinks coefficients towards zero but rarely makes them exactly zero
- Loss = Original Loss + lambda * sum(w_i^2)

Elastic Net:
- Combination of L1 and L2 regularization
- Loss = Original Loss + lambda1 * sum(|w_i|) + lambda2 * sum(w_i^2)

Dropout (for Neural Networks):
- Randomly deactivates neurons during training with probability p
- Forces the network to learn redundant representations
- Acts as an ensemble of sub-networks

Early Stopping:
- Monitor validation loss during training
- Stop training when validation loss starts increasing
- Prevents the model from memorizing training data
"""

ml_txt_path = os.path.join(COURSE_DIR, "ML_fundamentals_notes.txt")
with open(ml_txt_path, "w", encoding="utf-8") as f:
    f.write(ML_TXT_CONTENT)
print(f"Created: {ml_txt_path}")


ML_CSV_DATA = [
    ["Topic", "Algorithm", "Type", "Description", "Use Case"],
    ["Supervised", "Linear Regression", "Regression",
     "Models the relationship between a dependent variable and one or more independent variables by fitting a linear equation. The model minimizes the sum of squared residuals (OLS). Assumptions include linearity, independence, homoscedasticity, and normality of residuals.",
     "Predicting house prices based on square footage, number of bedrooms, and location."],
    ["Supervised", "Logistic Regression", "Classification",
     "Despite its name, logistic regression is a classification algorithm. It uses the sigmoid function to map predictions to probabilities between 0 and 1. The decision boundary is linear. It can be extended to multi-class classification using softmax (multinomial logistic regression).",
     "Email spam detection: classify emails as spam or not spam based on features."],
    ["Supervised", "Decision Tree", "Both",
     "A tree-structured model that makes decisions by splitting data based on feature values. Each internal node represents a test on a feature, each branch represents the outcome, and each leaf node represents a class label or value. Splitting criteria include Gini impurity, entropy (information gain), and variance reduction.",
     "Customer churn prediction: determine which customers are likely to leave based on usage patterns."],
    ["Supervised", "Random Forest", "Both",
     "An ensemble of decision trees trained on random subsets of data and features (bagging). Each tree votes, and the majority vote (classification) or average (regression) determines the final prediction. Random forests reduce overfitting compared to single decision trees and handle high-dimensional data well.",
     "Credit risk assessment: evaluate loan applications using multiple financial features."],
    ["Supervised", "Support Vector Machine", "Classification",
     "SVM finds the optimal hyperplane that maximizes the margin between classes. It can handle non-linear boundaries using the kernel trick (RBF, polynomial, sigmoid kernels). Support vectors are the data points closest to the decision boundary. SVM works well in high-dimensional spaces.",
     "Image classification: distinguishing handwritten digits (0-9) in the MNIST dataset."],
    ["Supervised", "K-Nearest Neighbors", "Both",
     "A non-parametric, instance-based algorithm that classifies new data points based on the majority class of their K nearest neighbors in feature space. Distance metrics include Euclidean, Manhattan, and Minkowski. The choice of K affects the bias-variance tradeoff: small K = low bias/high variance, large K = high bias/low variance.",
     "Recommendation systems: suggest products similar to what a customer has purchased."],
    ["Unsupervised", "K-Means Clustering", "Clustering",
     "Partitions data into K clusters by iteratively assigning points to the nearest centroid and updating centroids. The algorithm minimizes within-cluster sum of squares (inertia). Limitations include sensitivity to initialization (use K-means++), assumption of spherical clusters, and the need to specify K in advance. Use the elbow method or silhouette score to choose K.",
     "Customer segmentation: group customers into segments based on purchasing behavior for targeted marketing."],
    ["Unsupervised", "PCA", "Dimensionality Reduction",
     "Principal Component Analysis reduces dimensionality by projecting data onto the directions of maximum variance (principal components). PCs are orthogonal linear combinations of original features. The first PC captures the most variance, the second the next most, and so on. Use scree plots to decide how many components to keep.",
     "Reducing 100 features to 10 principal components that capture 95% of the variance for visualization."],
    ["Ensemble", "Gradient Boosting", "Both",
     "Builds models sequentially, each new model correcting errors of the combined previous models. It uses gradient descent to minimize a loss function. XGBoost, LightGBM, and CatBoost are popular implementations with regularization, handling missing values, and GPU support. Gradient boosting often achieves state-of-the-art results on tabular data.",
     "Kaggle competitions: gradient boosting models frequently win competitions on structured data problems."],
    ["Deep Learning", "Neural Network", "Both",
     "Neural networks consist of layers of interconnected nodes (neurons). Each connection has a weight, and each neuron applies an activation function (ReLU, sigmoid, tanh). Training uses backpropagation with gradient descent to update weights. Deep networks (many layers) can learn hierarchical representations of data.",
     "Image recognition: CNNs for classifying images; NLP: RNNs/Transformers for text understanding."],
]

ml_csv_path = os.path.join(COURSE_DIR, "ML_algorithms_reference.csv")
with open(ml_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(ML_CSV_DATA)
print(f"Created: {ml_csv_path}")


print("\n✅ All sample course materials created successfully!")
