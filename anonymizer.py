import re
from docx import Document

def anonymize_name(name):
    if len(name) > 1:
        return name[0] + '*' * (len(name) - 1)
    return name

def advanced_anonymizer(text):
    # 2. БҮХ "Ө.Бахыт" хэлбэрийн хүний нэрийг "Ө.Б" болгох
    # "Ө.Бахыт" → "Ө.Б"
    # "Б.Даш" → "Б.Д"
    # "Д.Болд" → "Д.Б"
    text = re.sub(r'\b([А-ЯӨҮ])\.([А-ЯӨҮ])([а-яөү]+)\b', r'\1.\2', text)
    text = re.sub(r'\b([А-ЯӨҮ])\.\s+([А-ЯӨҮ])([а-яөү]+)\b', r'\1.\2', text)

    # 3. БҮТЭН НЭРИЙГ НУУЦЛАХ (том үсгээр эхэлсэн 2+ үсэгтэй)
    # Харин "Ө.Бахыт" аль хэдийн "Ө.Б" болсон учраас энэ хэсэгт орохгүй
    name_pattern = r'\b[А-ЯӨҮ][а-яөү]{2,}\b'
    names = re.findall(name_pattern, text)
    
    # Нууцлах ёсгүй үгс
    exclude_words = {
        'Монгол', 'Монголын', 'Хууль', 'Шүүх', 'Хэрэг', 'Улс', 'Улсын','Шүүгдэгчийн', 'Шүүгдэгчийг','Эрүүгийн','Шүүхийн','Шүүхийг','Иргэний','Сум','Тус','Тиймээ','Миний','Анхан','Хэргийн', 'Прокурорын', 'Прокурор', 'Баян-Өлгий', 'Надад', 'Прокурор', 'Мал', 'Тухайлбал', 'Тавдугаар', 'Арван', 'Өмчлөгч', 'Гэмт', 'Иймд', 'Энэ', 'Шүүхээс', 
        'Нийслэл', 'Иргэний', 'Нэхэмжлэгчийн', 'Улсын', 'Хэрэгт', 'Гэрлэгчид', 'Засаг', 'Хариуцагч', 'Нэхэмжлэгч', 'Хот', 'Аймаг', 'Сум', 'Баг', 'Иргэн', 'Эрх', 'Дугаар', 'Орчуулагч', 'Шүүгдэгч', 'Эрүү', 'Анх', 'Нэг', 'Хоёр', 'Гэм', 'Үүнд', 'Хохирогч', 'Гэрч', 'Хөрөнгө', 'Шүүх', 'Дараа', 'Тухайн', 'Өөрөөр', 'Үндсэн', 'Баян', 'Өлгий', 'Шүүхээс', 'Үүнийг', 'Тэгээд', 'Гэхдээ', 'Шаардлагатай', 'Энэхүү', 'Бид', 'Хулгайд', 'Сүүлд',
    }
    
    for name in set(names):
        if name not in exclude_words and not re.match(r'[А-ЯӨҮ]\.Б$', name):
            # "Ө.Б" хэлбэртэй биш нэрийг л нууцлах
            text = re.sub(rf'\b{name}\b', anonymize_name(name), text)

    # 4. ХУВИЙН МЭДЭЭЛЭЛ НУУЦЛАХ
    text = re.sub(r'\b[А-Яа-я]{2}\d{8}\b', '[********]', text)
    text = re.sub(r'\b\d{8}\b', '[********]', text)
    text = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[********]', text)
    text = re.sub(r'\b(БЗД|СБД|ХУД|ЧД)\b', '[ДҮҮРЭГ]', text)
    text = re.sub(r'\b(Улаанбаатар|УБ)\b', '[ХОТ]', text)
    
    # 6. СУМ, БАГ, КОМПАНИ НУУЦЛАХ
    def replace_company_stars(match):
        company_name = match.group(0)
        words = company_name.split()
        
        # ХХК, ХК, банк гэх мэт төгсгөлийг хадгалах
        company_types = ['ХХК', 'ХК', 'ХКК', 'банк', 'компани', 'JSC', 'LLC']
        
        if words[-1] in company_types:
            # Үг бүрийн уртаар тохирох тооны * үсэг үүсгэх
            anonymized_words = []
            for word in words[:-1]:
                if word not in company_types:
                    anonymized_words.append('*' * len(word))
                else:
                    anonymized_words.append(word)
            anonymized_words.append(words[-1])  # Төгсгөлийн үгийг хадгалах
            return ' '.join(anonymized_words)
        else:
            # Хэрэв төгсгөлийн үг компанийн төрөл биш бол
            anonymized_words = ['*' * len(word) for word in words]
            return ' '.join(anonymized_words)
    
    # Компани нэрийг олох хэв маяг
    company_patterns = [
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+ХХК\b',
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+ХК\b',
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+ХКК\b',
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+банк\b',
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+компани\b',
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+JSC\b',
        r'\b[А-ЯӨҮа-яөүA-Za-z\s-]+\s+LLC\b'
    ]
    
    for pattern in company_patterns:
        text = re.sub(pattern, replace_company_stars, text, flags=re.IGNORECASE)
  

    return text

def anonymize_docx(input_path, output_path):
    doc = Document(input_path)
    for para in doc.paragraphs:
        para.text = advanced_anonymizer(para.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell.text = advanced_anonymizer(cell.text)
    doc.save(output_path)
