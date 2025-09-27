import sys
import customtkinter as ctk
import requests
import keyboard
import threading

class ChatWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title for chat interface
        self.chat_title = ctk.CTkLabel(
            self,
            text="Chat with Assistant",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "gray80")
        )
        self.chat_title.pack(pady=(10, 5))
        
        # Chat history with improved styling
        self.chat_text = ctk.CTkTextbox(
            self,
            height=300,
            font=ctk.CTkFont(size=12),
            wrap="word",
            corner_radius=8,
            border_width=1,
            border_color=("gray70", "gray30")
        )
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=(5,5))
        
        # Input area container frame
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="x", padx=10, pady=10, side="bottom")
        
        # Message input
        self.message_input = ctk.CTkEntry(
            self.bottom_frame,
            placeholder_text="Type your message here...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.message_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="Send",
            width=100,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.send_message
        )
        self.send_button.pack(side="right")
        
        # Back button
        self.back_button = ctk.CTkButton(
            self,
            text="← Back to Menu",
            command=self.return_to_menu,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            text_color=("gray40", "gray60"),
            hover_color=("gray75", "gray25")
        )
        self.back_button.pack(padx=10, pady=5, anchor="w")
        
        # Bind Enter key
        self.message_input.bind("<Return>", lambda e: self.send_message())
        
        # Welcome message
        self.chat_text.insert("end", "Assistant: Hello! How can I help you today?\n\n")
        self.chat_text.configure(state="disabled")  # Make read-only initially

    def send_message(self):
        message = self.message_input.get().strip()
        if message:
            # Enable text widget temporarily
            self.chat_text.configure(state="normal")
            self.chat_text.insert("end", f"You: {message}\n\n")
            self.chat_text.see("end")  # Auto-scroll to bottom
            self.chat_text.configure(state="disabled")
            self.message_input.delete(0, "end")
            
            # Disable input while processing
            self.message_input.configure(state="disabled")
            self.send_button.configure(state="disabled")
            
            # Send to backend
            threading.Thread(
                target=self.get_response,
                args=(message,),
                daemon=True
            ).start()

    def get_response(self, message):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": message}
            )
            if response.status_code == 200:
                ai_response = response.json()["response"]
                self.after(0, self.update_chat, ai_response)
            else:
                self.after(0, self.update_chat, "Error: Could not get response")
        except Exception as e:
            self.after(0, self.update_chat, f"Error: {str(e)}")
        finally:
            # Re-enable input
            self.after(0, self.enable_input)

    def update_chat(self, response):
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"Assistant: {response}\n\n")
        self.chat_text.see("end")
        self.chat_text.configure(state="disabled")

    def enable_input(self):
        self.message_input.configure(state="normal")
        self.send_button.configure(state="normal")
        self.message_input.focus()  # Focus back to input

    def return_to_menu(self):
        if hasattr(self.master.master, "show_buttons"):
            self.master.master.show_buttons()

