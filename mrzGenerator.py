import cv2
import pytesseract
from pymongo import MongoClient

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# MongoDB database connection
client = MongoClient("mongodb://localhost:27017/")
db = client["MRZ"]

#File location of Img
img = cv2.imread(r'**')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# OCR
text = pytesseract.image_to_string(gray)
text = text.replace(' ', '')
#img sonucu lines
lines = text.splitlines()
mrz_lines = []

for i, line in enumerate(lines):
    #Identity Card
    if line.startswith('I'):
        mrz_block = lines[i:i+3]
        mrz_lines = mrz_block[:3] 

        # Datas
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
        
        # Surname
        surname_end = mrz_lines[2].find('<<')
        surname = mrz_lines[2][0:surname_end]
        
        # Name
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
        #Identity Card collection
        collection = db["IdentityCard"]  
        #Push into collection
        collection.insert_one(document)



#Passport MRZ
    elif line.startswith('P'):
        # Passport MRZ
        mrz_block = lines[i:i+2]
        mrz_lines = mrz_block

        country_code = mrz_lines[0][2:5]

        passport_number = mrz_lines[1][0:9]
        passport_check_digit = mrz_lines[1][9]
        nationality = mrz_lines[1][10:13]

        if int(mrz_lines[1][13:15]) > 24:
            birth_date = f"19{mrz_lines[1][13:15]}-{mrz_lines[1][15:17]}-{mrz_lines[1][17:19]}"
        else:
            birth_date = f"20{mrz_lines[1][13:15]}-{mrz_lines[1][15:17]}-{mrz_lines[1][17:19]}"
        
        birth_check_digit = mrz_lines[1][19]

        sex = "Erkek" if mrz_lines[1][20] == "M" else "Kadın"

        if int(mrz_lines[1][21:23]) > 24:
            expiry_date = f"19{mrz_lines[1][21:23]}-{mrz_lines[1][23:25]}-{mrz_lines[1][25:27]}"
        else:
            expiry_date = f"20{mrz_lines[1][21:23]}-{mrz_lines[1][23:25]}-{mrz_lines[1][25:27]}"
        
        expiry_check_digit = mrz_lines[1][27]
        


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
        #Passport collection
        collection = db["Passport"]  # Passport koleksiyonu
        collection.insert_one(document)


    #Visa MRZ
    elif line.startswith('V'):
        mrz_block = lines[i:i+2]
        mrz_lines = mrz_block  

        country_code = mrz_lines[0][2:5]

        visa_number = mrz_lines[1][0:9]
        visa_check_digit = mrz_lines[1][9]
       
        nationality = mrz_lines[1][10:13]
        if int(mrz_lines[1][13:15]) > 24:
            birth_date = f"19{mrz_lines[1][13:15]}-{mrz_lines[1][15:17]}-{mrz_lines[1][17:19]}"
        else:
            birth_date = f"20{mrz_lines[1][13:15]}-{mrz_lines[1][15:17]}-{mrz_lines[1][17:19]}"
        
        birth_check_digit = mrz_lines[1][19]

        sex = "Erkek" if mrz_lines[1][20] == "M" else "Kadın"

        if int(mrz_lines[1][21:23]) > 24:
            expiry_date = f"19{mrz_lines[1][21:23]}-{mrz_lines[1][23:25]}-{mrz_lines[1][25:27]}"
        else:
            expiry_date = f"20{mrz_lines[1][21:23]}-{mrz_lines[1][23:25]}-{mrz_lines[1][25:27]}"
        expiry_check_digit = mrz_lines[1][27]

        

        surname_end = mrz_lines[0].find('<<')
        surname = mrz_lines[0][5:surname_end]
        name_section = mrz_lines[0][surname_end+2:]
        names = name_section.split('<')
        first_name = names[0] if len(names) > 0 else None
        second_name = names[1] if len(names) > 1 else None

        document = {
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
        collection.insert_one(document)
