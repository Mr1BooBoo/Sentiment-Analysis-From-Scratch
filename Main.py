# -*- coding: utf-8 -*-
"""IRTM2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MAudl6fC6OIGMb7LgY7b9LWJuNpX-aIf

# Libraries
"""

import json
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

"""# Reading and arranging data"""

file_path = '/content/train_dataset.json'
with open(file_path, 'r') as json_file:
    dataset = json.load(json_file)

main_dict = dataset["conversation"]


#labels contains emotions
#data contains the text

initial_labels = []
og_data = []

for sub_dict in main_dict.values():
    for inner_dict in sub_dict:
        emotion = inner_dict.get('emotion')
        text = inner_dict.get('text')
        initial_labels.append(emotion)
        og_data.append(text)



# Create a mapping from emotions to numbers
emotion_mapping = {
    "neutral": 0,
    "joy": 1,
    "surprise": 2,
    "disgust": 3,
    "sadness": 4,
    "anger": 5,
    "fear": 6
}

labels = [emotion_mapping[emotion] for emotion in initial_labels]


del file_path,json_file,dataset,emotion,text,main_dict,sub_dict,inner_dict,initial_labels,emotion_mapping

"""# Data preprocessing"""

import re
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text)

    tokens = word_tokenize(text)
    filtered_text = [word for word in tokens if word.lower() not in stop_words]

    lemmatized_text = [lemmatizer.lemmatize(word) for word in filtered_text]

    cleaned_text = " ".join(lemmatized_text)

    return cleaned_text

data = [clean_text(phrase) for phrase in og_data]

"""# Check data integrity
***don't run this***
"""

for original, cleaned in zip(og_data[14:20], data[14:20]):
    print(f"Original: {original}\nCleaned: {cleaned}\n---")

print(len(data),len(labels))

print(set(labels))

"""# ML stuff"""

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

"""# SVC"""

svm_classifier = SVC(kernel='linear')
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001], 'kernel': ['linear']}
grid_search = GridSearchCV(svm_classifier, param_grid, refit=True, verbose=3, cv=3)
grid_search.fit(X_train_tfidf, y_train)
#svm_classifier.fit(X_train_tfidf, y_train)

best_params = grid_search.best_params_
print("Best Parameters:", best_params)

y_pred = grid_search.predict(X_test_tfidf)

print("Classification Report:")
print(classification_report(y_test, y_pred))

"""# Random Forest"""

rf_classifier = RandomForestClassifier()
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]}
grid_search = GridSearchCV(rf_classifier, param_grid, refit=True, verbose=3, cv=3)
grid_search.fit(X_train_tfidf, y_train)

best_params = grid_search.best_params_
print("Best Parameters:", best_params)

y_pred = grid_search.predict(X_test_tfidf)

print("Classification Report:")
print(classification_report(y_test, y_pred))

"""# NN LSTM"""

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(data)

vocab_size = len(tokenizer.word_index) + 1

sequences = tokenizer.texts_to_sequences(data)

max_sequence_length = 100

padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post', truncating='post')

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

X_train, X_test, y_train, y_test = train_test_split(padded_sequences, encoded_labels, test_size=0.2, random_state=42)

embedding_dim = 50  # Choose an appropriate embedding dimension
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_length),
    tf.keras.layers.LSTM(100),
    tf.keras.layers.Dense(7, activation='softmax')  # Adjust the number of units based on your number of classes
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test))

# Evaluate the model
y_pred_probabilities = model.predict(X_test)
y_pred = tf.argmax(y_pred_probabilities, axis=1)

"""# TASK 2 ⚡


"""

#pip install datasets

import json
from transformers import BertTokenizer, BertForSequenceClassification, BartForConditionalGeneration, BartTokenizer, AdamW
from torch.utils.data import DataLoader, Dataset
import torch
import torch.optim as optim
import pandas as pd
import nltk
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import load_metric
import numpy as np

