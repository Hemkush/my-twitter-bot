import customtkinter as ctk
import threading
from tkinter import messagebox

from twitter_client import post_tweet
from reddit_client import post_reddit
from gemini_client import generate_post_from_prompt, refine_text_for_twitter, refine_text_for_reddit
from scraper.fetcher import fetch_techcrunch_ai

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
X_CHARACTER_LIMIT = 280
reddit_CHARACTER_LIMIT = 300

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Tweet Co-Pilot v4.0")
        self.geometry("800x1000")
        self.grid_columnconfigure(0, weight=1)

        self.main_label = ctk.CTkLabel(self, text="AI Tweet Co-Pilot", font=ctk.CTkFont(size=28, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.prompt_label = ctk.CTkLabel(self, text="1. Select an Article:", font=ctk.CTkFont(size=16, weight="bold"))
        self.prompt_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.article_listbox = ctk.CTkComboBox(self, values=[], width=700)
        self.article_listbox.grid(row=2, column=0, padx=20, pady=5)

        self.generate_button = ctk.CTkButton(self, text="Send to Editor", command=self.send_article_to_editor)
        self.generate_button.grid(row=3, column=0, padx=20, pady=10)

        self.articles = []
        self.populate_articles()

        self.edit_label = ctk.CTkLabel(self, text="2. Edit Your Draft Here:", font=ctk.CTkFont(size=16, weight="bold"))
        self.edit_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")

        self.content_textbox = ctk.CTkTextbox(self, height=150)
        self.content_textbox.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")

        # --- SIDE-BY-SIDE PREVIEW SECTION ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(1, weight=1)

        # Tweet Preview Section
        self.tweet_label = ctk.CTkLabel(self.preview_frame, text="3. Final Preview - Tweet", font=ctk.CTkFont(size=16, weight="bold"))
        self.tweet_label.grid(row=0, column=0, padx=10, pady=(0, 2), sticky="w")

        self.char_count_label = ctk.CTkLabel(self.preview_frame, text=f"0 / {X_CHARACTER_LIMIT}", text_color="gray")
        self.char_count_label.grid(row=0, column=0, padx=10, pady=(0, 2), sticky="e")

        self.preview_textbox = ctk.CTkTextbox(self.preview_frame, height=150, state="disabled", fg_color="gray14")
        self.preview_textbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Reddit Preview Section
        self.reddit_label = ctk.CTkLabel(self.preview_frame, text="4. Final Preview - Reddit", font=ctk.CTkFont(size=16, weight="bold"))
        self.reddit_label.grid(row=0, column=1, padx=10, pady=(0, 2), sticky="w")

        self.char_count_label_reddit = ctk.CTkLabel(self.preview_frame, text=f"0 / {reddit_CHARACTER_LIMIT}", text_color="gray")
        self.char_count_label_reddit.grid(row=0, column=1, padx=10, pady=(0, 2), sticky="e")

        self.reddit_preview_textbox = ctk.CTkTextbox(self.preview_frame, height=150, state="disabled", fg_color="gray14")
        self.reddit_preview_textbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.refine_button = ctk.CTkButton(self, text="Refine & Preview", command=self.run_refine_thread)
        self.refine_button.grid(row=8, column=0, padx=20, pady=10)


        self.post_button = ctk.CTkButton(self, text="POST TO X & REDDIT", command=self.run_post_thread, state="disabled", fg_color="#1DA1F2", hover_color="#0c85d0")
        self.post_button.grid(row=11, column=0, padx=20, pady=15)

        self.status_textbox = ctk.CTkTextbox(self, height=100, state="disabled")
        self.status_textbox.grid(row=12, column=0, padx=20, pady=10, sticky="nsew")

    def populate_articles(self):
        try:
            self.articles = fetch_techcrunch_ai()
            titles = [a['title'] for a in self.articles]
            self.article_listbox.configure(values=titles)
            if titles:
                self.article_listbox.set(titles[0])
        except Exception as e:
            self.show_error_popup("Article Fetch Failed", str(e))

    def send_article_to_editor(self):
        idx = self.article_listbox.cget("values").index(self.article_listbox.get())
        article = self.articles[idx]
        content = f"{article['title']}\n\n{article.get('summary', '')}"
        self.content_textbox.delete("1.0", "end")
        self.content_textbox.insert("0.0", content)
        self.update_status(f"Article '{article['title']}' sent to editor.")

    def update_status(self, message):
        self.status_textbox.configure(state="normal")
        self.status_textbox.insert("end", f"-> {message}\n")
        self.status_textbox.configure(state="disabled")
        self.status_textbox.see("end")

    def show_error_popup(self, title, message):
        self.after(0, messagebox.showerror, title, message)
        self.update_status(f"🔴 ERROR: {title} - {message}")

    def update_preview_char_count(self):
        content = self.preview_textbox.get("1.0", "end-1c")
        char_count = len(content)
        contect_reddit = self.reddit_preview_textbox.get("1.0", "end-1c")
        char_count_reddit = len(contect_reddit)
        self.char_count_label.configure(text=f"{char_count} / {X_CHARACTER_LIMIT}")
        self.char_count_label.configure(text_color="red" if char_count > X_CHARACTER_LIMIT else "green")
        self.char_count_label_reddit.configure(text=f"{char_count_reddit} / {reddit_CHARACTER_LIMIT}")
        self.char_count_label_reddit.configure(text_color="red" if char_count_reddit > reddit_CHARACTER_LIMIT else "green")

    def lock_buttons(self, is_working):
        state = "disabled" if is_working else "normal"
        self.generate_button.configure(state=state)
        self.refine_button.configure(state=state)
        if is_working:
            self.post_button.configure(state="disabled")

    def _run_threaded_task(self, task_function):
        self.lock_buttons(True)
        thread = threading.Thread(target=task_function)
        thread.start()

    def run_refine_thread(self): self._run_threaded_task(self._refine_logic)
    def run_post_thread(self): self._run_threaded_task(self._post_logic)

    def _refine_logic(self):
        self.refine_button.configure(text="Refining...")
        try:
            raw_text = self.content_textbox.get("1.0", "end-1c")
            if not raw_text.strip():
                raise ValueError("The edit box is empty. Please generate or write content first.")
            refined_tweet = refine_text_for_twitter(raw_text)
            refined_reddit = refine_text_for_reddit(raw_text)

            self.preview_textbox.configure(state="normal")
            self.preview_textbox.delete("1.0", "end")
            self.preview_textbox.insert("0.0", refined_tweet)
            self.preview_textbox.configure(state="disabled")

            self.reddit_preview_textbox.configure(state="normal")
            self.reddit_preview_textbox.delete("1.0", "end")
            self.reddit_preview_textbox.insert("0.0", refined_reddit)
            self.reddit_preview_textbox.configure(state="disabled")

            self.update_status("AI refinement complete.")
            self.update_preview_char_count()
            if len(refined_tweet) <= X_CHARACTER_LIMIT:
                self.post_button.configure(state="normal")

        except Exception as e:
            self.show_error_popup("Refinement Error", str(e))
        finally:
            self.refine_button.configure(text="Refine & Preview")
            self.lock_buttons(False)

    def _post_logic(self):
        self.post_button.configure(text="Posting...")
        try:
            tweet = self.preview_textbox.get("1.0", "end-1c")
            reddit_post = self.reddit_preview_textbox.get("1.0", "end-1c")
            if not tweet.strip():
                raise ValueError("Tweet box is empty.")
            if len(tweet) > X_CHARACTER_LIMIT:
                raise ValueError("Tweet exceeds character limit.")

            post_tweet(tweet)
            post_reddit(reddit_post)
            self.update_status("✅ Posted to X and Reddit successfully.")

        except Exception as e:
            self.show_error_popup("Posting Error", str(e))
        finally:
            self.post_button.configure(text="POST TO X & REDDIT")
            self.lock_buttons(False)

if __name__ == "__main__":
    App().mainloop()

