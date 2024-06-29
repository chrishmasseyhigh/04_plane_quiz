from tkinter import *
from functools import partial
import csv
import random
from PIL import Image, ImageTk
import os
import re

class Mainpage:
    def __init__(self, master):
        self.master = master
        master.title("Plane Quiz")

        # Set up GUI Frame
        self.rounds_frame = Frame(master)
        self.rounds_frame.grid()

        # Header label
        Label(self.rounds_frame, text="Plane Quiz", font=("Arial", 16, "bold")).grid(row=0)

        # Instructions label
        instructions = "Instructions: In this quiz you will be displayed an image and " \
                       "you have to guess what plane it is and type the answer in the box.\n" \
                       "\nNames must be a nickname like tomcat or the name of the " \
                       "aircraft (no “-”) e.g. f14, 737, a320 ect.\n"\
                       "\nOn this page you will either enter rounds in the white box "\
                       "or choose to do infinite rounds."
        Label(self.rounds_frame, text=instructions, wrap=250, width=50, justify="left").grid(row=1)

        # Button frame for conversion and other actions
        self.button_frame = Frame(self.rounds_frame)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10)

        # Entry widget for user input
        self.rounds_entry = Entry(self.button_frame, font=("Arial", "18"), width=10)
        self.rounds_entry.grid(row=0, column=0, padx=2, pady=2)

        # Error message label
        self.output_label = Label(self.rounds_frame, text="", fg="#9C0000")
        self.output_label.grid(row=3)

        # Infinite mode button
        Button(self.button_frame, text="Inf Rounds", bg="#009900",
               fg="#FFFFFF", font=("Arial", "11", "bold"), width=10,
               command=lambda: self.to_play("inf")).grid(row=0, column=2, padx=2, pady=2)

        # Bind the Entry key to call the check_input method
        self.rounds_entry.bind("<Return>", lambda event: self.check_input())
    def check_input(self):
        player_rounds = self.num_check(1)
        if player_rounds != "invalid":
            self.to_play(player_rounds)

    def num_check(self, low_val):
        has_error = False
        error = f"Please enter a whole number higher than or\n " \
                f"equal to {low_val} with no other characters. "

        response = self.rounds_entry.get()

        try:
            rounds = int(response)
            if rounds <= low_val - 0.000001:
                has_error = True

        except ValueError:
            has_error = True

        if has_error:
            self.rounds_entry.config(bg="#D9544D")
            self.output_label.config(text=error)
            return "invalid"
        else:
            self.rounds_entry.config(bg="white")
            self.output_label.config(text="")
            return rounds

    def to_play(self, num_rounds):
        Play(self.master, num_rounds)
        # hide root window (i.e., hide rounds choice window)
        self.master.withdraw()

