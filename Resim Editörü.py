import os
import subprocess
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox


class ImageEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere ayarları
        self.title("Resim Galerisi Yönetimi")
        self.geometry("800x600")

        # Klasör yolları
        self.output_folder = os.path.join(os.getcwd(), "output")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Sol panel (Seçenekler)
        self.left_panel = ctk.CTkFrame(self, width=200)
        self.left_panel.pack(side="left", fill="y")

        # Sağ panel (İçerik)
        self.right_panel = ctk.CTkFrame(self, width=600)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Resim seçimi düğmesi
        self.select_image_button = ctk.CTkButton(
            self.left_panel, text="Resim Seç", command=self.select_image
        )
        self.select_image_button.pack(pady=20)

        # Yeniden boyutlandırma alanı
        self.resize_label = ctk.CTkLabel(self.left_panel, text="Yeniden Boyutlandır:")
        self.resize_label.pack(pady=10)

        self.width_input = ctk.CTkEntry(self.left_panel, placeholder_text="Genişlik")
        self.width_input.pack(pady=5)

        self.height_input = ctk.CTkEntry(self.left_panel, placeholder_text="Yükseklik")
        self.height_input.pack(pady=5)

        # Format değiştirme alanı
        self.format_label = ctk.CTkLabel(self.left_panel, text="Format Dönüştür:")
        self.format_label.pack(pady=10)

        self.format_input = ctk.CTkEntry(self.left_panel, placeholder_text="jpg, png, vb.")
        self.format_input.pack(pady=5)

        # İşlemi başlat düğmesi
        self.process_button = ctk.CTkButton(
            self.left_panel, text="Uygula", command=self.process_image
        )
        self.process_button.pack(pady=20)

        # Klasöre git düğmesi
        self.open_folder_button = ctk.CTkButton(
            self.left_panel, text="Klasöre Git", command=self.open_output_folder
        )
        self.open_folder_button.pack(pady=20)

        # Resim önizleme alanı
        self.image_label = ctk.CTkLabel(self.right_panel, text="Resim önizlemesi")
        self.image_label.pack(pady=20, padx=20)

        # Mesaj kutusu
        self.message_box = ctk.CTkLabel(self.right_panel, text="", text_color="green")
        self.message_box.pack(pady=10)

        # Seçilen dosya yolu
        self.selected_file = None

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Resim Seç", filetypes=[("Resim Dosyaları", "*.jpg *.png *.jpeg *.bmp")]
        )
        if file_path:
            self.selected_file = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 300))
            img.save("preview_temp.png")
            photo = ctk.CTkImage(file="preview_temp.png")
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.message_box.configure(text="Resim yüklendi.", text_color="green")

    def process_image(self):
        if not self.selected_file:
            messagebox.showerror("Hata", "Lütfen bir resim seçin!")
            return

        try:
            base_name = os.path.basename(self.selected_file)
            name, ext = os.path.splitext(base_name)

            # Yeniden boyutlandırma
            if self.width_input.get() and self.height_input.get():
                width = int(self.width_input.get())
                height = int(self.height_input.get())
                with Image.open(self.selected_file) as img:
                    img = img.resize((width, height))
                    output_path = os.path.join(self.output_folder, f"{name}_resized{ext}")
                    img.save(output_path)
                    self.message_box.configure(
                        text=f"Resim başarıyla boyutlandırıldı: {output_path}",
                        text_color="green",
                    )

            # Format değiştirme
            if self.format_input.get():
                new_format = self.format_input.get().lower()
                output_path = os.path.join(self.output_folder, f"{name}.{new_format}")
                with Image.open(self.selected_file) as img:
                    img.save(output_path)
                self.message_box.configure(
                    text=f"Resim başarıyla {new_format} formatına dönüştürüldü: {output_path}",
                    text_color="green",
                )

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def open_output_folder(self):
        try:
            if os.name == "nt":  # Windows
                os.startfile(self.output_folder)
            elif os.name == "posix":  # macOS/Linux
                subprocess.call(["open" if "darwin" in os.sys.platform else "xdg-open", self.output_folder])
        except Exception as e:
            messagebox.showerror("Hata", f"Klasör açılamadı: {e}")


if __name__ == "__main__":
    app = ImageEditorApp()
    app.mainloop()
