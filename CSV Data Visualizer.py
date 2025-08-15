import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSV_Visualizer:
    def __init__(self, base):
        self.base = base
        self.base.title("CSV Data Visualizer")
        self.base.geometry("900x700")

        self.df = None
        self.canvas = None

        load_button = tk.Button(base, text="Load CSV", command=self.load_csv, bg="lightblue")
        load_button.pack(pady=5)

        self.tree = ttk.Treeview(base)
        self.tree.pack(pady=10)

        control_frame = tk.Frame(base)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="X-axis:").grid(row=0, column=0, padx=5)
        self.x_column = ttk.Combobox(control_frame, width=20)
        self.x_column.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Y-axis:").grid(row=0, column=2, padx=5)
        self.y_column = ttk.Combobox(control_frame, width=20)
        self.y_column.grid(row=0, column=3, padx=5)

        tk.Label(control_frame, text="Chart Type:").grid(row=0, column=4, padx=5)
        self.chart_type = ttk.Combobox(control_frame, width=15, values=["Line", "Bar", "Pie"])
        self.chart_type.current(0)
        self.chart_type.grid(row=0, column=5, padx=5)

        plot_button = tk.Button(control_frame, text="Plot Graph", command=self.plot_graph, bg="lightgreen")
        plot_button.grid(row=0, column=6, padx=5)

        self.chart_frame = tk.Frame(base)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

    def load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])

        if not filepath:
            return
        try:
            self.df = pd.read_csv(filepath)
            self.show_data()
            self.x_column['values'] = list(self.df.columns)
            self.y_column['values'] = list(self.df.columns)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def show_data(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"

        for col in self.df.columns:
            self.tree.heading(col, text=col)
        
        for _, row in self.df.head(50).iterrows():
            self.tree.insert("", tk.END, values=list(row))
    
    def plot_graph(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV file first.")
            return
        x_col = self.x_column.get()
        y_col = self.y_column.get()
        chart = self.chart_type.get()

        if x_col not in self.df.columns or y_col not in self.df.columns and chart != "Pie":
            messagebox.showerror("Error", "Select a valid coloumns for X and Y axes.")
            return
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        fig, ax = plt.subplots(figsize=(8, 5))
    
        if chart == "Line":
            ax.plot(self.df[x_col], self.df[y_col], marker='o')
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} vs {x_col}")
        elif chart == "Bar":
            ax.bar(self.df[x_col], self.df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} vs {x_col}")
        elif chart == "Pie":
            values = self.df[y_col]
            label = self.df[x_col] if x_col in self.df.columns else range(len(values))
            ax.pie(values, labels=label, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Pie chart of {y_col}")

        if chart != "Pie":
            ax.grid(True)

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSV_Visualizer(root)
    root.mainloop()