class Play:

    def __init__(self, master, how_many):
        self.master = master  # Store the master widget reference

        self.play_box = Toplevel()

        # If users press cross at top, closes help(releases help button)
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        # Variables used to work out stats when game ends
        self.rounds_wanted = how_many

        # initialy set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)


        #sets the win/ loss variables
        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        self.rounds_lost = IntVar()
        self.rounds_lost.set(0)

        # lists to hold user scores
        self.user_scores = []

        # Load plane images and create a list of available planes
        self.planes_list, self.available_planes = self.load_plane_images()

        # get all the colours for use in the game
        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading = "Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

        instructions = "What plane is this?"

        self.instructions_label = Label(self.quest_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame)
        self.rounds_frame.grid(row=4, pady=5)

        # Button frame for conversion and other actions
        self.button_frame = Frame(self.rounds_frame)
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        # Initialize plane image label
        self.plane_image_label = Label(self.rounds_frame)
        self.plane_image_label.grid(row=0)

        # gets user input/ gets what plane they chose
        self.planes_entry = Entry(self.rounds_frame, font=("Arial", "18"), width=26)
        self.planes_entry.grid(row=1, column=0, padx=2, pady=5)

        # Tell player if their right or wrong and displays errors
        self.message_label = Label(self.rounds_frame, text="", fg="white")
        self.message_label.grid(row=3)

        # Call new_round after defining next_button
        self.new_round()

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["green", "Finish Quiz", "finish quiz"]
        ]

        # lists to hold refrences for control buttons
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=10, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5)

            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        self.help_button = self.control_button_ref[0]

        # Create the stats button
        self.to_stats_btn = Button(self.control_frame,
                                   fg="#FFFFFF",
                                   bg=control_buttons[1][0],
                                   text=control_buttons[1][1],
                                   width=10, font=("Arial", "12", "bold"),
                                   command=lambda: self.to_do("get stats"),
                                   state=DISABLED)
        self.to_stats_btn.grid(row=0, column=1, padx=5)

        # Binds planes_entry to quiz_input function
        self.planes_entry.bind("<Return>", lambda event: self.check_input())

    # loads plane images and creates a list of names and image id
    def load_plane_images(self):

        # lists to hold plane data
        planes_list = {}

        with open("planes.csv", "r") as file:
            reader = csv.reader(file)
            # skips the first row
            next(reader)
            for row in reader:
                designation = row[0]
                nickname = row[1]
                image_filename = row[2]
                planes_list[designation] = {"nickname": nickname, "image_filename": image_filename}

        return planes_list, list(planes_list.keys())

    #set up new images, inf mode and removes items from  list when picked
    def new_round(self):
        # sets total rounds and times amount of rounds played to
        # rounds to make inf if inf mode is pressed
        self.total_rounds = 2

        if self.rounds_wanted == 'inf':
            self.total_rounds += 10 * self.rounds_played.get()
        else:
            self.total_rounds = self.rounds_wanted

        # Check if the number of rounds played equals the number of rounds wanted + 1
        if self.rounds_played.get() == self.total_rounds:
            # Disable the entry box if the condition is met
            self.planes_entry.config(state=DISABLED)
            self.planes_entry.unbind("<Return>")
            self.instructions_label.config(text="Game Over")
            return

        else:
            # Check if all planes have been displayed and reset if needed
            if not self.available_planes:
                self.available_planes = list(self.planes_list.keys())
                self.planes_displayed = 0

            # Select a random plane from the available planes
            self.plane_designation = random.choice(self.available_planes)
            plane_data = self.planes_list[self.plane_designation]
            image_filename = plane_data["image_filename"]
            image_path = os.path.join("Plane_Images", image_filename)

            # Remove the chosen plane from the available planes list
            self.available_planes.remove(self.plane_designation)

            # Open and display the new plane images
            plane_image = Image.open(image_path)
            self.plane_photo = ImageTk.PhotoImage(plane_image)
            self.plane_image_label.config(image=self.plane_photo)

            # Enable the stats button if at least one round has been played
            if self.rounds_played.get() >= 1:
                self.to_stats_btn.config(state=NORMAL)

            # retrieve number of rounds wanted / played
            # and update heading.
            how_many = self.rounds_wanted
            current_round = self.rounds_played.get()
            new_heading = "Choose - Round {} of " \
                          "{}".format(current_round + 1, how_many)
            self.choose_heading.config(text=new_heading)

    def check_input(self):
        user_input = self.planes_entry.get().strip().lower()
        error = self.check_input_validity(user_input)
        if error:
            # if there is an error display it
            self.planes_entry.config(bg="#D9544D")
            self.message_label.config(fg="#D9544D", text=error)
        else:
            # If the input is valid pass it on to the quiz input function
            self.quiz_input(user_input)

    def check_input_validity(self, input_text):
        # Check if the input is empty
        if not input_text:
            problem =("Please enter something.")
            return problem

        valid_char = "[A-Za-z0-9 ]"

        # iterates though filename and checks each letter
        for letter in input_text:
            # If the character is valid, continue checking the next character
            if re.match(valid_char, letter):
                continue
            else:
                # If an invalid character is found, set the problem message
                problem = ("Sorry, no '{}'s allowed".format(letter))
                return problem

    def quiz_input(self, user_input):
        # Adds one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)
        
        # gets plane info
        plane_data = self.planes_list[self.plane_designation]
        designation = self.plane_designation.lower()
        nickname = plane_data["nickname"].lower()

        # if answer is correct
        if user_input == designation or user_input == nickname:
            self.planes_entry.config(bg="#98FB98")
            self.message_label.config(fg="green", text="Correct!!")
            self.new_round()
            self.rounds_won.set(self.rounds_won.get() +1)
            return "valid"

        # if answer is incorrect
        else:
            self.planes_entry.config(bg="#D9544D")
            self.message_label.config(fg="#D9544D", text="Wrong answer was {}".format(designation))
            self.new_round()
            self.rounds_lost.set(self.rounds_lost.get() +1)
            return "invalid"



    # Detects which 'control' button was pressed and
    # invokes necessary function.  Can possibly replace functions
    # with calls to classes in this section!
    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            DisplayStats(self, self.rounds_won, self.rounds_lost, self.rounds_played)
        else:
            self.close_play()

    def get_stats(self):
        print("You chose to get the statistics")

    def get_help(self):
        # Call DisplayHelp class to display help dialog
        DisplayHelp(self.master)

    def close_play(self):
        # end current game and allow new game to start
        self.master.deiconify()
        self.play_box.destroy()

