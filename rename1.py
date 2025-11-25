import tkinter as tk
from tkinter import messagebox
import datetime
import hashlib
import os

# --- FUNGSI LOGIKA (BACKEND) ---

def generate_new_base_name(base_name_input):
    """
    Menghasilkan string nama file baru tanpa ekstensi dengan format: 
    [NamaDasar]_[DDMMYYYY]_[HASH_5_DIGIT]
    """
    
    if not base_name_input:
        return "ERROR: Nama Dasar tidak boleh kosong."
        
    # 1. Membersihkan input
    final_base_name = base_name_input.strip().replace(" ", "_")
    
    # 2. Mendapatkan metadata waktu dan Hash
    now = datetime.datetime.now()
    date_str = now.strftime("%d%m%Y") # Format: TanggalBulanTahun
    
    unique_string = f"{final_base_name}{now.timestamp()}"
    hash_object = hashlib.sha256(unique_string.encode())
    unique_hash = hash_object.hexdigest()[:5] # Hash 5 Digit
    
    # 3. Membuat Nama File Baru Final (TANPA EKSTENSI)
    new_name_string = (
        f"{final_base_name}_"
        f"{date_str}_" 
        f"{unique_hash}" 
    )
    
    return new_name_string


# --- FUNGSI FRONTEND (TKINTER) ---

class NameGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("File Name Generator Simple")
        master.geometry("500x200")
        
        # 0. Judul
        tk.Label(master, text="GENERATE NAMA FILE OTOMATIS", font=('Arial', 14, 'bold')).pack(pady=10)

        # 1. Input Nama Dasar (Tanpa Nilai Default)
        tk.Label(master, text="1. Nama Dasar File (cth: Laporan_Final):").pack(anchor='w', padx=20)
        self.entry_base_name = tk.Entry(master, width=60)
        # self.entry_base_name.insert(0, "Laporan_Final") <--- BARIS INI DIHAPUS
        self.entry_base_name.pack(padx=20)
        
        # 2. Tombol Generate
        tk.Button(master, text="GENERATE NAMA", command=self.run_generation, bg='lightblue', font=('Arial', 10, 'bold')).pack(pady=10)

        # 3. Output dan Tombol Copy
        tk.Label(master, text="Nama File Baru (Target):").pack(anchor='w', padx=20)
        
        frame_output = tk.Frame(master)
        frame_output.pack(padx=20)
        
        self.output_result = tk.Entry(frame_output, width=50, state='readonly', readonlybackground='lightgray')
        self.output_result.pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(frame_output, text="COPY", command=self.copy_to_clipboard, bg='yellow').pack(side=tk.LEFT)

    def run_generation(self):
        """Mengeksekusi generasi nama secara instan."""
        
        base_name = self.entry_base_name.get().strip()
        
        # Panggil fungsi backend
        new_name = generate_new_base_name(base_name)
        
        # Tampilkan hasil
        self.output_result.config(state=tk.NORMAL)
        self.output_result.delete(0, tk.END)
        self.output_result.insert(0, new_name)
        self.output_result.config(state='readonly')
        
        if new_name.startswith("ERROR"):
             messagebox.showerror("Error", new_name)

    def copy_to_clipboard(self):
        """Menyalin teks dari field output ke clipboard."""
        text_to_copy = self.output_result.get()
        if text_to_copy and not text_to_copy.startswith("ERROR"):
            self.master.clipboard_clear()
            self.master.clipboard_append(text_to_copy)
            self.master.update() 
            messagebox.showinfo("Berhasil", "Nama file telah disalin ke clipboard!")
        else:
            messagebox.showwarning("Gagal Salin", "Tidak ada nama file valid untuk disalin.")


# --- JALANKAN APLIKASI GUI ---

if __name__ == "__main__":
    root = tk.Tk()
    app = NameGeneratorApp(root)
    root.mainloop()