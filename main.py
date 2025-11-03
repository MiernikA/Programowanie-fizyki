import tkinter as tk
import subprocess
import os

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "projects")

PROJECTS = [
    "SoftBodyCollision.py",
    "TikTokBallCollision.py",
    "VerletCloth.py"
]

def run_script(script_name):
    script_path = os.path.join(PROJECTS_DIR, script_name)
    subprocess.run(["python", script_path])

root = tk.Tk()
root.title("Physics Simulations Launcher")
root.geometry("800x400")

label = tk.Label(root, text="Wybierz projekt do uruchomienia:", font=("Arial", 12))
label.pack(pady=10)

for project in PROJECTS:
    btn = tk.Button(root, text=project, command=lambda p=project: run_script(p), height=2, width=25)
    btn.pack(pady=5)

root.mainloop()
