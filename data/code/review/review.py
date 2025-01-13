import tkinter as tk
import webbrowser
import json
import sys

assert sys.argv[1] in ['goodui', 'vwo', 'mobbin']
website = sys.argv[1]

if sys.argv[1] == 'goodui':
    with open('../../goodui_leaks.json', 'r') as f:
        data = json.load(f)
elif sys.argv[1] == 'vwo':
    with open('../../vwo_success_stories.json', 'r') as f:
        data = json.load(f)
else:
    with open('../../mobbin.json', 'r') as f:
        data = json.load(f)

websites = []
for idx, leak in enumerate(data):
    websites.append(leak['analysis_url'])

# Index to track the current website
if len(sys.argv) > 2:
    current_index = int(sys.argv[2])
else:
    current_index = 0

# File to save comments
comment_file = f"{website}_comments.txt"

def save_comment():
    """Save the comment for the current website."""
    global current_index
    comment = comment_entry.get()
    if comment.strip():
        with open(comment_file, "a") as f:
            f.write(f"Index: {current_index - 1}\nWebsite: {websites[current_index - 1]}\nComment: {comment}\n\n")
        print(f"Comment saved for {websites[current_index - 1]} : {comment}")
        comment_entry.delete(0, tk.END)

def open_next_website():
    """Open the next website and allow for a comment."""
    global current_index

    if current_index > 0:
        with open(comment_file, "a") as f:
            f.write(f"Index {current_index - 1} Reviewed\n\n")

    if current_index < len(websites):
        webbrowser.open(websites[current_index])
        current_index += 1
    else:
        label.config(text="All websites visited. Thank you!", fg="red")
        loop_finished = True
    

# Create the main application window
root = tk.Tk()
root.title("Website Opener")

# Set the size of the window
root.geometry("400x300")

# Create a label
label = tk.Label(root, text="Press the button to go to the next website", font=("Arial", 12))
label.pack(pady=20)

# Create a "Next" button
next_button = tk.Button(root, text="Next", command=open_next_website, font=("Arial", 12), bg="lightblue", fg="black", width=20, height=2)
next_button.pack(pady=20)

# Create an entry box for comments
comment_label = tk.Label(root, text="Enter your comment for this website:", font=("Arial", 12))
comment_label.pack(pady=10)

comment_entry = tk.Entry(root, font=("Arial", 12), width=40)
comment_entry.pack(pady=10)

# Create a "Save Comment" button
save_button = tk.Button(root, text="Save Comment", command=save_comment, font=("Arial", 12), bg="lightgreen", fg="black", width=20, height=2)
save_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()