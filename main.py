import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
import os
import sys
import time


# assume that files are small enough to fit into memory but there are a lot of them
def find_words(files, words):
    result = {}
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                for word in words:
                    if word in text:
                        if not result.get(word):
                            result[word] = set()
                        result[word].add(file)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
    return result

def combine_results(results):
    result = {}
    for r in results:
        for word, files in r.items():
            if not result.get(word):
                result[word] = set()
            result[word].update(files)
    return result

def find_words_threading(files, words, num_workers):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        file_batches = [files[i:i+num_workers] for i in range(0, len(files), num_workers)]
        fs = [executor.submit(find_words, files, words) for files in file_batches]
        wait(fs)
        
        results = [f.result() for f in fs]
        return combine_results(results)

def find_words_multiprocessing(files, words, num_workers):
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        file_batches = [files[i:i+num_workers] for i in range(0, len(files), num_workers)]
        fs = [executor.submit(find_words, files, words) for files in file_batches]
        wait(fs)
        
        results = [f.result() for f in fs]
        return combine_results(results)

def get_files(directory):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        sys.exit(1)
        
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        print(f"No files found in directory '{directory}'.")
        sys.exit(1)
        
    return files
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Source directory")
    parser.add_argument("-p", "--parallelism", type=int, default=4, help="Parallelism factor")
    parser.add_argument("-w", "--words", nargs="+", type=str, help="Multiple words to process")
    args = parser.parse_args()
    
    parallelism = args.parallelism
    
    words = args.words
    
    files = get_files(args.input)
    print(f"Found {len(files)} files to process.")
    
    time_start = time.time()
    result = find_words_threading(files, words, parallelism)
    time_end = time.time()
    print(f"Threading: {time_end - time_start} seconds")
    
    time_start = time.time()
    result = find_words_multiprocessing(files, words, parallelism)
    time_end = time.time()
    print(f"Multiprocessing: {time_end - time_start} seconds")
    
    
    if len(result) == 0:
        print(f"Not matches found")
    else:
        for word, files in result.items():
            print(f"Word {word} found in files:")
            for file in files:
                print(f"  {file}")
    