import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from pdf_watermark_remove import (
    extreme_watermark_removal, check_for_watermarks,
    get_watermark_keywords, set_watermark_keywords,
    get_default_watermark_keywords, reset_watermark_keywords
)

class KeywordDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Watermark Keywords")
        
        # Set window size and position
        window_width = 500
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Keywords list
        ttk.Label(main_frame, text="Current Keywords:").grid(row=0, column=0, sticky=tk.W)
        
        # Keywords text area with scrollbar
        self.keywords_text = tk.Text(main_frame, height=15, width=50)
        self.keywords_text.grid(row=1, column=0, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.keywords_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.keywords_text.configure(yscrollcommand=scrollbar.set)
        
        # Load current keywords
        current_keywords = get_watermark_keywords()
        self.keywords_text.insert('1.0', '\n'.join(current_keywords))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save_keywords).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Default", command=self.reset_to_default).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        # Help text
        help_text = "Enter one keyword per line. These keywords will be used to identify watermarks."
        ttk.Label(main_frame, text=help_text, wraplength=400).grid(row=3, column=0, columnspan=2, pady=10)
    
    def save_keywords(self):
        # Get keywords from text area
        keywords_text = self.keywords_text.get('1.0', tk.END).strip()
        keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        if not keywords:
            messagebox.showerror("Error", "Please enter at least one keyword")
            return
        
        # Save keywords
        set_watermark_keywords(keywords)
        messagebox.showinfo("Success", "Keywords have been updated")
        self.destroy()
    
    def reset_to_default(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset to default keywords?"):
            reset_watermark_keywords()
            self.keywords_text.delete('1.0', tk.END)
            self.keywords_text.insert('1.0', '\n'.join(get_default_watermark_keywords()))

class PDFWatermarkRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Text Watermark Remover")
        
        # Set window size and position
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input file selection
        ttk.Label(main_frame, text="Select PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=1, column=1)
        
        # Output file selection
        ttk.Label(main_frame, text="Save Output As:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=3, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=3, column=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Check Watermarks", command=self.check_watermarks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Watermarks", command=self.remove_watermarks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Manage Keywords", command=self.manage_keywords).pack(side=tk.LEFT, padx=5)
        
        # Log text area
        self.log_text = tk.Text(main_frame, height=10, width=60)
        self.log_text.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=7, column=2, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
    
    def manage_keywords(self):
        """打开关键词管理对话框"""
        KeywordDialog(self.root)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            # Automatically set output path
            output_filename = os.path.splitext(filename)[0] + "_no_watermark.pdf"
            self.output_path.set(output_filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def check_watermarks(self):
        input_file = self.input_path.get()
        if not input_file:
            messagebox.showerror("Error", "Please select an input PDF file")
            return
        
        self.status_var.set("Checking for watermarks...")
        self.log_message("Starting watermark check...")
        self.log_message(f"Using keywords: {', '.join(get_watermark_keywords())}")
        
        try:
            total_watermarks, pages_with_watermarks, watermarks_per_page = check_for_watermarks(input_file)
            
            if total_watermarks > 0:
                self.log_message(f"\nFound {total_watermarks} watermarks in {len(pages_with_watermarks)} pages")
                for page_num, (count, details) in watermarks_per_page.items():
                    self.log_message(f"\nPage {page_num}: {count} watermarks")
                    for keyword, keyword_count in details.items():
                        self.log_message(f"  - '{keyword}': {keyword_count}")
            else:
                self.log_message("\nNo watermarks found in the document")
            
            self.status_var.set("Watermark check completed")
        except Exception as e:
            self.status_var.set("Error during watermark check")
            messagebox.showerror("Error", str(e))

    def remove_watermarks(self):
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        
        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files")
            return
        
        self.status_var.set("Removing watermarks...")
        self.log_message("\nStarting watermark removal...")
        self.log_message(f"Using keywords: {', '.join(get_watermark_keywords())}")
        
        try:
            modified_pages = extreme_watermark_removal(input_file, output_file)
            
            if modified_pages > 0:
                self.log_message(f"\nSuccessfully processed {modified_pages} pages")
                self.log_message(f"Saved output to: {output_file}")
                self.status_var.set("Watermark removal completed")
                messagebox.showinfo("Success", "Watermarks have been removed successfully!")
            else:
                self.status_var.set("No watermarks found")
                messagebox.showinfo("Info", "No watermarks were found to remove")
        except Exception as e:
            self.status_var.set("Error during watermark removal")
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = PDFWatermarkRemoverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 