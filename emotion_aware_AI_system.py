import cv2
import time
import threading
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, scrolledtext
from deepface import DeepFace
from textblob import TextBlob
import speech_recognition as sr

# ----------------------------- Emotion Analysis via Camera -----------------------------
def analyze_emotions():
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    emotions_count = {}

    while time.time() - start_time < 20:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
            emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
            cv2.putText(frame, emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
        except:
            pass
        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return emotions_count

# ----------------------------- Mental Health Report -----------------------------
def generate_report(emotions_count):
    total = sum(emotions_count.values())
    if total == 0:
        report = "No emotions detected. Try again."
        emoji = "😶"
    else:
        dominant = max(emotions_count, key=emotions_count.get)
        report = f"Your dominant emotion: {dominant}.\nMental Health Status: "
        if dominant in ['happy', 'neutral']:
            report += "Stable mental state. Keep it up! 😊"
            emoji = "😊"
        elif dominant in ['sad', 'fear', 'angry']:
            report += "You may be feeling low or stressed. Take care 💙"
            emoji = "😢"
        else:
            report += "Mixed feelings detected. Stay mindful 💭"
            emoji = "🤔"

    show_popup("Mental Health Report", report, emoji)

# ----------------------------- Text Sentiment Analysis -----------------------------
def analyze_text_logic(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        status = "You're feeling good! Keep the positivity up! 😊"
        emoji = "😄"
    elif polarity < -0.2:
        status = "You're feeling low. Please take care of yourself. 💙"
        emoji = "😢"
    else:
        status = "You're feeling neutral. Stay mindful. 🤔"
        emoji = "😐"

    show_popup("Text Emotion Analysis", status, emoji)

# ----------------------------- Text Chatbot Interface -----------------------------
def analyze_text_chat():
    root = tk.Tk()
    root.withdraw()

    chat_window = Toplevel(root)
    chat_window.title("Mental Health Chatbot")
    chat_window.geometry("500x500")
    chat_window.configure(bg="#f0f0f0")

    Label(chat_window, text="How are you feeling today? 💬", font=("Arial", 13), bg="#f0f0f0").pack(pady=5)

    chat_display = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, font=("Arial", 11), state="disabled", width=60, height=20)
    chat_display.pack(pady=10, padx=10)

    user_input = tk.Entry(chat_window, font=("Arial", 12), width=45)
    user_input.pack(pady=5, side=tk.LEFT, padx=(20, 5))

    messages = []

    def generate_bot_reply(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.2:
            return "That's great to hear! 😊"
        elif polarity < -0.2:
            return "I'm sorry you're feeling that way. I'm here to listen. 💙"
        else:
            return "Thanks for sharing. Would you like to talk more?"

    def send_message():
        msg = user_input.get().strip()
        if msg:
            messages.append(msg)
            bot_reply = generate_bot_reply(msg)
            chat_display.config(state="normal")
            chat_display.insert(tk.END, f"You: {msg}\n")
            chat_display.insert(tk.END, f"Bot: {bot_reply}\n\n")
            chat_display.config(state="disabled")
            chat_display.yview(tk.END)
            user_input.delete(0, tk.END)

    def finish_chat():
        chat_window.destroy()
        full_text = ' '.join(messages)
        analyze_text_logic(full_text)

    tk.Button(chat_window, text="Send", font=("Arial", 11), bg="#2196f3", fg="white", command=send_message).pack(pady=5, side=tk.LEFT)
    tk.Button(chat_window, text="Finish & Analyze", font=("Arial", 11), bg="#4caf50", fg="white", command=finish_chat).pack(pady=5, side=tk.RIGHT, padx=(5, 20))

    chat_window.mainloop()

# ----------------------------- Speech Analysis -----------------------------
def analyze_speech():
    recognizer = sr.Recognizer()
    root = tk.Tk()
    root.withdraw()

    popup = Toplevel()
    popup.title("Speech Analyzer")
    popup.geometry("400x300")
    popup.configure(bg="#f0f0f0")

    Label(popup, text="🎙 Speak now... Recording for 20 seconds", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    transcript_display = tk.Text(popup, font=("Arial", 11), height=8, wrap=tk.WORD, state="disabled")
    transcript_display.pack(pady=10, padx=10)

    def transcribe():
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, phrase_time_limit=20)
                text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                text = "Sorry, I couldn't understand your speech."
            except Exception as e:
                text = f"Error: {e}"

        transcript_display.config(state="normal")
        transcript_display.insert(tk.END, text)
        transcript_display.config(state="disabled")

        popup.destroy()
        analyze_text_logic(text)

    threading.Thread(target=transcribe).start()
    popup.mainloop()

# ----------------------------- Utility Popup -----------------------------
def show_popup(title, message, emoji):
    root = tk.Tk()
    root.withdraw()
    popup = Toplevel()
    popup.title(title)
    popup.geometry("420x250")
    popup.configure(bg="#f0f0f0")

    Label(popup, text=emoji, font=("Arial", 50), bg="#f0f0f0").pack(pady=10)
    Label(popup, text=message, font=("Arial", 12), bg="#f0f0f0", wraplength=380, justify="center").pack(pady=10)

    Button(popup, text="OK", font=("Arial", 12), command=popup.destroy, bg="#4caf50", fg="white", padx=10, pady=5).pack(pady=10)
    popup.mainloop()

# ----------------------------- GUI Main -----------------------------
def main_menu():
    root = tk.Tk()
    root.title("Mental Health Companion")
    root.geometry("400x400")
    root.configure(bg="#e3f2fd")

    Label(root, text="Welcome to Mental Health Companion", font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=20)

    Button(root, text="🧠 Analyze Face Emotions", font=("Arial", 12), bg="#90caf9", fg="black", width=30,
           command=lambda: [root.withdraw(), generate_report(analyze_emotions()), root.deiconify()]).pack(pady=10)

    Button(root, text="💬 Text-Based Chat", font=("Arial", 12), bg="#a5d6a7", fg="black", width=30,
           command=lambda: [root.withdraw(), analyze_text_chat(), root.deiconify()]).pack(pady=10)

    Button(root, text="🎤 Speak to Analyze", font=("Arial", 12), bg="#ffcc80", fg="black", width=30,
           command=lambda: [root.withdraw(), analyze_speech(), root.deiconify()]).pack(pady=10)

    Button(root, text="❌ Exit", font=("Arial", 12), bg="#ef9a9a", fg="black", width=30,
           command=root.quit).pack(pady=20)

    root.mainloop()

# ----------------------------- Run -----------------------------
if _name_ == "_main_":
    main_menu()