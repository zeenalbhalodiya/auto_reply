import tkinter as tk
from tkinter import scrolledtext
import requests

API_URL = "http://127.0.0.1:8001/api/auto-reply/"

root = tk.Tk()
root.title("ChatBot")
root.geometry("500x600")
root.configure(bg="#f2f2f2")

# ====== Header ======
header = tk.Label(root, text="ChatBot Master", bg="#4CAF50", fg="white",
                  font=("Segoe UI", 16, "bold"), pady=12)
header.pack(fill="x")

# ====== Chat Display Area ======
chat_display = tk.Text(root, wrap='word', bg="white", fg="black", font=("Segoe UI", 12),
                       padx=10, pady=10, bd=0, relief="flat", state=tk.DISABLED)
chat_display.pack(padx=15, pady=(10, 5), fill="both", expand=True)

# ====== Input Section ======
input_frame = tk.Frame(root, bg="#f2f2f2")
input_frame.pack(padx=15, pady=10, fill="x")

user_input = tk.Entry(input_frame, font=("Segoe UI", 12), bd=2, relief="groove")
user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

send_button = tk.Button(input_frame, text="Send", bg="#4CAF50", fg="white",
                        font=("Segoe UI", 11), command=lambda: on_enter())
send_button.pack(side="right")

# ====== Chatbot Logic Variables ======
user_name = ""
asked_name = False
expecting_name = False
selected_color = ""

# ====== Functions ======
def add_message(message, sender="Bot", color="black", align="left"):
    chat_display.config(state=tk.NORMAL)

    if sender == "You":
        tag_name = "user_msg"
        chat_display.insert(tk.END, f"\n{sender}: {message}", tag_name)
        chat_display.tag_config(tag_name, justify="right", foreground="#007acc", font=("Segoe UI", 12, "bold"))
    elif sender == "Bot":
        if color != "black":
            before = "Thanks, "
            after = " to connect with us! 😊"
            chat_display.insert(tk.END, "\nBot: " + before)
            chat_display.insert(tk.END, user_name, color)
            chat_display.insert(tk.END, after)
            chat_display.tag_config(color, foreground=color, font=("Segoe UI", 12, "bold"))
        else:
            tag_name = "bot_msg"
            chat_display.insert(tk.END, f"\nBot: {message}", tag_name)
            chat_display.tag_config(tag_name, justify="left", foreground="#333333", font=("Segoe UI", 12))
    
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

def send_to_api(message):
    try:
        response = requests.post(API_URL, json={"message": message})
        if response.status_code == 200:
            return response.json().get("reply", "")
        else:
            return "⚠️ API Error."
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

def on_enter(event=None):
    global user_name, asked_name, expecting_name, selected_color

    message = user_input.get().strip()
    user_input.delete(0, tk.END)

    if not message:
        return

    add_message(message, sender="You", align="right")

    lower_msg = message.lower()

    if lower_msg in ["hi", "hello", "hii", "hiii"] and not asked_name:
        add_message("Hello, What is your good name?")
        asked_name = True
        expecting_name = True
        return

    if expecting_name:
        user_name = message
        add_message("Which is your favorite colour?")
        expecting_name = False
        return

    if lower_msg in ["blue", "green", "yellow", "pink", "red", "orange"]:
        selected_color = lower_msg
        add_message("", sender="Bot", color=selected_color)
        return

    reply = send_to_api(message)
    add_message(reply)

user_input.bind("<Return>", on_enter)

root.mainloop()
