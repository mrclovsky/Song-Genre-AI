import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import spacy
import matplotlib.pyplot as plt
from bayes import Bayes
import pickle

words_to_delete = ['the', 'as', 'i', 'be', 'a', 'you', 'to', 'and', 'it', 'not', 'do', 'in', 'my', 'us', 'of',
                   'your', 'know', "'", 'so', 'love', 'but', 'no', 'yes', '?', 'he', 'she', 'we', 'make', 'if',
                   "'ve", 'want', '!', 'well', '"', 'could', 'from', 'would', "'s", 'at', '...', 'her', 'his',
                   'all', 'around', 'then', 'when', 'they', 'them', 'into', 'an', ':', 'their', 'those', 'these',
                   'this', 'mine', 'too', 'through', 'who', 'how', 'why', 'until', 'unless', 'that', 'with', 'on',
                   'or', 'will', "won't", "can't", "haven't", "isn't", 'have', 'what', 'by', 'there', 'here',
                   'which', 'whom', 'whose', 'some', 'than', 'like', 'also', 'because', '!', 'each', 'during', '(',
                   ')', '[', ']', u"\u2122", 'soon', 'although', 'however', 'let', 'get', 'go', 'come', 'can',
                   'take', 'our', '.', '..', '*', '_', '+', '/', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'b1', 'b2',
                   'b3', 'b4', 'b5', 'b6', 'b7', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'd1', 'd2', 'd3', 'd4', 'd5',
                   'd6', 'd7', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'g1',
                   'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']


def lemmatize_text(text):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])


def remove_words(text, words_to_delete):
    words = text.split()
    filtered_words = [word for word in words if word not in words_to_delete]
    return ' '.join(filtered_words)


def remove_num(text, word_to_delete):
    words = text.split()
    filtered_words = [word for word in words if word != word_to_delete]
    return ' '.join(filtered_words)


def remove_hyphenated_words(text):
    words = text.split()
    removed_words = [word for word in words if word.count("-") >= 2]
    filtered_words = [word for word in words if word.count("-") < 2]
    return ' '.join(filtered_words)

def convert_to_lowercase(text):
    return text.lower()

def manage_lyrics(lyric):
    lyric = lemmatize_text(lyric)
    lyric = convert_to_lowercase(lyric)
    lyric = remove_hyphenated_words(lyric)
    lyric = remove_words(lyric, words_to_delete)
    for i in range(10000):
        if i != 420:
            remove_num(lyric, str(i))
    return lyric

def output_window(song, window):
    new_window = tk.Toplevel(window)
    new_window.title("Song Genre AI")
    new_window.geometry("700x500")
    label = tk.Label(new_window, text="The genre of this song is: " + song)
    label.pack(pady=(10, 10))
    image = Image.open("plot.jpg")
    image = image.resize((640, 420))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(new_window, image=photo)
    label.pack()
    new_window.mainloop()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_path)

def submit_file():
    print("File submitted successfully")
    path = entry.get()
    with open(path, 'r') as file:
        content = file.read()
    with open("instance.pickle", "rb") as file:
        data = pickle.load(file)
    data.deserializeDictionaries('compressed_data.json.gz')
    lyric = manage_lyrics(content)

    probabilities = data.calculateOneSong(lyric)
    min_prob = min(probabilities.values())
    for prob in probabilities:
        probabilities[prob] -= min_prob

    total = sum(probabilities.values())
    for prob in probabilities:
        probabilities[prob] = round(probabilities[prob]/total * 100, 2)

    max_prob = max(probabilities.values())
    for key, value in probabilities.items():
        if value == max_prob:
            song = key

    plt.figure(figsize=(12, 6))
    plt.bar(probabilities.keys(), probabilities.values())
    plt.xlabel("Genre")
    plt.ylabel("Probability")
    plt.savefig('plot.jpg', format='jpg')
    plt.show()

    output_window(song, window)


window = tk.Tk()
window.title("Song Genre AI")
window.geometry("700x500")

image = Image.open("logo.png")
image = image.resize((300, 225))
photo = ImageTk.PhotoImage(image)

label = tk.Label(window, image=photo)
label.pack()

label = tk.Label(window, text="Choose txt file:")
label.pack(pady=(10, 10))

button = tk.Button(window, text="Browse files", command=browse_file)
button.pack(pady=(10, 10))

entry = tk.Entry(window, width=50)
entry.pack(pady=(10, 10))

button = tk.Button(window, text="Submit", command=submit_file)
button.pack(pady=(10, 10))

window.mainloop()