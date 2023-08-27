from bs4 import BeautifulSoup
from selenium import webdriver

new=[]

def difference(string1, string2):
  # Split both strings into list items
  string1 = string1.split()
  string2 = string2.split()

  A = set(string1) # Store all string1 list items in set A
  B = set(string2) # Store all string2 list items in set B
 
  str_diff = A.symmetric_difference(B)
  isEmpty = (len(str_diff) == 0)
 
  if isEmpty:
    return False
  else:
    return True

def run_app():
    with open('config.txt', "r") as f:
        mangas=[]
        lines=f.readlines()
    for line in lines:
        mangas.append(line.replace(" - \n",""))
    for manga in mangas:
        url="https://manga4life.com/manga/"+manga.replace(" ","-").split("---")[0]
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver=webdriver.Chrome(PATH)
        driver.get(url)
        elem = driver.find_element("xpath", "/html/body/div[2]/div/div/div/div/div[2]")
        source_code = elem.get_attribute("outerHTML")
        driver.quit()
        soup=BeautifulSoup(source_code,'html.parser')
        chapter_num=soup.find('span').text.replace(" ","").replace("Chapter","").replace("\n","").replace("\t","").replace("Episode","")
        new_line=manga.split(" - ")[0]+" - "+chapter_num
        for line in lines:
            if manga in line:
                if difference(line, new_line):
                    new.append(manga.split(" - ")[0])
                    with open('config.txt', "r") as f:
                        lines=f.readlines()
                    with open('config.txt', "w") as f:
                        for line in lines:
                            if manga.lower() in line.lower():
                                continue
                            else:
                                f.write(line)
                        f.write(new_line+"\n")
                        f.flush()
    if len(new)==0:
        print("No new manga chapters!")
    else:
        print("This is the list of mangas with new chapters:")
        print(new)

def config():
    config_choice=input("Do you want to remove(r) or add(a) an manga to the list?")
    while not config_choice=="r" and not config_choice=="a":
        config_choice=input("Please choose one of the provided options!")
    if config_choice=="a":
        run=True
        while run:
            manga=input("Please type the name of the manga that you want to add as it is on 'Manga4Life' website:")
            url="https://manga4life.com/manga/"+manga.lower().replace(" ","-")
            PATH="C:\Program Files (x86)\chromedriver.exe"
            driver=webdriver.Chrome(PATH)
            driver.get(url)
            elem = driver.find_element("xpath", "/html/body/div[2]/div/div/div/div/div[2]")
            source_code = elem.get_attribute("outerHTML")
            driver.quit()
            soup=BeautifulSoup(source_code,'html.parser')
            chapter_num=int(soup.find('span').text.replace(" ","").replace("Chapter","").replace("\n","").replace("\t","").replace("Episode",""))
            with open('config.txt', "a") as f:
                f.write(str(manga)+f" - {chapter_num}\n")
                f.flush()
            run_again=input("Do you want to add another one (y/n)?")
            if run_again=="y":
                continue
            else:
                run=False
    elif config_choice=="r":
        run=True
        while run:
            manga=input("Please type the name of the manga that you want to remove as it is on 'Manga4Life' website:")
            with open('config.txt', "r") as f:
                lines=f.readlines()
            with open('config.txt', "w") as f:
                for line in lines:
                    if manga.lower() in line.lower():
                        continue
                    else:
                        f.write(line)
                f.flush()
            run_again=input("Do you want to remove another one (y/n)?")
            if run_again=="y":
                continue
            else:
                run=False

choice=input("Do you want to run the app(a) or open configuration(c)?")
while not choice=="a" and not choice=="c":
    choice=input("Please choose one of the provided options!")
if choice=="a":
    run_app()
elif choice=="c":
    config()