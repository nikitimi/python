from PyPDF2 import PdfReader
from os import path, system
from threading import Thread

from modules.timer import Timer

class PDF_to_JSON:
    def __init__(self, filepath:str):
        self.filepath = filepath
        self.is_finish = False
        self.t = Timer()

        self.sec_to_min = self.t.seconds/60

        self.process_with_ocr(filepath)
    
    def process_with_ocr(self, filepath:str):
        result_json = './result.json'
        pages:list[dict[str,str]] = []
        reader = PdfReader(filepath)
        MAX_PAGES = len(reader.pages)

        if not path.isfile(filepath):
            return print(f"{filepath} is not a page")
        if path.isfile(result_json):
            return print(f"Delete {result_json} first before executing this script!")
        
        Thread(target=self.t.timer, daemon=True).start()
        for index in range(MAX_PAGES+1):
            percentage = ((index)/MAX_PAGES)*100
            try:
                page = reader.pages[index]
                pages.append({"page": page.extract_text()})
                self.animate_percentage(percentage)
            except IndexError:
                self.animate_percentage(percentage)
                pass
        
        f = open(result_json, 'w')
        content = f"\"pages\":{str(pages)}"
        f.write(content)
        f.close()
        self.is_finish = True
        print(f"Conversion finished with {f'{str(self.sec_to_min)} minute(s)' if self.sec_to_min >= 1 else f'{str(self.t.seconds)} second(s)'}!")

    def animate_percentage(self, p:int):
        system('clear')
        percentage = f"{p}%"
        holder = f"__________\t{percentage}"
        if p >= 100:
            print("##########\t", percentage)
        elif p <= 10:
            print(holder)
        else:
            first_char_num = int(str(p)[0], 10)
            NEW_PROGRESS = holder.replace('_', "#", first_char_num)
            print(NEW_PROGRESS)