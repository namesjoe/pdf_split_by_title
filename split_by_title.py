import fitz
import re
import os
from pathlib import Path


folder_for_pdfs = '~/Documents/biblio'

def walk(path: str, extension):
    if extension:
        for address, _, files in os.walk(os.path.expanduser(path)):
            for file_path in files:
                if file_path.lower().endswith(extension):
                    yield Path(address, file_path)
    else:
        for address, _, files in os.walk(os.path.expanduser(path)):
            for file_path in files:
                yield Path(address, file_path)


files = walk(folder_for_pdfs, extension="pdf")

for file_path in files:
    print(file_path)
    doc = fitz.open(file_path)
    name = file_path.stem
    print(name)

    # Создаем директорию для рассказов из этого файла
    stories_dir = Path(file_path.parent, name)
    stories_dir.mkdir(exist_ok=True)

    current_story = ""
    current_title = ""
    story_counter = 0

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        page_text = page.get_text()

        match = re.match(r'^([A-ZА-Я\s]+)\n', page_text)

        if match:
            if current_story:
                with open(f"{stories_dir}/{story_counter}_{current_title[:35]}.txt", "w", encoding="utf-8") as file:
                    file.write(current_story)
                current_story = ""
            current_title = match.group(1).strip()
            story_counter += 1
            current_story += page_text
        else:
            current_story += page_text

    if current_story:  # добавляем последний рассказ
        with open(f"{stories_dir}/{story_counter}_{current_title[:35]}.txt", "w", encoding="utf-8") as file:
            file.write(current_story)
