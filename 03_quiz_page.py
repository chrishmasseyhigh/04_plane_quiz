from tkinter import *
from functools import partial
import csv
import random
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

        # Bind the Enter key to call the check_input method
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

        # Initialize count for planes displayed
        self.planes_displayed = 0

        # Variables used to work out stats when game ends
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # initialy set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user scores

        self.user_scores = []

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
        self.rounds_entry = Entry(self.rounds_frame, font=("Arial", "18"), width=26)
        self.rounds_entry.grid(row=1, column=0, padx=2, pady=5)


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

    def new_round(self):

        # Construct the absolute path to the directory containing the files
        directory_path = "C:/Users/hoggc0017/OneDrive - Massey High School/2024_school_work/Com 301/03_programing_assessment/Plane_Images"

        # Load the data from the CSV file into a dictionary
        planes_list = {}
        csv_file_path = "C:/Users/hoggc0017/OneDrive - Massey High School/2024_school_work/Com 301/03_programing_assessment/planes.csv"

        with open(csv_file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row
            for row in reader:
                designation = row[0]
                nickname = row[1]
                image_filename = row[2]
                planes_list[designation] = {"nickname": nickname, "image_filename": image_filename}

        # reset list if all planes have been chosen
        if self.planes_displayed == 53:
            self.chosen_planes = set()
            available_planes = planes_list

        # Select a random plane from the dictionary
        plane_designation = random.choice(list(planes_list.keys()))
        plane_data = planes_list[plane_designation]
        nickname = plane_data["nickname"]
        image_filename = plane_data["image_filename"]
        image_path = os.path.join(directory_path, image_filename)

        # Open and display the new plane image
        plane_image = Image.open(image_path)
        self.plane_photo = ImageTk.PhotoImage(plane_image)
        self.plane_image_label.config(image=self.plane_photo)

        # Increment the count of planes displayed
        self.planes_displayed += 1

        # Enable the stats button if at least one round has been played
        if self.rounds_played.get() >= 1:
            self.to_stats_btn.config(state=NORMAL)

        # retrieve number of rounds wanted / played
        # and update heading.
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = "Choose - Round {} of " \
                      "{}".format(current_round + 1, how_many)
        self.choose_heading.config(text=new_heading)

    # work if the game is over
    def to_compare(self):

        how_many = self.rounds_wanted.get()

        # Add one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)

        if current_round == how_many:
            # Change 'next' button to show overall
            # win / loss result and disable it
            self.next_button.config(state=DISABLED,
                                    text="finished")


            # change all colour button background to light grey
            for item in self.choice_button_ref:
                item['bg'] = "#C0C0C0"

        else:
            # enable next round button and update heading
            self.next_button.config(state=NORMAL)

    # Detects which 'control' button was pressed and
    # invokes necessary function.  Can possibly replace functions
    # with calls to classes in this section!
    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            DisplayStats(self, self.user_scores)
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

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, bg=background,
                                        text="Help / hints",
                                        font=("Arial", "18", "bold"))
        self.help_heading_label.grid(row=0)
        help_text = """ Your goal in this game is to beat the computer and you have an
    advantage-you get to chose the colour first. The points
    associated with the colours are based on the colours hex code. 
    The higher the value of the colour, the greater your score. 

    To see that statistics, click on the statistics button. Win the
    game by scoring more that the computer overall. Don't be
    discouraged if you don't win every round, it's your overall score
    that counts. 

    Good luck! Chose carefully.."""
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wrap=350,
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
    def __init__(self, partner, user_scores):
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
        self.user_stats = self.get_stats(user_scores,"User")

        # background for formating
        head_back = "#FFFFFF"
        odd_rows = "#C9D6E8"
        even_rows = stats_bg_colour

        row_names = ["", "Total", "Best Score", "Worst Score", "Average Score"]
        row_formats = [head_back, odd_rows, even_rows, odd_rows, even_rows]

        # data for all labels
        all_labels = []

        count = 0
        for item in range(0, len(self.user_stats)):
            all_labels.append([row_names[item], row_formats[count]])
            all_labels.append([self.user_stats[item], row_formats[count]])
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

    @staticmethod
    def get_stats(score_list, entity):
        total_score = sum(score_list)
        best_score = max(score_list)
        worst_score = min(score_list)
        average = total_score / len(score_list)
        rounded_average = round(average, 1)

        return [entity, total_score, best_score, worst_score, rounded_average]

    def close_stats(self, partner):
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()

if __name__ == "__main__":
    root = Tk()
    my_game = Mainpage(root)
    root.mainloop()
