import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn import linear_model

# Load and preprocess data
data = pd.read_csv("GaltonFamilies.csv")
data = data.drop(["rownames", "family", "midparentHeight", "children", "childNum"], axis=1)
data["gender"] = data["gender"].map({"male": 1, "female": 0})
data = data.sample(frac=1).reset_index(drop=True)  # Shuffle and reset index

# Train the regression model
train_dataset, test_dataset = data[:800], data[800:]
train_data, train_label = train_dataset.drop(["childHeight"], axis=1), train_dataset["childHeight"]
test_data, test_label = test_dataset.drop(["childHeight"], axis=1), test_dataset["childHeight"]
regr = linear_model.LinearRegression()
regr.fit(train_data, train_label)


# Function to predict child height
def predict_height():
    try:
        # Get inputs
        father_height = float(father_height_entry.get())
        mother_height = float(mother_height_entry.get())
        gender = gender_var.get()

        # Prepare input data
        input_data = np.array([[father_height, mother_height, gender]])
        predicted_height = regr.predict(input_data)[0]

        # Display result
        result_label.config(text=f"Predicted Child Height: {predicted_height:.2f} inches")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for heights.")


# Function to convert cm to inches
def convert_to_inches():
    try:
        cm_value = float(cm_entry.get())
        inches = cm_value / 2.54
        cm_to_in_label.config(text=f"Converted: {inches:.2f} inches")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for cm.")


# Function to convert inches to cm
def convert_to_cm():
    try:
        inch_value = float(inch_entry.get())
        cm = inch_value * 2.54
        in_to_cm_label.config(text=f"Converted: {cm:.2f} cm")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for inches.")


# Create the UI
root = tk.Tk()
root.title("Height Predictor")
root.geometry("400x600")

# Input fields for heights
tk.Label(root, text="Father's Height (in inches):").pack(pady=5)
father_height_entry = tk.Entry(root)
father_height_entry.pack()

tk.Label(root, text="Mother's Height (in inches):").pack(pady=5)
mother_height_entry = tk.Entry(root)
mother_height_entry.pack()

# Gender selection
tk.Label(root, text="Child's Gender:").pack(pady=5)
gender_var = tk.IntVar(value=1)  # Default to male (1)
ttk.Radiobutton(root, text="Male", variable=gender_var, value=1).pack()
ttk.Radiobutton(root, text="Female", variable=gender_var, value=0).pack()

# Predict button
predict_button = tk.Button(root, text="Predict Child Height", command=predict_height)
predict_button.pack(pady=10)

# Result display
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Conversion: cm to inches
tk.Label(root, text="Convert cm to inches:").pack(pady=10)
cm_entry = tk.Entry(root)
cm_entry.pack()
convert_to_inches_button = tk.Button(root, text="Convert to Inches", command=convert_to_inches)
convert_to_inches_button.pack(pady=5)
cm_to_in_label = tk.Label(root, text="")
cm_to_in_label.pack(pady=5)

# Conversion: inches to cm
tk.Label(root, text="Convert inches to cm:").pack(pady=10)
inch_entry = tk.Entry(root)
inch_entry.pack()
convert_to_cm_button = tk.Button(root, text="Convert to CM", command=convert_to_cm)
convert_to_cm_button.pack(pady=5)
in_to_cm_label = tk.Label(root, text="")
in_to_cm_label.pack(pady=5)

# Run the application
root.mainloop()
