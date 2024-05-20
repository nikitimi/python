from PyPDF2 import PdfReader
from os import path, system
from time import sleep
from threading import Thread

# print(path.expanduser('~'))

class Timer:
    seconds = 0

    def timer(self):
        global is_finish
        while not is_finish:
            self.seconds += 1
            sleep(1)

def process_with_ocr(filepath:str):
    global is_finish
    if not path.isfile(filepath):
        return print(f"{filepath} is not a page")
    
    pages:list[dict[str,str]] = []
    reader = PdfReader(filepath)
    MAX_PAGES = len(reader.pages)

    for index in range((MAX_PAGES+1)):
        page = reader.pages[index]
        pages.append({"page": page.extract_text()})
        percentage = ((index)/MAX_PAGES)*100
        animate_percentage(percentage)
    
    result_json = './result.json'
    if not path.isfile(result_json):
        f = open(result_json, 'w')
        content = f"\"pages\":{str(pages)}"
        f.write(content)
        f.close()
    is_finish = True

def animate_percentage(p:int):
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
    sleep(.5)
    
if __name__ == "__main__":
    filepath = "/mnt/c/Users/Admin/Desktop/ojt/MTAP/B. Reference Books/2. Microbiology (Bacte & MycoViro)/Other books/Copy of Burton’s Microbiology for the Health Sciences 11th Ed.pdf"
    is_finish = False
    t = Timer()
    Thread(target=t.timer, daemon=True).start()

    sec_to_min = t.seconds/60

    process_with_ocr(filepath)
    print(f"Conversion finished with {f'{str(sec_to_min)} minute(s)' if sec_to_min >= 1 else f'{str(t.seconds)} second(s)'}!")
