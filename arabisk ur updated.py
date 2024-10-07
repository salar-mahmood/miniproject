# Import necessary libraries
import tkinter as tk  # For creating the GUI
import math  # For mathematical calculations (sin, cos, etc.)
import time  # For getting the current time

# Define the main clock class, inheriting from tk.Canvas
class RolexClock(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        # Initialize the canvas with a size of 400x400 pixels
        super().__init__(master, width=400, height=400, *args, **kwargs)
        # Set the background color to white and remove the border
        self.configure(bg='white', highlightthickness=0)
        # Call methods to create the watch face and hands
        self.create_watch_face()
        self.create_hands()
        # Start updating the clock
        self.update_clock()

    def create_watch_face(self):
        # Create the outer bezel of the watch (silver circle)
        self.create_oval(20, 20, 380, 380, fill='silver', width=2)
        # Create the inner dial of the watch (light blue circle)
        self.create_oval(40, 40, 360, 360, fill='#87CEEB', width=0)
        
        # Add the Rolex crown logo
        self.create_text(200, 100, text='👑', font=('Arial', 20), fill='gold')
        # Add the Rolex text
        self.create_text(200, 130, text='ROLEX', font=('Arial', 12, 'bold'), fill='gold')
        # Add the "OYSTER PERPETUAL" text
        self.create_text(200, 150, text='OYSTER PERPETUAL', font=('Arial', 8), fill='black')
        # Add the "DAY-DATE" text
        self.create_text(200, 170, text='DAY-DATE', font=('Arial', 8), fill='black')

        # Define Arabic numerals for hour markers (1 to 11)
        arabic_numbers = ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '١٠', '١١']  # No 12
        angle_step = 360 / 12  # Angle between each hour marker
        radius = 130  # Distance of numbers from the center
        
        # Place the hour markers around the dial
        for i, num in enumerate(arabic_numbers):
            # Calculate the angle for each number (shifted by -90 degrees to start at 12 o'clock)
            angle = math.radians((i + 1) * angle_step - 90)
            # Calculate x and y coordinates for each number
            x = 200 + radius * math.cos(angle)
            y = 200 + radius * math.sin(angle)
            # Create the text for each hour marker
            self.create_text(x, y, text=num, font=('Arial', 20), fill='black')

        # Create a rectangle for the date window
        self.date_window = self.create_rectangle(300, 170, 340, 210, fill='white', outline='black')
        # Create a text object for the date (to be updated later)
        self.date_text = self.create_text(320, 190, text='', font=('Arial', 12, 'bold'), fill='black')

        # Create a rectangle for the day of the week
        self.day_of_week_box = self.create_rectangle(160, 60, 240, 90, fill='white', outline='black')
        # Create a text object for the day of the week (to be updated later)
        self.day_of_week_text = self.create_text(200, 75, text='', font=('Arial', 12, 'bold'), fill='black')

    def create_hands(self):
        # Create the hour hand (black, width 6)
        self.hour_hand = self.create_line(200, 200, 200, 140, width=6, fill='black')
        # Create the minute hand (black, width 4)
        self.minute_hand = self.create_line(200, 200, 200, 120, width=4, fill='black')
        # Create the second hand (red, width 2)
        self.second_hand = self.create_line(200, 200, 200, 100, width=2, fill='red')

    def update_clock(self):
        try:
            # Get the current time (including fractional seconds for smooth movement)
            current_time = time.time()
            # Extract hours, minutes, and seconds from the current time
            hours = time.localtime(current_time).tm_hour
            minutes = time.localtime(current_time).tm_min
            seconds = current_time % 60  # This includes the fractional part for smooth movement

            # Calculate angles for each hand
            # Hour hand moves slightly with each minute
            hour_angle = math.radians((hours % 12) * 30 + (minutes / 2) - 90)
            # Minute hand moves every minute
            minute_angle = math.radians(minutes * 6 - 90)
            # Second hand moves smoothly (not just every second)
            second_angle = math.radians(seconds * 6 - 90)

            # Update the position of the hour hand
            self.coords(self.hour_hand, 200, 200, 200 + 60 * math.cos(hour_angle), 200 + 60 * math.sin(hour_angle))
            # Update the position of the minute hand
            self.coords(self.minute_hand, 200, 200, 200 + 80 * math.cos(minute_angle), 200 + 80 * math.sin(minute_angle))
            # Update the position of the second hand
            self.coords(self.second_hand, 200, 200, 200 + 100 * math.cos(second_angle), 200 + 100 * math.sin(second_angle))

            # Get the current day of the month
            day_of_month = time.localtime(current_time).tm_mday
            # Update the date text
            self.itemconfig(self.date_text, text=str(day_of_month))

            # Define the Arabic days of the week in reverse order (Sunday to Monday)
            arabic_days = ['الأحد', 'السبت', 'الجمعة', 'الخميس', 'الأربعاء', 'الثلاثاء', 'الاثنين']
            # Get the current day of the week (0 = Monday, 6 = Sunday)
            day_of_week = time.localtime(current_time).tm_wday
            # Update the day of the week text (6 - day_of_week to reverse the order)
            self.itemconfig(self.day_of_week_text, text=arabic_days[6 - day_of_week])

            # Schedule the next update in 50 milliseconds (for smooth movement)
            self.after(50, self.update_clock)
        except Exception as e:
            # Print any errors that occur during the update
            print(f"Error updating clock: {e}")

# This block only runs if the script is executed directly (not imported)
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Set the window title
    root.title("Rolex Day-Date Clock")
    # Create an instance of the RolexClock
    clock = RolexClock(root)
    # Add the clock to the window
    clock.pack()
    # Start the main event loop
    root.mainloop()