import tkinter as tk
from tkinter import filedialog, messagebox

window = tk.Tk()
window.title('Self Destruct Text')
window.minsize(width=900, height=450)
window.config(padx=10, pady=10)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(3, weight=1)

# Remaining time variable
time_remaining = 0
initial_time = 0
timer_running = False
timer_id = None


def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Text Files', '.txt'), ('All Files', '.*')],
        title='Save As'
    )

    if file_path:
        try:
            with open(file_path, "w") as file:
                # Write text data to the chosen file
                file.write(text.get("1.0", tk.END))  # Get text from the text widget
            messagebox.showinfo("File Saved", f"File saved successfully at {file_path}")
            text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file:\n{e}")


# Update Timer Display
def update_timer():
    global time_remaining, timer_running, timer_id
    if time_remaining > 0:
        timer_label.config(text=f'Time Remaining: {time_remaining} seconds')
        time_remaining -= 1
        timer_id = window.after(1000, update_timer)
    else:
        timer_label.config(text='Times Up!')
        text.config(state='disabled')
        timer_running = False
        if not timer_running:
            save_file()


# Start Timer
def start_timer():
    global time_remaining, initial_time, timer_running
    difficulty = dif_select.get()
    if difficulty == 'Easy':
        initial_time = 10
    elif difficulty == 'Medium':
        initial_time = 7
    elif difficulty == 'Hard':
        initial_time = 5
    else:
        messagebox.showwarning('Select Difficulty', 'Please select a difficulty from the dropdown.')
        return

    # Set time_remaining to initial_time after difficulty selection
    time_remaining = initial_time
    timer_label.config(text=f'Time Remaining: {time_remaining} seconds')
    text.config(state='normal')
    reset_timer()


# Reset Timer Function
def reset_timer(event=None):
    global time_remaining, timer_running, timer_id
    # Reset Timer to initial time
    time_remaining = initial_time
    timer_label.config(text=f'Time Remaining: {time_remaining} seconds')
    if timer_running:
        # Cancels countdown if user types
        window.after_cancel(timer_id)
        timer_running = False
    # Start Timer after 1-second pause
    timer_id = window.after(1000, start_countdown)


def start_countdown():
    global timer_running
    if not timer_running:
        timer_running = True
        update_timer()


# Message Label
msg_label = tk.Label(
    window,
    text="Typing is dangerous... be sure you are ready!",
    font=('Open Sans', 22),
    fg='white',
    bg='#323132',
    anchor='center'
)
msg_label.grid(row=0, column=0, columnspan=3)

# Timer Label
timer_label = tk.Label(
    window,
    text='Timer Remaining: Not Started ∞', fg='red', font=('Open Sans', 16),
)
timer_label.grid(row=2, column=2, columnspan=2, sticky='nw', padx=10, pady=5)

# Text Input Window
text = tk.Text(
    window,
    width=60,
    height=10,
    background='#ffffff',
    foreground='#2d3d50',
    font=('Open Sans', 16),
    wrap=tk.WORD,
    state='disabled'
)
text.grid(row=1, column=0, rowspan=3, sticky='nsew', padx=10, pady=10)

# Bind Key Press to Text widget
text.bind('<KeyPress>', reset_timer)

# Save & Clear button
save_btn = tk.Button(text='Save & Clear', command=save_file, foreground='#517385')
save_btn.grid(row=4, column=0)

# Select Difficulty
difficulty_label = tk.Label(
    window,
    text='Select Difficulty',
    foreground="#ff7e79",
    background='#323132',
    font=('Open Sans', 16),
)
difficulty_label.grid(row=1, column=2, sticky='w', padx=10)

dif_select = tk.StringVar()
dif_select.set('Pick One')
ds_drop = tk.OptionMenu(window, dif_select, 'Easy', 'Medium', 'Hard')
ds_drop.grid(row=1, column=3, sticky='e')

# Start Timer Button
start_button = tk.Button(window, text='Start Typing', command=start_timer, bg='#ff7e79', fg='green')
start_button.grid(row=3, column=2)

window.mainloop()