def read_json_and_create_dataframes(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    utterance_rows = []
    pair_rows = []
    full_convo_texts = {}
    full_convo_texts_tagged = {}

    for conversation_id, conversation in data['conversation'].items():
        full_convo_texts[conversation_id] = ""
        full_convo_texts_tagged[conversation_id] = ""

        for utterance in conversation:
            full_convo_texts[conversation_id] += utterance["text"] + " "
            full_convo_texts_tagged[conversation_id] += f"{utterance['utterance_ID']}_{utterance['text']} "

            utterance_row = {
                "conversation_id": conversation_id,
                "utterance_id": utterance["utterance_ID"],
                "speaker": utterance["speaker"],
                "emotion": utterance["emotion"],
                "text": utterance["text"]
            }
            utterance_rows.append(utterance_row)

        if conversation_id in data['emotion-cause_pairs']:
            for pair in data['emotion-cause_pairs'][conversation_id]:
                emotion_id, cause_text = pair
                utterance_id, emotion = emotion_id.split("_")
                pair_row = {
                    "conversation_id": conversation_id,
                    "emotion_utterance_id": utterance_id,
                    "cause_text": cause_text
                }
                pair_rows.append(pair_row)

    df_utterances = pd.DataFrame(utterance_rows)
    df_pairs = pd.DataFrame(pair_rows)

    df_full_convos = pd.DataFrame(list(full_convo_texts.items()), columns=['conversation_id', 'full_conversation'])
    df_full_convos_tagged = pd.DataFrame(list(full_convo_texts_tagged.items()), columns=['conversation_id', 'full_conversation_tagged'])

    df_utterances['utterance_id'] = df_utterances['utterance_id'].astype(str)
    df_pairs['emotion_utterance_id'] = df_pairs['emotion_utterance_id'].astype(str)

    df_merged = pd.merge(df_utterances, df_pairs, how='left', left_on=['conversation_id', 'utterance_id'], right_on=['conversation_id', 'emotion_utterance_id'], suffixes=('', '_pair'))
    df_final = pd.merge(df_merged, df_full_convos, on='conversation_id', how='left')
    df_final = pd.merge(df_final, df_full_convos_tagged, on='conversation_id', how='left')

    df_final['cause_text'] = df_final['cause_text'].fillna('')

    df_final = df_final.drop(columns=['emotion_utterance_id'])

    return df_final

file_path = '/content/train_dataset.json'
file_path_test = '/content/test_dataset.json'

df_conversations = read_json_and_create_dataframes(file_path)
df_test_conversations = read_json_and_create_dataframes(file_path_test)

class EmotionCauseDatasetQA_BERT(Dataset):
    def __init__(self, dataframe, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.data = dataframe
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        full_conversation = row['full_conversation']
        text = f"{row['utterance_id']}_{row['text']}"
        cause_text = row['cause_text'] if pd.notnull(row['cause_text']) else ""

        inputs = self.tokenizer.encode_plus(
            f"{full_conversation} [SEP] {text} [SEP] ",
            None,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        input_ids = inputs['input_ids'].squeeze()
        attention_mask = inputs['attention_mask'].squeeze()
        labels = torch.tensor(1 if cause_text else 0, dtype=torch.long)

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

class EmotionCauseDatasetBART(Dataset):
    def __init__(self, dataframe, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.data = dataframe
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        full_conversation = row['full_conversation']
        target_phrase = f"{row['utterance_id']}_{row['text']}"
        cause_text = f"<EMOTION>{row['utterance_id']}_{row['emotion']}<CAUSE>{row['cause_text']}" if pd.notnull(row['cause_text']) else '<NO_CAUSE>'

        prompt = f"Given the following conversation where each phrase is labeled with its ID: {full_conversation}. Considering the specific statement: '{target_phrase}', with its emotion, identify and label the part of the conversation that likely caused this emotion."

        inputs = self.tokenizer(prompt, return_tensors="pt", padding="max_length", truncation=True, max_length=self.max_length)
        targets = self.tokenizer(cause_text, return_tensors="pt", padding="max_length", truncation=True, max_length=self.max_length)

        input_ids = inputs["input_ids"].squeeze()
        attention_mask = inputs["attention_mask"].squeeze()
        labels = targets["input_ids"].squeeze()
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

def train_bart_model(model, dataloader, device, epochs=2):
    optimizer = AdamW(model.parameters(), lr=5e-5)

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch_idx, batch in enumerate(dataloader):
            batch = {k: v.to(device) for k, v in batch.items()}

            outputs = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'], labels=batch['labels'])
            loss = outputs.loss
            total_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (batch_idx + 1) % 10 == 0:
                print(f"Epoch {epoch+1}, Batch {batch_idx+1}/{len(dataloader)}, Loss: {loss.item()}")

        avg_train_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}, Average Loss: {avg_train_loss}")

def safe_decode_predictions(token_ids, tokenizer):
    token_ids = token_ids[token_ids != -100]
    return tokenizer.decode(token_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)

def evaluate_predictions_on_id(predictions, true_labels):
    def extract_id(text):
        id_end_index = text.find('_')
        if id_end_index != -1:
            return text[:id_end_index].strip()
        return ''

    correct_count = 0
    total_count = len(predictions)

    for pred, true in zip(predictions, true_labels):
        pred_id = extract_id(pred)
        true_id = extract_id(true)

        if pred_id == true_id:
            correct_count += 1

    accuracy = correct_count / total_count if total_count > 0 else 0
    print(f"Accuracy based on ID comparison: {accuracy:.4f} ({correct_count}/{total_count})")

def evaluate_bart_model(model, dataloader, device):
    model.eval()
    predictions, true_labels = [], []

    for batch_idx, batch in enumerate(dataloader):
        batch = {k: v.to(device) for k, v in batch.items()}
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']

        outputs = model.generate(input_ids, attention_mask=attention_mask)
        pred_texts = [safe_decode_predictions(g, tokenizer) for g in outputs]
        true_texts = [safe_decode_predictions(t.cpu().numpy(), tokenizer) for t in batch['labels']]

        predictions.extend(pred_texts)
        true_labels.extend(true_texts)

        if (batch_idx + 1) % 10 == 0:
            print(f"Evaluating Batch {batch_idx+1}/{len(dataloader)}")
    exact_matches = sum([1 for pred, true in zip(predictions, true_labels) if pred == true])
    exact_match_rate = exact_matches / len(predictions)
    print(f"Exact Match Rate: {exact_match_rate}")
    evaluate_predictions_on_id(predictions, true_labels)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_bart = BartForConditionalGeneration.from_pretrained('facebook/bart-base')
tokenizer_bart = BartTokenizer.from_pretrained('facebook/bart-base')
model_bart.to(device)

train_dataset_bart = EmotionCauseDatasetBART(df_conversations, tokenizer_bart)
train_dataloader_bart = DataLoader(train_dataset_bart, batch_size=4, shuffle=True)

test_dataset_bart = EmotionCauseDatasetBART(df_test_conversations, tokenizer_bart)
test_dataloader_bart = DataLoader(test_dataset_bart, batch_size=4)

# Train and evaluate
train_bart_model(model_bart, train_dataloader_bart, device, epochs=2)
evaluate_bart_model(model_bart, test_dataloader_bart, device)

