from tkinter import *
from PIL import Image, ImageTk
import os

class Mainpage:
    def __init__(self, master):
        self.master = master
        master.title("Plane Quiz")

        # Set up GUI Frame
        self.rounds_frame = Frame(master)
        self.rounds_frame.grid()

        # Header label
        Label(self.rounds_frame, text="Plane Quiz", font=("Arial", 16, "bold")).grid(row=0)

        # Initialize plane image label
        self.plane_image_label = Label(self.rounds_frame)
        self.plane_image_label.grid(row=1)

        # Button frame for conversion and other actions
        self.button_frame = Frame(self.rounds_frame)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10)

        # Entry widget for user input
        self.rounds_entry = Entry(self.button_frame, font=("Arial", "18"), width=10)
        self.rounds_entry.grid(row=0, column=0, padx=2, pady=2)

        # Bind the Enter key to call the check_input method
        self.rounds_entry.bind("<Return>", lambda event: self.check_input())

    def new_round(self, image_path):
        plane_image = Image.open(image_path)
        self.plane_photo = ImageTk.PhotoImage(plane_image)
        self.plane_image_label.config(image=self.plane_photo)

    def check_input(self):
        pass  # Add your input validation logic here

if __name__ == "__main__":
    root = Tk()
    my_game = Mainpage(root)

    # Construct the absolute path to the directory containing the files
    directory_path = "C:/Users/hoggc0017/OneDrive - Massey High School/2024_school_work/Com 301/03_programing_assessment/Plane_Images"

    # Construct the absolute path to the image file
    image_path = os.path.join(directory_path, "a380.jpg")

    # Construct the absolute path to the CSV file
    csv_path = os.path.join(directory_path, "planes.csv")

    my_game.new_round(image_path)  # Call new_round to display the image
    root.mainloop()