class Overlay(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure window
        self.title("Pixly")
        self.geometry("500x500")
        self.overrideredirect(True)  # Remove window decorations
        self.attributes('-topmost', True)  # Stay on top
        self.configure(fg_color=("gray90", "gray10"))
        
        # Add subtle transparency
        self.attributes('-alpha', 0.80)
        
        # Make the window itself have rounded corners
        self.attributes('-transparentcolor', 'white')
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create main frame with rounded corners and shadow effect
        self.frame = ctk.CTkFrame(
            self, 
            corner_radius=25,
            border_width=2,
            border_color=("gray70", "gray30"),
            fg_color=("white", "gray15")
        )
        self.frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Create header section
        self.header_frame = ctk.CTkFrame(
            self.frame, 
            corner_radius=15,
            fg_color=("gray85", "gray20"),
            height=60
        )
        self.header_frame.pack(fill="x", padx=15, pady=(15, 10))
        self.header_frame.pack_propagate(False)
        # Close/Back button in top left
        self.header_button = ctk.CTkButton(
            self.header_frame,
            text="✕",
            command=self.close_app,
            width=30,
            height=30,
            corner_radius=15,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("darkgrey", "darkgrey"),
            hover_color=("red", "red"),
            text_color="white"
        )
        self.header_button.place(x=10, y=15)
        # Title with icon
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Pixly Control Panel",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("gray20", "gray80")
        )
        self.title_label.pack(pady=15)
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self.frame)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Chat window (initially hidden)
        self.chat_window = ChatWindow(self.content_frame)
        
        # Buttons container
        self.buttons_frame = ctk.CTkFrame(self.content_frame)
        self.buttons_frame.pack(fill="both", expand=True)
        
        # Create buttons
        self.chat_button = self.create_button(
            "Chat with Assistant",
            self.toggle_chat_window,
            "blue"
        )
        self.button2 = self.create_button("Button 2", lambda: None, "green")
        self.button3 = self.create_button("Button 3", lambda: None, "orange")
        self.button4 = self.create_button("Button 4", lambda: None, "purple")
        
        # Show buttons initially
        self.show_buttons()
        
        # Center window
        self.center_window()
        
        # Bind drag events to header
        self.header_frame.bind('<Button-1>', self.start_drag)
        self.header_frame.bind('<B1-Motion>', self.on_drag)
        self.title_label.bind('<Button-1>', self.start_drag)
        self.title_label.bind('<B1-Motion>', self.on_drag)
        
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width - 430  # Adjusted for new width (400 + padding)
        y = (screen_height - 530) // 2  # Adjusted for new height (500 + padding)
        self.geometry(f'+{x}+{y}')
    
    def close_app(self):
        """Close the application permanently"""
        print("Pixly closed permanently")
        self.quit()
        self.destroy()
        sys.exit()
    
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def call_backend(self, endpoint, task_name):
        # Disable buttons during processing
        self.button_a.configure(state="disabled")
        self.button_b.configure(state="disabled")
        
        # Run the request in a separate thread to avoid blocking UI
        def make_request():
            try:
                response = requests.get(f"http://127.0.0.1:8000{endpoint}", timeout=5)
                if response.status_code == 200:
                    result = response.json()

                    print(f"Task {task_name} result: {result}")
                else:
                    print(f"Error: Server returned {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Network error: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
            finally:
                # Re-enable buttons after a short delay
                self.after(1500, self.enable_buttons)
                # Reset status after delay
        
        # Start the request in a separate thread
        threading.Thread(target=make_request, daemon=True).start()
    
    
    def enable_buttons(self):
        """Re-enable all buttons"""
        self.button_a.configure(state="normal")
        self.button_b.configure(state="normal")
    
    def create_button(self, text, command, color):
        return ctk.CTkButton(
            self.buttons_frame,
            text=text,
            command=command,
            height=45,
            corner_radius=12,
            fg_color=color,
            hover_color=f"dark{color}"
        )

    def toggle_chat_window(self):
        if self.chat_window.winfo_viewable():
            self.show_buttons()
        else:
            self.show_chat()

    def show_chat(self):
        self.buttons_frame.pack_forget()
        self.chat_window.pack(fill="both", expand=True)
        # Update header button to back button
        self.header_button.configure(
            text="←",
            command=self.show_buttons,
            hover_color=("gray50", "gray50")
        )

    def show_buttons(self):
        self.chat_window.pack_forget()
        self.buttons_frame.pack(fill="both", expand=True)
        for btn in [self.chat_button, self.button2, self.button3, self.button4]:
            btn.pack(pady=5, padx=20, fill="x")
        # Restore close button
        self.header_button.configure(
            text="✕",
            command=self.close_app,
            hover_color=("red", "red")
        )

def main():
    app = Overlay()
    
    # Toggle visibility with global hotkey
    def toggle_overlay():
        if app.winfo_viewable():
            app.withdraw()
            print("Overlay is now hidden (Ctrl+Alt+M to show)")
        else:
            app.deiconify()
            app.lift()  # Bring to front
            print("Pixly is now active!")
    
    keyboard.add_hotkey('ctrl+alt+m', toggle_overlay)
    
    app.withdraw()  # Start hidden
    print("Pixly initialized! Press Ctrl+Alt+M to toggle visibility")
    app.mainloop()

if __name__ == "__main__":
    main()