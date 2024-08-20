import cv2
import pytesseract

# Tesseract'ın sistemdeki kurulu olduğu yolu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows için

# Resmi yükleyin
img = cv2.imread(r'C:/Users/Mert/Desktop/Staj/MRZ/tc1.jpg')

# Görüntüyü gri tonlamaya çevir
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Yazıyı OCR ile oku
text = pytesseract.image_to_string(gray)

# Sonuçları satırlara ayır
lines = text.splitlines()

# "I<", "P<" veya "V<" ile başlayan satırı ve altındaki 2 satırı bul ve bir dizi içinde topla
mrz_lines = []
for i, line in enumerate(lines):
    if line.startswith('I'):
        # Geçerli satırı ve altındaki 2 satırı al
        mrz_block = lines[i:i+3]
        mrz_lines.append("".join(mrz_block))
        print("\n" + mrz_lines[0] + "\n")
        print("Kimlik Kartı")
        print("Ülke Kodu: "+mrz_lines[0][2:5])
        print("Kimlik seri numarası: " + mrz_lines[0][5:14])
        print("Kontrol numarası: "  + mrz_lines[0][14])
        print("TC Kimlik No: " + mrz_lines[0][16:27])
        print("Doğum tarihi: "  + mrz_lines[0][34:36] + "/" + mrz_lines[0][32:34] + "/" + mrz_lines[0][30:32])
        
        if mrz_lines[0][36] == "M":
            print("Cinsiyet: Erkek")
        else: 
            print("Cinsiyet: Kadın")
        
        print("Son kullanma tarihi: "  + mrz_lines[0][42:44] + "/" + mrz_lines[0][40:42] + "/" + mrz_lines[0][38:40])
        
        # Soyadı bulma
        surname_start = 60
        surname_end = mrz_lines[0].find('<<', 56)
        surname = mrz_lines[0][57:surname_end]
        print("Soyad: " + surname)

        # Adları bulma
        name_section = mrz_lines[0][surname_end+2:]
        names = name_section.split('<')
        names = [name for name in names if name]  # Boş stringleri filtrele

        # Adları yazdırma
        for i, name in enumerate(names):
            print(f"Ad {i+1}: " + name)

    elif line.startswith('P') or line.startswith('V'):
        mrz_block= lines[i:i+2]
        mrz_lines.append("".join(mrz_block))
        # Pasaport veya Vize MRZ'si ise
        if mrz_lines[0][0:2] == "P":
            print("Pasaport")
        elif mrz_lines[0][0:2] == "V":
            print("Visa")
