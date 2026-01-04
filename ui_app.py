import customtkinter as ctk
import subprocess
import sys
import math
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

controller_process = None
current_mode = "WEB"

# ---------------- ANIMATED BACKGROUND ----------------

class Particle:
    def __init__(self, canvas_width, canvas_height):
        self.x = random.randint(0, canvas_width)
        self.y = random.randint(0, canvas_height)
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-0.5, 0.5)
        self.color = random.choice(['#FF6B9D', '#C44569', '#4A90E2', '#50C9CE', '#FFA07A', '#9B59B6'])
        
    def move(self, canvas_width, canvas_height):
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.x < 0 or self.x > canvas_width:
            self.speed_x *= -1
        if self.y < 0 or self.y > canvas_height:
            self.speed_y *= -1

# ---------------- LOGIC ----------------

def start_controller():
    global controller_process
    if controller_process is None:
        controller_process = subprocess.Popen(
            [sys.executable, "gesture_engine/controller.py"]
        )
        status_label.configure(text="● RUNNING", text_color="#00E676")
        animate_status_change()

def stop_controller():
    global controller_process
    if controller_process:
        controller_process.terminate()
        controller_process = None
        status_label.configure(text="● STOPPED", text_color="#FF5252")
        animate_status_change()

def switch_mode_ui():
    global current_mode
    current_mode = "PPT" if current_mode == "WEB" else "WEB"
    mode_label.configure(text=f"MODE: {current_mode}")
    animate_mode_switch()

def animate_mode_switch():
    # Fade out current frame
    if current_mode == "WEB":
        fade_transition(ppt_frame, web_frame)
    else:
        fade_transition(web_frame, ppt_frame)

def fade_transition(frame_out, frame_in):
    frame_out.pack_forget()
    frame_in.pack(fill="both", expand=True, padx=20, pady=10)

def animate_status_change():
    # Simple pulse animation
    original_size = status_label.cget("font").cget("size")
    status_label.configure(font=ctk.CTkFont(size=original_size + 4, weight="bold"))
    app.after(100, lambda: status_label.configure(font=ctk.CTkFont(size=original_size, weight="bold")))

# ---------------- BACKGROUND ANIMATION ----------------

particles = []
animation_running = True

def animate_background():
    if not animation_running:
        return
    
    bg_canvas.delete("all")
    
    # Draw gradient-like effect with particles
    for particle in particles:
        particle.move(900, 600)
        bg_canvas.create_oval(
            particle.x - particle.size,
            particle.y - particle.size,
            particle.x + particle.size,
            particle.y + particle.size,
            fill=particle.color,
            outline=""
        )
    
    # Draw connecting lines between nearby particles
    for i, p1 in enumerate(particles):
        for p2 in particles[i+1:]:
            dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
            if dist < 100:
                opacity = int(255 * (1 - dist/100))
                bg_canvas.create_line(
                    p1.x, p1.y, p2.x, p2.y,
                    fill=f'#{opacity:02x}{opacity:02x}{opacity:02x}',
                    width=1
                )
    
    app.after(30, animate_background)

# ---------------- UI WINDOW ----------------

app = ctk.CTk()
app.title("Gesture-Based AI Controller")
app.geometry("900x650")
app.resizable(False, False)

# Background canvas
bg_canvas = ctk.CTkCanvas(app, width=900, height=650, bg="#1a1a1a", highlightthickness=0)
bg_canvas.place(x=0, y=0)

# Initialize particles
for _ in range(50):
    particles.append(Particle(900, 650))

# Start animation
animate_background()

# Main container with transparency effect
main_container = ctk.CTkFrame(app, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=20)
main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

# ---------------- HEADER ----------------

header = ctk.CTkFrame(main_container, height=90, fg_color="transparent")
header.pack(fill="x", pady=(10, 0))

title_label = ctk.CTkLabel(
    header,
    text="🖐️ Gesture-Based AI Controller",
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color=("#FFFFFF", "#E0E0E0")
)
title_label.pack(pady=20)

# ---------------- STATUS & MODE ----------------

status_mode_frame = ctk.CTkFrame(main_container, fg_color="transparent")
status_mode_frame.pack(pady=10)

status_label = ctk.CTkLabel(
    status_mode_frame,
    text="● STOPPED",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color="#FF5252"
)
status_label.pack()

mode_label = ctk.CTkLabel(
    status_mode_frame,
    text="MODE: WEB",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#4FC3F7"
)
mode_label.pack(pady=5)

# ---------------- BUTTONS ----------------

btn_frame = ctk.CTkFrame(main_container, fg_color="transparent")
btn_frame.pack(pady=15)

start_btn = ctk.CTkButton(
    btn_frame, 
    text="▶ START", 
    width=180, 
    height=50,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color=("#2E7D32", "#1B5E20"),
    hover_color=("#43A047", "#2E7D32"),
    corner_radius=15,
    command=start_controller
)
start_btn.grid(row=0, column=0, padx=12)

stop_btn = ctk.CTkButton(
    btn_frame, 
    text="■ STOP", 
    width=180, 
    height=50,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color=("#C62828", "#B71C1C"),
    hover_color=("#E53935", "#C62828"),
    corner_radius=15,
    command=stop_controller
)
stop_btn.grid(row=0, column=1, padx=12)

