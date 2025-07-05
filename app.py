import customtkinter as ctk
import threading
from tkinter import messagebox

# Import our custom modules
from twitter_client import post_tweet
from gemini_client import generate_post_from_prompt, refine_text_for_twitter

# --- App Settings ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
X_CHARACTER_LIMIT = 280

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Tweet Co-Pilot v4.0")
        self.geometry("700x900")
        self.grid_columnconfigure(0, weight=1)

        # --- WIDGETS ---
        self.main_label = ctk.CTkLabel(self, text="AI Tweet Co-Pilot", font=ctk.CTkFont(size=24, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 1. AI PROMPT SECTION
        self.prompt_label = ctk.CTkLabel(self, text="1. Enter Your Idea or Prompt:", font=ctk.CTkFont(weight="bold"))
        self.prompt_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.prompt_textbox = ctk.CTkTextbox(self, height=100)
        self.prompt_textbox.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        self.generate_button = ctk.CTkButton(self, text="Generate Draft", command=self.run_ai_thread)
        self.generate_button.grid(row=3, column=0, padx=20, pady=5)

        # 2. EDITABLE CONTENT SECTION
        self.edit_label = ctk.CTkLabel(self, text="2. Edit Your Draft Here:", font=ctk.CTkFont(weight="bold"))
        self.edit_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.content_textbox = ctk.CTkTextbox(self, height=150)
        self.content_textbox.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")

        # 3. REFINE & PREVIEW SECTION
        self.preview_label = ctk.CTkLabel(self, text="3. AI-Refined Final Preview:", font=ctk.CTkFont(weight="bold"))
        self.preview_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
        self.char_count_label = ctk.CTkLabel(self, text=f"0 / {X_CHARACTER_LIMIT}", text_color="gray")
        self.char_count_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="e")
        self.preview_textbox = ctk.CTkTextbox(self, height=150, state="disabled", fg_color="gray14")
        self.preview_textbox.grid(row=7, column=0, padx=20, pady=5, sticky="nsew")
        self.refine_button = ctk.CTkButton(self, text="Refine & Preview", command=self.run_refine_thread)
        self.refine_button.grid(row=8, column=0, padx=20, pady=5)
        
        # 4. POSTING SECTION
        self.post_button = ctk.CTkButton(self, text="POST TO X", command=self.run_post_thread, state="disabled", fg_color="#1DA1F2", hover_color="#0c85d0")
        self.post_button.grid(row=9, column=0, padx=20, pady=10)

        # 5. STATUS LOG
        self.status_textbox = ctk.CTkTextbox(self, height=100, state="disabled")
        self.status_textbox.grid(row=10, column=0, padx=20, pady=(5, 20), sticky="nsew")

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
        self.char_count_label.configure(text=f"{char_count} / {X_CHARACTER_LIMIT}")
        self.char_count_label.configure(text_color="red" if char_count > X_CHARACTER_LIMIT else "green")
    
    def lock_buttons(self, is_working):
        state = "disabled" if is_working else "normal"
        self.generate_button.configure(state=state)
        self.refine_button.configure(state=state)
        # Post button has its own logic, but disable it during any operation
        if is_working: self.post_button.configure(state="disabled")

    def _run_threaded_task(self, task_function):
        self.lock_buttons(True)
        thread = threading.Thread(target=task_function)
        thread.start()

    def run_ai_thread(self): self._run_threaded_task(self._generate_draft_logic)
    def run_refine_thread(self): self._run_threaded_task(self._refine_and_preview_logic)
    def run_post_thread(self): self._run_threaded_task(self._post_the_tweet_logic)

    def _generate_draft_logic(self):
        self.generate_button.configure(text="Generating...")
        try:
            prompt = self.prompt_textbox.get("1.0", "end-1c")
            generated_text = generate_post_from_prompt(prompt)
            self.update_status("AI draft generated.")
            self.content_textbox.delete("1.0", "end")
            self.content_textbox.insert("0.0", generated_text)
        except Exception as e:
            self.show_error_popup("AI Draft Failed", str(e))
        finally:
            self.generate_button.configure(text="Generate Draft")
            self.lock_buttons(False)

    def _refine_and_preview_logic(self):
        self.refine_button.configure(text="Refining...")
        try:
            raw_text = self.content_textbox.get("1.0", "end-1c")
            if not raw_text.strip():
                raise ValueError("The edit box is empty. Please generate or write content first.")
            refined_text = refine_text_for_twitter(raw_text)
            self.update_status("AI refinement complete.")
            self.preview_textbox.configure(state="normal")
            self.preview_textbox.delete("1.0", "end")
            self.preview_textbox.insert("0.0", refined_text)
            self.preview_textbox.configure(state="disabled")
            self.update_preview_char_count()
        except Exception as e:
            self.show_error_popup("AI Refinement Failed", str(e))
        finally:
            self.refine_button.configure(text="Refine & Preview")
            self.lock_buttons(False)
            # Only enable post button if refinement was successful and within limits
            if len(self.preview_textbox.get("1.0", "end-1c")) <= X_CHARACTER_LIMIT:
                self.post_button.configure(state="normal")

    def _post_the_tweet_logic(self):
        self.post_button.configure(text="Posting...")
        try:
            final_text = self.preview_textbox.get("1.0", "end-1c")
            if not final_text.strip(): raise ValueError("Preview box is empty.")
            if len(final_text) > X_CHARACTER_LIMIT: raise ValueError("Tweet is over character limit.")
            self.update_status("Sending final tweet to X...")
            post_tweet(final_text)
            self.update_status("✅✅✅ TWEET POSTED SUCCESSFULLY!")
        except Exception as e:
            self.show_error_popup("Posting Failed", str(e))
        finally:
            self.post_button.configure(text="POST TO X")
            self.lock_buttons(False)
            self.post_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()