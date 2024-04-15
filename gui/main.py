import tkinter as tk
from tkinter import messagebox
import joblib

# Function to predict the outcome of the match
def predict_match():
    home_team = home_team_var.get()
    away_team = away_team_var.get()
    
    if home_team == '' or away_team == '':
        messagebox.showwarning("Warning", "Please select both teams.")
        return
    
    # Load the machine learning model
    model = joblib.load('football_prediction_model.pkl')
    
    # Make prediction using the loaded model
    prediction = model.predict([[home_team, away_team]])  # Assuming your model takes team names as input features
    
    # Show the prediction
    messagebox.showinfo("Prediction", f"The match between {home_team} and {away_team} is predicted to be a {prediction[0]}.")

# Create the main window
root = tk.Tk()
root.title("Football Match Prediction")
root.geometry("600x600")  # Set window size to 600x600 pixels

# Create labels and entry fields
label_home = tk.Label(root, text="Home Team:", font=("Arial", 14))
label_home.grid(row=0, column=0, padx=20, pady=10, sticky="e")

home_team_var = tk.StringVar()
<<<<<<< HEAD
home_team_option = tk.OptionMenu(root, home_team_var, '', "Arsenal", "Liverpool", "Chelsea")  # Add more teams as needed
=======
home_team_option = tk.OptionMenu(root, home_team_var, '', "Team A", "Team B", "Team C")  # Add more teams as needed
>>>>>>> dev
home_team_option.config(font=("Arial", 14))
home_team_option.grid(row=0, column=1, padx=20, pady=10)

label_away = tk.Label(root, text="Away Team:", font=("Arial", 14))
label_away.grid(row=1, column=0, padx=20, pady=10, sticky="e")

away_team_var = tk.StringVar()
<<<<<<< HEAD
away_team_option = tk.OptionMenu(root, away_team_var, '', "Manchester United", "Wolverhampton", "Manchester City")  # Add more teams as needed
=======
away_team_option = tk.OptionMenu(root, away_team_var, '', "Team X", "Team Y", "Team Z")  # Add more teams as needed
>>>>>>> dev
away_team_option.config(font=("Arial", 14))
away_team_option.grid(row=1, column=1, padx=20, pady=10)

# Create the predict button with adjusted appearance
predict_button = tk.Button(root, text="Predict", command=predict_match, font=("Arial", 14))
predict_button.grid(row=2, columnspan=2, padx=20, pady=10, sticky="ew")

# Run the main event loop
root.mainloop()
