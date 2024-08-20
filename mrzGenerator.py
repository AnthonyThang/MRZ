import cv2
import pytesseract
from pymongo import MongoClient

# Tesseract'ın sistemdeki kurulu olduğu yolu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# MongoDB veritabanı bağlantısı/ Database seçimi ve koleksiyon seçimi
client = MongoClient("mongodb://localhost:27017/")
db = client["MRZ"]

# Resmi yükleyin ve gri tonlamaya çevirin
img = cv2.imread(r'C:/Users/Mert/Desktop/Staj/MRZ/passport2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# OCR işlemi yapın
text = pytesseract.image_to_string(gray)
text = text.replace(' ', '')  # Boşlukları kaldır
# Sonuçları satırlara ayır
lines = text.splitlines()

# "I", "P" veya "V" ayrımı
mrz_lines = []

for i, line in enumerate(lines):
    if line.startswith('I'):
        # Identity card ise 2 satır daha al
        mrz_block = lines[i:i+3]
        mrz_lines = mrz_block[:3]  # İlk iki satırı ayrı indekslere yerleştir

        # Datalar
        country_code = mrz_lines[0][2:5]
        document_number = mrz_lines[0][5:14]
        check_digit = mrz_lines[0][14]
        national_id = mrz_lines[0][16:27]
        if int(mrz_lines[1][0:2]) > 24:
            birth_date = f"19{mrz_lines[1][0:2]}-{mrz_lines[1][2:4]}-{mrz_lines[1][4:6]}"
        else:
            birth_date = f"20{mrz_lines[1][0:2]}-{mrz_lines[1][2:4]}-{mrz_lines[1][4:6]}"
        gender = "Erkek" if mrz_lines[1][7] == "M" else "Kadın"
        expiry_date = f"20{mrz_lines[1][8:10]}-{mrz_lines[1][10:12]}-{mrz_lines[1][12:14]}"
        
        # Soyad
        surname_end = mrz_lines[2].find('<<')
        surname = mrz_lines[2][0:surname_end]
        
        # Ad
        name_section = mrz_lines[2][surname_end+2:]
        names = name_section.split('<')
        names = [name for name in names if name]
        
        first_name = names[0] if len(names) > 0 else None
        second_name = names[1] if len(names) > 1 else None

        document = {
            "CountryCode": country_code,
            "DocumentNumber": document_number,
            "CheckDigit": check_digit,
            "NationalID": national_id,
            "BirthDate": birth_date,
            "Gender": gender,
            "ExpiryDate": expiry_date,
            "Surname": surname,
            "FirstName": first_name,
            "SecondName": second_name
        }

        collection = db["IdentityCard"]  # IdentityCard koleksiyonu
        collection.insert_one(document)

    elif line.startswith('P'):
        # Pasaport MRZ'si ise
        mrz_block = lines[i:i+2]
        mrz_lines = mrz_block  # İlk iki satırı ayrı indekslere yerleştir

        country_code = mrz_lines[0][2:5]
        passport_number = mrz_lines[1][0:9]
        passport_check_digit = mrz_lines[1][9]
        birth_date = f"19{mrz_lines[1][13:15]}-{mrz_lines[1][15:17]}-{mrz_lines[1][17:19]}"
        birth_check_digit = mrz_lines[1][19]
        sex = "Erkek" if mrz_lines[1][20] == "M" else "Kadın"
        expiry_date = f"20{mrz_lines[1][21:23]}-{mrz_lines[1][23:25]}-{mrz_lines[1][25:27]}"
        expiry_check_digit = mrz_lines[1][16]
        nationality = mrz_lines[1][10:13]


        surname_end = mrz_lines[0].find('<<')
        surname = mrz_lines[0][5:surname_end]
        name_section = mrz_lines[0][surname_end+2:]
        names = name_section.split('<')
        first_name = names[0] if len(names) > 0 else None
        second_name = names[1] if len(names) > 1 else None

        document = {
            "CountryCode": country_code,
            "PassportNumber": passport_number,
            "PassportCheckDigit": passport_check_digit,
            "BirthDate": birth_date,
            "BirthCheckDigit": birth_check_digit,
            "Gender": sex,
            "ExpiryDate": expiry_date,
            "ExpiryCheckDigit": expiry_check_digit,
            "Nationality": nationality,
            "Surname": surname,
            "FirstName": first_name,
            "SecondName": second_name
        }

        collection = db["Passport"]  # Passport koleksiyonu
        collection.insert_one(document)

    elif line.startswith('V'):
        # Vize MRZ'si ise
        mrz_block = lines[i:i+2]
        mrz_lines = mrz_block  # İlk iki satırı ayrı indekslere yerleştir

        visa_type = mrz_lines[0][0]
        country_code = mrz_lines[0][2:5]
        visa_number = mrz_lines[0][5:14]
        visa_check_digit = mrz_lines[0][14]
        birth_date = f"19{mrz_lines[0][13:15]}-{mrz_lines[0][15:17]}-{mrz_lines[0][17:19]}"
        birth_check_digit = mrz_lines[0][19]
        sex = "Erkek" if mrz_lines[0][20] == "M" else "Kadın"
        expiry_date = f"20{mrz_lines[0][21:23]}-{mrz_lines[0][23:25]}-{mrz_lines[0][25:27]}"
        expiry_check_digit = mrz_lines[0][27]
        nationality = mrz_lines[0][28:31]

        surname_end = mrz_lines[0].find('<<')
        surname = mrz_lines[0][5:surname_end]
        name_section = mrz_lines[1][surname_end+2:]
        names = name_section.split('<')
        first_name = names[0] if len(names) > 0 else None
        second_name = names[1] if len(names) > 1 else None

        document = {
            "VisaType": visa_type,
            "CountryCode": country_code,
            "VisaNumber": visa_number,
            "VisaCheckDigit": visa_check_digit,
            "BirthDate": birth_date,
            "BirthCheckDigit": birth_check_digit,
            "Gender": sex,
            "ExpiryDate": expiry_date,
            "ExpiryCheckDigit": expiry_check_digit,
            "Nationality": nationality,
            "Surname": surname,
            "FirstName": first_name,
            "SecondName": second_name
        }
        
        collection = db["Visa"] 