switch_btn = ctk.CTkButton(
    btn_frame, 
    text="🔁 SWITCH MODE", 
    width=220, 
    height=50,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color=("#6A1B9A", "#4A148C"),
    hover_color=("#8E24AA", "#6A1B9A"),
    corner_radius=15,
    command=switch_mode_ui
)
switch_btn.grid(row=0, column=2, padx=12)

# ---------------- MAIN PANEL WITH SCROLLBAR ----------------

main_panel = ctk.CTkFrame(main_container, fg_color="transparent")
main_panel.pack(padx=20, pady=10, fill="both", expand=True)

# ---------------- WEB MODE PANEL ----------------

web_frame = ctk.CTkScrollableFrame(
    main_panel, 
    corner_radius=20,
    fg_color=("#2b2b2b", "#1e1e1e"),
    scrollbar_button_color=("#4A90E2", "#357ABD"),
    scrollbar_button_hover_color=("#5BA3F5", "#4A90E2")
)

web_title = ctk.CTkLabel(
    web_frame,
    text="🌐 WEB MODE – GESTURES",
    font=ctk.CTkFont(size=24, weight="bold"),
    text_color="#4FC3F7"
)
web_title.pack(pady=20)

web_gestures = [
    ("MODE SWITCH (ACTUAL SYSTEM)", "✌️✌️✌️ Three Fingers (Hold 3s)", "Switch between WEB and PPT modes", "#FF6B9D"),
    ("MEDIA CONTROL", "👍 Thumbs Up", "Play / Pause (YouTube / Media)", "#50C9CE"),
    ("SCROLL ACTION", "✌️ Two Fingers", "Scroll Down", "#9B59B6"),
    ("NAVIGATION", "☝️ Index Finger", "Previous Video", "#FFA07A"),
    ("NAVIGATION", "🤘 Index + Pinky", "Next Video", "#4A90E2"),
]

for title, gesture, action, color in web_gestures:
    gesture_card = ctk.CTkFrame(web_frame, corner_radius=15, fg_color=("#363636", "#252525"))
    gesture_card.pack(padx=15, pady=10, fill="x")
    
    ctk.CTkLabel(
        gesture_card,
        text=title,
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=color,
        anchor="w"
    ).pack(padx=20, pady=(15, 5), anchor="w")
    
    ctk.CTkLabel(
        gesture_card,
        text=f"{gesture}",
        font=ctk.CTkFont(size=18, weight="bold"),
        anchor="w"
    ).pack(padx=20, pady=5, anchor="w")
    
    ctk.CTkLabel(
        gesture_card,
        text=f"→ {action}",
        font=ctk.CTkFont(size=14),
        text_color="#B0B0B0",
        anchor="w"
    ).pack(padx=20, pady=(5, 15), anchor="w")

# ---------------- PPT MODE PANEL ----------------

ppt_frame = ctk.CTkScrollableFrame(
    main_panel, 
    corner_radius=20,
    fg_color=("#2b2b2b", "#1e1e1e"),
    scrollbar_button_color=("#4A90E2", "#357ABD"),
    scrollbar_button_hover_color=("#5BA3F5", "#4A90E2")
)

ppt_title = ctk.CTkLabel(
    ppt_frame,
    text="📽️ PPT MODE – GESTURES",
    font=ctk.CTkFont(size=24, weight="bold"),
    text_color="#FF6B9D"
)
ppt_title.pack(pady=20)

ppt_gestures = [
    ("PRESENTATION CONTROL", "👍 Thumbs Up", "Play / Pause Slide Show", "#50C9CE"),
    ("SLIDE NAVIGATION", "✌️ Two Fingers", "Next Slide", "#9B59B6"),
    ("SLIDE NAVIGATION", "☝️ Index Finger", "Previous Slide", "#FFA07A"),
]

for title, gesture, action, color in ppt_gestures:
    gesture_card = ctk.CTkFrame(ppt_frame, corner_radius=15, fg_color=("#363636", "#252525"))
    gesture_card.pack(padx=15, pady=10, fill="x")
    
    ctk.CTkLabel(
        gesture_card,
        text=title,
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=color,
        anchor="w"
    ).pack(padx=20, pady=(15, 5), anchor="w")
    
    ctk.CTkLabel(
        gesture_card,
        text=f"{gesture}",
        font=ctk.CTkFont(size=18, weight="bold"),
        anchor="w"
    ).pack(padx=20, pady=5, anchor="w")
    
    ctk.CTkLabel(
        gesture_card,
        text=f"→ {action}",
        font=ctk.CTkFont(size=14),
        text_color="#B0B0B0",
        anchor="w"
    ).pack(padx=20, pady=(5, 15), anchor="w")

# Show WEB by default
web_frame.pack(fill="both", expand=True, padx=20, pady=10)

# ---------------- FOOTER ----------------

footer = ctk.CTkLabel(
    main_container,
    text="✨ Real-time Human–Computer Interaction using Computer Vision ✨",
    font=ctk.CTkFont(size=13),
    text_color="#808080"
)
footer.pack(pady=15)

def on_closing():
    global animation_running
    animation_running = False
    stop_controller()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()