#import section
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Flower Box Section
################################################################################
#Name: Spandana Yendapally
#Date: 3/1/2025
#Description: This program reads a CSV file containing reviews and ratings, processes the reviews to extract useful information, 
#and saves the processed data to a new CSV file. It also generates a word cloud of the top 50 words used in the reviews 
#and a bar plot of the common parts of speech (POS) tags found in the reviews.
################################################################################

# Download necessary NLTK datafiles
nltk.download('punkt')  
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('stopwords')
nltk.download('punkt_tab')  

#Function Section:

# Function to clean the text
def clean_text(text):
    text = ''.join(char if char.isalnum() or char.isspace() or char in '.!?' else ' ' for char in text)
    return text

# Function to split the text into sentences
def split_sentences(text):
    sentences = []
    sentence = ''
    for char in text:
        if char in '.!?':
            sentence += char
            sentences.append(sentence.strip())
            sentence = ''
        else:
            sentence += char
    if sentence.strip():
        sentences.append(sentence.strip())
    return sentences

# Function to remove stop words from tokenized text
def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word.lower() not in stop_words]

# Function to process each review
def process_review(review):
    cleaned_text = clean_text(review)
    
    tokens = word_tokenize(cleaned_text) # Tokenize the text
    
    filtered_tokens = remove_stop_words(tokens) # Remove stop words
    
    tagged_tokens = pos_tag(filtered_tokens) # Tag the filtered tokens with their parts of speech (POS)
    
    tag_counts = Counter(tag for word, tag in tagged_tokens)
    
    most_common_pos = tag_counts.most_common(2) # Get the two most common POS tags
    
    num_words = len(filtered_tokens)
    num_sentences = len(split_sentences(cleaned_text))
    
    # Format the most common POS tags
    pos_1 = most_common_pos[0] if len(most_common_pos) > 0 else ("None", 0)
    pos_2 = most_common_pos[1] if len(most_common_pos) > 1 else ("None", 0)
    
    return {
        "Number of Words": num_words,
        "Number of Sentences": num_sentences,
        "Most Common POS Tag 1": pos_1[0],
        "Occurrences 1": pos_1[1],
        "Most Common POS Tag 2": pos_2[0],
        "Occurrences 2": pos_2[1]
    }

# Input Section:

# Reading the CSV file
input_file = 'Reviews.csv'
df = pd.read_csv(input_file)

# Initialize list for storing the results
results = []
word_freq = Counter()
pos_tag_2_counts = Counter()

#process section:
# Process each review in the CSV file
for index, row in df.iterrows():
    review = row['Review']
    rating = row.get('Rating', None)
    
    # Process the review using the process_review function
    processed_data = process_review(review)
    
    # Track word frequencies for word cloud
    word_freq.update(word_tokenize(clean_text(review)))
    
    # Track POS Tag 2 occurrences for the bar chart
    pos_tag_2_counts.update([processed_data['Most Common POS Tag 2']])
    
    # Append the processed data along with the rating and review text
    result = {
        "Rating": rating,
        "Review": review,
        **processed_data
    }
    
    results.append(result)

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

rating_review_df = results_df[['Rating', 'Review']]
pos_tag_analysis_df = results_df[['Number of Words', 'Number of Sentences', 'Most Common POS Tag 1', 'Occurrences 1', 'Most Common POS Tag 2', 'Occurrences 2']]

# Display the DataFrames separately but aligned
from IPython.display import display

#Output Section:
print("Rating and Review:")
display(rating_review_df)

print("\nPOS Tag Analysis:")
display(pos_tag_analysis_df)

# Save the DataFrame to a CSV file
output_file = 'processed_reviews.csv'
results_df.to_csv(output_file, index=False)

# Print confirmation
print(f"Results saved to {output_file}")

# Generate a Word Cloud for the top 50 words
wordcloud = WordCloud(width=800, height=400, max_words=50, background_color='white').generate_from_frequencies(word_freq)

# Display the Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Top 50 Words Used in Reviews', fontsize=16)
plt.show()

# Generate a bar plot for the most common POS Tag 2
plt.figure(figsize=(10, 5))
plt.bar(pos_tag_2_counts.keys(), pos_tag_2_counts.values(), color=['blue', 'orange', 'green', 'red', 'purple', 'brown'])
plt.xlabel('POS Tag', fontsize=12)
plt.ylabel('Occurrences', fontsize=12)
plt.title('Most Common POS Tag 2', fontsize=16)
plt.tight_layout()
plt.show()