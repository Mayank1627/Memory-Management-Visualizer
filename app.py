import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def fifo(reference_string, frames):
    memory = deque(maxlen=frames)
    page_faults = 0
    gantt_chart = []
    for page in reference_string:
        if page not in memory:
            if len(memory) == frames:
                memory.popleft()
            memory.append(page)
            page_faults += 1
        gantt_chart.append(list(memory))
    return page_faults, gantt_chart

def lru(reference_string, frames):
    memory = []
    page_faults = 0
    gantt_chart = []
    for page in reference_string:
        if page not in memory:
            if len(memory) == frames:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
        else:
            memory.remove(page)
            memory.append(page)
        gantt_chart.append(list(memory))
    return page_faults, gantt_chart

def optimal(reference_string, frames):
    memory = []
    page_faults = 0
    gantt_chart = []

    for i in range(len(reference_string)):
        page = reference_string[i]
        if page not in memory:
            page_faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                # Find which page in memory won't be used for longest time
                farthest = -1
                page_to_replace = None
                for m in memory:
                    # Check if the page appears in future references
                    try:
                        next_use = reference_string[i+1:].index(m)
                    except ValueError:
                        next_use = float('inf')
                    
                    if next_use > farthest:
                        farthest = next_use
                        page_to_replace = m
                
                memory.remove(page_to_replace)
                memory.append(page)
        gantt_chart.append(list(memory))
    return page_faults, gantt_chart

class MemoryManagementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Apply a modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 10), padding=5)
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Input Parameters", padding=(15, 10))
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Reference String
        ttk.Label(self.input_frame, text="Reference String:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ref_string_entry = ttk.Entry(self.input_frame, width=40)
        self.ref_string_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Number of Frames
        ttk.Label(self.input_frame, text="Number of Frames:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.frames_entry = ttk.Entry(self.input_frame, width=10)
        self.frames_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons
        self.random_btn = ttk.Button(self.button_frame, text="Generate Random String", 
                                   command=self.generate_random_string)
        self.random_btn.pack(side=tk.LEFT, padx=5)
        
        self.fifo_btn = ttk.Button(self.button_frame, text="Run FIFO", 
                                 command=lambda: self.run_algorithm("FIFO"))
        self.fifo_btn.pack(side=tk.LEFT, padx=5)
        
        self.lru_btn = ttk.Button(self.button_frame, text="Run LRU", 
                                command=lambda: self.run_algorithm("LRU"))
        self.lru_btn.pack(side=tk.LEFT, padx=5)
        
        self.optimal_btn = ttk.Button(self.button_frame, text="Run Optimal", 
                                   command=lambda: self.run_algorithm("Optimal"))
        self.optimal_btn.pack(side=tk.LEFT, padx=5)
        
        # Tooltips
        self.create_tooltip(self.ref_string_entry, "Enter comma-separated numbers (e.g., 1,2,3,4)")
        self.create_tooltip(self.frames_entry, "Enter the number of available frames")
        
        # Set focus to first entry field
        self.ref_string_entry.focus()
        
    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(self.root)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        
        label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", padding=5)
        label.pack()
        
        def enter(event):
            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty() + (widget.winfo_height() // 2)
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()
            
        def leave(event):
            tooltip.withdraw()
            
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def generate_random_string(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Random Reference String")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Frame for entries
        entries_frame = ttk.Frame(dialog, padding="10")
        entries_frame.pack(fill=tk.BOTH, expand=True)
        
        # Length of reference string
        ttk.Label(entries_frame, text="Length of reference string:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        length_entry = ttk.Entry(entries_frame)
        length_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Start of range
        ttk.Label(entries_frame, text="Start of range:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        range_start_entry = ttk.Entry(entries_frame)
        range_start_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 5))
        
        # End of range
        ttk.Label(entries_frame, text="End of range:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        range_end_entry = ttk.Entry(entries_frame)
        range_end_entry.grid(row=2, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Button frame
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X)
        
        def generate():
            try:
                length = int(length_entry.get())
                start = int(range_start_entry.get())
                end = int(range_end_entry.get())
                
                if length <= 0 or start >= end:
                    raise ValueError("Invalid range or length")
                
                # Generate random string
                ref_string = [str(random.randint(start, end)) for _ in range(length)]
                self.ref_string_entry.delete(0, tk.END)
                self.ref_string_entry.insert(0, ",".join(ref_string))
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}", parent=dialog)
        
        # Generate button
        generate_btn = ttk.Button(button_frame, text="Generate", command=generate)
        generate_btn.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Set focus to first entry field
        length_entry.focus()
        
        # Make the dialog modal
        dialog.grab_set()
        dialog.wait_window()
    
    def run_algorithm(self, algorithm):
        try:
            self.reference_string = list(map(int, self.ref_string_entry.get().split(',')))
            self.frames = int(self.frames_entry.get())
            
            if self.frames <= 0:
                raise ValueError("Number of frames must be positive")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input!\n{str(e)}\nPlease check your reference string and number of frames.")
            return
        
        if algorithm == "FIFO":
            faults, gantt_chart = fifo(self.reference_string, self.frames)
        elif algorithm == "LRU":
            faults, gantt_chart = lru(self.reference_string, self.frames)
        elif algorithm == "Optimal":
            faults, gantt_chart = optimal(self.reference_string, self.frames)
        
        messagebox.showinfo("Results", f"{algorithm} Algorithm\nTotal Page Faults: {faults}")
        self.plot_gantt_chart(gantt_chart, algorithm)
    
    def plot_gantt_chart(self, gantt_chart, algorithm_name):
        fig, ax = plt.subplots()
        colors = plt.cm.get_cmap("tab10", len(set(sum(gantt_chart, []))))
        
        def update(frame):
            ax.clear()
            ax.set_title(f"Gantt Chart - {algorithm_name}")
            ax.set_xlabel("Steps")
            ax.set_ylabel("Frames")
            for i, row in enumerate(gantt_chart[:frame + 1]):
                for j, val in enumerate(row):
                    ax.text(i, j, str(val), ha='center', va='center', 
                            bbox=dict(facecolor=colors(val), edgecolor='black', boxstyle='round,pad=0.3'))
            ax.set_xlim(-1, len(gantt_chart))
            ax.set_ylim(-1, max(len(row) for row in gantt_chart))
            ax.invert_yaxis()
        
        ani = animation.FuncAnimation(fig, update, frames=len(gantt_chart), repeat=False)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagementSimulator(root)
    root.mainloop()