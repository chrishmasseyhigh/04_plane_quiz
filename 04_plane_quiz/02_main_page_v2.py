from tkinter import *

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
        print(num_rounds)

if __name__ == "__main__":
    root = Tk()
    my_game = Mainpage(root)
    root.mainloop()