# show users help / game tips:
class DisplayHelp:

    def __init__(self, partner):

        background = "#ffe6cc"
        self.help_box = Toplevel()

        # Disable the help button in the partner Converter instance
        partner.help_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=500, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, bg=background,
                                        text="--- Help ---",
                                        font=("Arial", "18", "bold"))
        self.help_heading_label.grid(row=0)
        help_text = """Welcome to the Plane Quiz! This application tests your knowledge of different types of aircraft. Below are the instructions on how to play the game:

**Game Objective:**
Your objective is to identify the name of the airplane displayed in the image. 
You need to type the name of the airplane in the text box provided. Names should be either the official designation of the aircraft (e.g., "A320", "737") or a commonly used nickname (e.g., "Tomcat", "Flanker").

**Playing the Game:**
- In each round, an image of an airplane will be displayed along with the question "What plane is this?"
- Type your answer in the text box below the image and press Enter.
- If your answer is correct, the text box will turn green and display "Correct".
- If your answer is incorrect, the text box will turn red and display the correct answer.

**Control Buttons:**
- *Help*: Click on this button to view these instructions again.
- *Statistics*: Click on this button to view your game statistics, including the number of correct and incorrect answers, and the percentage. It also includes an option to save the statistics to a file.
- *Finish Quiz*: Click on this button to finish the quiz and return to the main menu.

**Game Over:**
The game ends when you have completed all rounds or clicked "Finish Quiz". You can start a new game by entering the number of rounds or pressing the "Infinite Rounds" button.

Enjoy playing the Plane Quiz and test your knowledge of airplanes!
"""
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wrap=600,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=18, pady=18)

    # closes help dialouge ( used by button and x at top of dialouge)
    def close_help(self, partner):
        self.help_box.destroy()
        # Enable the help button in the partner Converter instance
        partner.help_button.config(state=NORMAL)

class DisplayStats:
    def __init__(self, partner, rounds_won, rounds_lost, rounds_played):
        self.stats_box = Toplevel()

        stats_bg_colour = "#DAE8FC"

        partner.to_stats_btn.config(state=DISABLED)

        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=400,
                                 height=200, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame,
                                        text="Statistics",
                                        font=("Arial", "14", "bold"),
                                        bg=stats_bg_colour)
        self.help_heading_label.grid(row=0)

        stats_text = "Here are your game stats"
        self.help_text_label = Label(self.stats_frame, text = stats_text,
                                     justify="left",bg=stats_bg_colour)
        self.help_text_label.grid(row=1,padx=10)

        # frame to hold stats table
        self.data_frame = Frame(self.stats_frame,bg=stats_bg_colour,
                                borderwidth=1, relief="solid")
        self.data_frame.grid(row=2,padx=10,pady=10)

        # get stats for user
        rounds_won_value = rounds_won.get()
        rounds_lost_value = rounds_lost.get()
        rounds_played_value = rounds_played.get()
        percentage_won = (rounds_won_value / rounds_played_value) * 100 if rounds_played_value != 0 else 0
        percentage_lost = 100 - percentage_won

        # background for formating
        odd_rows = "#C9D6E8"
        even_rows = stats_bg_colour
        
        # sets up row formats   
        row_formats = [ odd_rows, even_rows, odd_rows]

        # Define rows
        main_header_list =["","Won","Lost"]
        totals_row_list =["Total",rounds_won_value,rounds_lost_value]
        percentage_row_list = ["Percentages",percentage_won,percentage_lost]
        
        # data for all labels
        all_labels = []

        count =0
        for item in range(0, 3):
            all_labels.append([main_header_list[item],  row_formats[count]])
            all_labels.append([totals_row_list[item],  row_formats[count]])
            all_labels.append([percentage_row_list[item],  row_formats[count]])
            count += 1

        # create labels based on list above
        for item in range(0, len(all_labels)):
            self.data_label = Label(self.data_frame, text=all_labels[item][0],
                                    bg=all_labels[item][1],
                                    width="10", height="2", padx=5
                                    )
            self.data_label.grid(row=item // 3,
                                 column=item % 3,
                                 padx=0, pady=0)

        # dismiss button
        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=6, column=0, columnspan=5, padx=10, pady=5)

    
    def close_stats(self, partner):
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()

if __name__ == "__main__":
    root = Tk()
    my_game = Mainpage(root)
    root.mainloop()
