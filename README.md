# Sentiment-Analysis-From-Scratch

Sentiment analysis is a natural language processing (NLP) task that involves determining the sentiment expressed in a piece of text. This documentation explores the application of sentiment analysis on chat conversations, specifically classifying each message into one of seven basic emotions: Anger, Disgust, Fear, Joy, Sadness, Surprise, or Neutral. The analysis utilizes a variety of machine learning algorithms, including Support Vector Classifier (SVC), Random Forest (RF), and Long Short-Term Memory (LSTM) networks.  
The dataset used for this sentiment analysis project consists of chat conversations, each conversation is represented in a JSON format, containing information about the conversation ID, utterance ID, text, speaker, and the emotion associated with each utterance. The dataset comprises a diverse range of emotions expressed in various conversational contexts.  
  
The initial step involves reading and parsing the JSON-formatted dataset. The json library in Python is used to load the dataset into a Python data structure. In the provided example, the dataset is assumed to have a structure where each conversation has a unique ID, and each conversation contains a list of utterances.  

- Data cleaning is essential to ensure the text is in a suitable format for analysis. Common text cleaning techniques are applied to the extracted text, including: Lowercasing Transforming all text to lowercase ensures consistency and reduces the complexity of the data.  
- Punctuation Removal is beneficial for text analysis as it helps the algorithm focus on the meaningful words.  
- Tokenization: involves breaking down the text into individual words or tokens, enabling further analysis at the word level. Tokenization is particularly useful for preparing the text data for feature extraction or embedding.  
These data preprocessing steps collectively contribute to creating a clean and structured dataset suitable for training machine learning models for sentiment analysis. The cleaned and tokenized text data, along with corresponding emotion labels, serve as the input for the subsequent steps in the analysis pipeline, including feature extraction and model training.  

Subtask 0:  
Machine learning algorithms used to tackle the first subtask are the following:  
- Support Vector Classifier (SVC) is a powerful algorithm for text classification tasks. It works well in high-dimensional spaces and is effective for handling sparse data, making it suitable for NLP tasks.  
- Random Forest is an ensemble learning method that combines the predictions from multiple decision trees. It is robust, handles non-linear relationships well, and provides feature importances.  
Both algorithms were implemented with a wide range grid search to make sure that we test every single combination of parameters of each model and leave no excuse such as poor hyper-parameter tuning affecting the results.  
- LSTM networks are a type of recurrent neural network (RNN) well-suited for sequential data. They are effective in capturing long-term dependencies in text, making them suitable for sentiment analysis tasks.


shallow learning approaches fail to capture the patterns in human consciousness such as feelings and intention and are more robust to real patterns that follow more logical and mathematical rules. Besides that we can clearly see that traditional neural network approaches also don’t capture the human sentiments in text which leads us to a strong conclusion that this task requires far more complex models solely constructed for such task with an exceptional amount of data and computational power. There is one such algorithm that comes to one’s mind which is google’s Bert and Bart which we will use for the following subtask which is even more complicated than the first one.  


This subtask is even more complicated than the first one for it asks for the cause of a certain emotion rather than just detecting it from given words and expressions, which somewhat forces us to refuge to highly complex and highly trained models such as:  
BERT and BART:  
The solution for subtask1 starts by reading data from a JSON file containing detailed conversation information, including speaker IDs, expressed emotions, and emotion-cause pairs. Structured into tables, the data undergoes preprocessing, facilitating effective organization and manipulation. The subsequent phase involves encoding individual phrases and entire conversations into a numerical format suitable for machine learning models. This process, often
termed tokenization, transforms raw text into sequences of numerical tokens, making it amenable to computational analysis. Two distinct models, BERT and BART, are then leveraged for distinct
aspects of emotion comprehension. The training regimen exposes these models to a diverse array of examples from the dataset, enabling them to adjust internal parameters and optimize their
predictive capabilities. Evaluation is conducted on a separate dataset to gauge the models' proficiency in predicting emotions and discerning emotion-cause relationships within
conversations. The overarching objective is to cultivate models with a nuanced understanding of emotional dynamics, capable of identifying the intricate factors contributing to emotional states
in conversations. The code, while showcasing effective functionality, also points to potential areas for refinement and future enhancements. It underscores the ongoing efforts to fine-tune
these models, aiming for heightened accuracy in deciphering the nuanced emotional landscape inherent in diverse conversations.
The results are weak even using this method with 0.30 match rate which can be tested with higher epochs and more data/data augmentation
