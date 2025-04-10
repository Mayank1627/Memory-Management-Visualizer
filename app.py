import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import messagebox, simpledialog

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
    return page_faults, gantt_chart // Random Comment

class MemoryManagementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")
        self.reference_string = []
        self.frames = 0
        
        tk.Label(root, text="Reference String (comma separated):").grid(row=0, column=0)
        self.ref_string_entry = tk.Entry(root)
        self.ref_string_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Number of Frames:").grid(row=1, column=0)
        self.frames_entry = tk.Entry(root)
        self.frames_entry.grid(row=1, column=1)
        
        tk.Button(root, text="Generate Random Reference String", command=self.generate_random_string).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="Run FIFO", command=lambda: self.run_algorithm("FIFO")).grid(row=3, column=0)
        tk.Button(root, text="Run LRU", command=lambda: self.run_algorithm("LRU")).grid(row=3, column=1)
        
    def generate_random_string(self):
        length = simpledialog.askinteger("Input", "Enter length of reference string:")
        range_start = simpledialog.askinteger("Input", "Enter start of range:")
        range_end = simpledialog.askinteger("Input", "Enter end of range:")
        self.reference_string = [random.randint(range_start, range_end) for _ in range(length)]
        self.ref_string_entry.delete(0, tk.END)
        self.ref_string_entry.insert(0, ",".join(map(str, self.reference_string)))
    
    def run_algorithm(self, algorithm):
        try:
            self.reference_string = list(map(int, self.ref_string_entry.get().split(',')))
            self.frames = int(self.frames_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please check your reference string and number of frames.")
            return
        
        if algorithm == "FIFO":
            faults, gantt_chart = fifo(self.reference_string, self.frames)
        elif algorithm == "LRU":
            faults, gantt_chart = lru(self.reference_string, self.frames)
        
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
