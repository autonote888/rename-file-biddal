import streamlit as st
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
    # Pastikan format date/time/hash tetap unik
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


# --- FUNGSI FRONTEND (STREAMLIT) ---

def main():
    st.set_page_config(page_title="File Renamer Otomatis", layout="centered")
    
    st.title("GENERATE NAMA FILE OTOMATIS")
    st.markdown("---")

    # 1. Input Nama Dasar
    base_name_input = st.text_input(
        "1. Nama Dasar File (cth: Laporan_Final):",
        value="",
        placeholder="Masukkan nama yang Anda inginkan (misalnya: Backup_Q4)"
    )

    # 2. Tombol Generate
    if st.button("GENERATE NAMA", type="primary"):
        
        # Panggil fungsi backend
        new_name = generate_new_base_name(base_name_input)
        
        if new_name.startswith("ERROR"):
            st.error(new_name)
        else:
            # 3. Output Hasil
            st.subheader("Nama File Baru (Target):")
            
            # Tampilkan hasil di kotak input read-only untuk kemudahan copy-paste
            st.code(new_name, language='text') 
            
            st.success("Nama file berhasil dibuat! Silakan salin di atas dan tambahkan ekstensinya secara manual.")
            
            # --- Tambahan untuk menyalin ke clipboard (Hanya bekerja di browser modern) ---
            # Streamlit belum memiliki tombol copy built-in, jadi kita gunakan st.code
            # atau HTML/JS, namun st.code sudah cukup baik untuk copy-paste.

if __name__ == "__main__":
    main()
