import os
import sys
from tkinter import Tk, Canvas, Button, Frame, filedialog, Text, Entry
from PIL import Image, ImageTk
import json
import webbrowser

class ImageCropper:
    def __init__(self, input_folder, output_folder, website):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
        self.image_files.sort()
        self.current_image_index = 0
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.img = None
        self.tk_img = None
        self.crop_count = 0

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        self.root = Tk()
        self.root.title("Image Cropper")

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True, side="left")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        button_frame = Frame(self.root, bg="lightgray")
        button_frame.pack(fill="y", side="right")

        self.submit_button = Button(button_frame, text="Submit Crop", command=self.submit_crop)
        self.submit_button.grid(row=0, column=0, padx=10, pady=10)

        self.submit_full_button = Button(button_frame, text="Submit Full", command=self.submit_full)
        self.submit_full_button.grid(row=1, column=0, padx=10, pady=10)

        self.next_image_button = Button(button_frame, text="Next Image", command=self.next_image)
        self.next_image_button.grid(row=2, column=0, padx=10, pady=10)

        self.comment_entry = Entry(button_frame, font=("Arial", 12), width=40)
        self.comment_entry.grid(row=3, pady=10)

        self.add_comment_button = Button(button_frame, text="Comment", command=self.save_comment)
        self.add_comment_button.grid(row=4, padx=10, pady=5)

        self.load_image()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def load_image(self):
        if self.current_image_index >= len(self.image_files):
            print("All images processed.")
            self.root.destroy()
            return

        image_path = os.path.join(self.input_folder, self.image_files[self.current_image_index])
        self.img = Image.open(image_path)

        # original image
        original_width, original_height = self.img.size

        # calculate scale
        max_display_width = 1200  # 최대 표시할 창 너비
        max_display_height = 800  # 최대 표시할 창 높이
        scale_x = max_display_width / original_width
        scale_y = max_display_height / original_height
        self.image_scale = min(scale_x, scale_y, 1)  # 축소 비율 (1보다 크지 않도록 제한)

        # scaled image
        display_width = int(original_width * self.image_scale)
        display_height = int(original_height * self.image_scale)

        # resize
        self.display_image = self.img.resize((display_width, display_height), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(self.display_image)

        self.canvas.delete("all")
        self.canvas.config(width=display_width, height=display_height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.root.title(f"Cropping: {self.image_files[self.current_image_index]}")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y

        # original coordinates
        self.original_start_x = int(self.start_x / self.image_scale)
        self.original_start_y = int(self.start_y / self.image_scale)
        self.original_end_x = int(self.end_x / self.image_scale)
        self.original_end_y = int(self.end_y / self.image_scale)

        #print(f"Original Coordinates: ({self.original_start_x}, {self.original_start_y}) to ({self.original_end_x}, {self.original_end_y})")

    def submit_crop(self):
        coords = (self.original_start_x, self.original_start_y, self.original_end_x, self.original_end_y)
        cropped_img = self.img.crop(coords)

        # Convert mode if not supported by JPEG
        if cropped_img.mode not in ("RGB", "L"):
            cropped_img = cropped_img.convert("RGB")

        output_path = os.path.join(self.output_folder, f"cropped_{self.image_files[self.current_image_index].strip('.png')}_{self.crop_count}.png")
        cropped_img.save(output_path, "JPEG")
        print(f"Cropped image saved to {output_path}")

        self.crop_count += 1

    def submit_full(self):
        output_path = os.path.join(self.output_folder, f"full_{self.image_files[self.current_image_index]}")
        if self.img.mode not in ("RGB", "L"):
            full_img = self.img.convert("RGB")
        else:
            full_img = self.img

        full_img.save(output_path, "JPEG")
        print(f"Full image saved to {output_path}")

    def save_comment(self):
        comment = self.comment_entry.get().strip()
        if comment:
            comment_file = os.path.join(f"{website}_img_comments.txt")
            with open(comment_file, "a") as f:
                f.write('Index: ' + self.input_folder.split('/')[-1] + '\n' + 'Comment: ' + comment + "\n")
            print(f"Comment saved to {comment_file}")

    def next_image(self):
        self.current_image_index += 1
        self.crop_count = 0
        self.load_image()

    def on_close(self):
        print("Application closed.")
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    # input_folder = filedialog.askdirectory(title="Select Input Folder")
    # output_folder = filedialog.askdirectory(title="Select Output Folder")

    assert sys.argv[1] in ['vwo', 'mobbin']
    website = sys.argv[1]

    if len(sys.argv) > 2:
        st = int(sys.argv[2])
    
    folder_list = os.listdir(f'../../image/{website}')
    folder_list.sort(key=lambda x: int(x))

    if website == 'vwo':
        with open('../../vwo_success_stories.json', 'r') as f:
            data = json.load(f)
    else:
        with open('../../mobbin.json', 'r') as f:
            data = json.load(f)
    
    if len(sys.argv) > 2:
        folder_list = folder_list[st:]

    for folder in folder_list:
        input_folder = f'../../image/{website}/{folder}'
        output_folder = f'../../image/{website}_crop/{folder}'

        print(f'Opening {data[int(folder)]["analysis_url"]}...')
        webbrowser.open(data[int(folder)]['analysis_url'])
        
        print(f'Processing {input_folder}...')
        ImageCropper(input_folder, output_folder, website)
