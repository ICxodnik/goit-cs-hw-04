import argparse
import os
import random
import shutil
import requests
import re

def get_words_list():
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    
    response = requests.get(url)
    text = response.text
    
    all_words = re.findall(r'[a-z]+', text.lower(), re.IGNORECASE)
    unique_words = list(set(all_words))
    
    return unique_words

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-o", "--output", type=str, help="Output directory")
    parser.add_argument("-n", "--number", type=int, help="Number of files to generate")
    parser.add_argument("-w", "--words", type=int, help="Number of words per file")
    parser.add_argument("-uw", "--unique_words", type=int, help="Number of unique words per file")
    args = parser.parse_args()

    number = args.number
    words_per_file = args.words
    unique_words_per_file = args.unique_words
    output_dir = args.output
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    words = get_words_list()
    for i in range(number):
        unique_words = random.sample(words, unique_words_per_file)
        with open(f"{output_dir}/file_{i}.txt", "w") as f:
            for j in range(words_per_file):
                f.write(random.choice(unique_words) + " ")
