from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
import csv  
from bs4 import BeautifulSoup  
from urllib.parse import urlparse  
import tkinter as tk
import time  
import re  
import json  
# Create a tkinter window
window = tk.Tk()

# //button style
button_size = (35, 2)
button_gap = 2 
screen_margin = 4





# Configure Chrome options to run in headless mode  
chrome_options = Options()  
chrome_options.add_argument('--headless')  
chrome_options.add_argument('--disable-gpu')  # To avoid an error message  

# Create a new WebDriver instance with the configured options  



def on_button_click(player):
    print(f"Button for player {player[3]} clicked!")
    getgame(player[3])

def getgame(link):    
    try:  
        driver = webdriver.Chrome(options=chrome_options)  
        url=link+'/match-summary'
        base_url = urlparse(url)._replace(fragment='').geturl()   
        driver.get(base_url)
        time.sleep(5)
        page_source = driver.page_source 
        soup = BeautifulSoup(page_source, 'html.parser')  
        script_tags = soup.find_all('script')  
        data_without_script_tags = re.sub(r'<script.*?>|</script>', '', str(script_tags[14]), flags=re.DOTALL)  
        start_index = data_without_script_tags.find('"eventParticipantEncodedId"')  
        output_string = data_without_script_tags[:start_index]
        findex=output_string.find('"participantsData"')  
        result=output_string[findex:]
        result="{"+result[:-1]+"}"
        data = json.loads(result)  
        detail_data=[["position","player","ranking"]]
        for item in data["participantsData"]["home"]:
            row=["home",item["name"],item["rank"][0]+item["rank"][1]]
            detail_data.append(row)

        for item in data["participantsData"]["away"]:
            row=["away",item["name"],item["rank"][0]+item["rank"][1]]
            detail_data.append(row)
        csv_file = 'matchdetail.csv' 

        with open(csv_file, mode='w', newline='') as file:  
            writer = csv.writer(file)  
            for row in detail_data:  
                writer.writerow(row)  

        preodds_data=[["oddsType0","up/down0","oddsValueInner0","oddsType1","up/down1","oddsValueInner1"]]
        driver.get(url)
        page_source = driver.page_source  
        soup = BeautifulSoup(page_source, 'html.parser')  
        odds = soup.find_all('div', class_='oddsRowContent')  
        for odd in odds:
            oddsTypes = odd.find_all('span', class_='oddsType')
            oddtypearr=[]
            dirarr=[]
            oddvalarr=[]
            prematchorderrow=[]
            for oddtype in oddsTypes:
                oddtypess=oddtype.get_text()        
                oddtypearr.append(oddtypess) 
            oddsValueInners = odd.find_all('span', class_='oddsValueInner')
            for oddval in oddsValueInners:
                oddsValueInnerss=oddval.get_text()
                
                parent_oddsValueInner = oddval.find_parent('span').get('class')
            
                oddvalarr.append(oddsValueInnerss)
                if "up" in parent_oddsValueInner:  
                    dir="up" 
                elif "down" in parent_oddsValueInner:    
                    dir="down" 
                else: dir=""
                dirarr.append(dir)
            preodds_data.append([oddtypearr[0],dirarr[0],oddvalarr[0],oddtypearr[1],dirarr[1],oddvalarr[1]]) 

        csv_file = 'prematchodds.csv' 
        with open(csv_file, mode='w', newline='') as file:  
            writer = csv.writer(file)  
            for row in preodds_data:  
                writer.writerow(row)  
    except Exception as e:  
        print('An error occurred:', e)  

    finally:  
        # Quit the WebDriver session  
        driver.quit()



try:  
    driver = webdriver.Chrome(options=chrome_options)  
    driver.get('https://www.flashscore.com/tennis/atp-singles/hamburg/#/IXBmIkp4/draw')  

    # Get the page source  
    page_source = driver.page_source  
    soup = BeautifulSoup(page_source, 'html.parser')  
    today = soup.find('div', class_='leagues--live contest--leagues')
    rows = today.find_all('div', class_='event__match')  
    data=[["time","player","score","link","nationality"]]
    print(len(rows))
    for div_tag in rows: 
        href_value=''
        event_time_value=''
        flag1=''
        player1_value=''
        flag2=''
        player2_value=''
        score1_value=''
        score2_value=''

        a_tag = div_tag.find('a')  
        if a_tag:  
            href_value = a_tag.get('href')  
            # print(href_value)     

        event_time = div_tag.find('div', class_='event__time')  
        if event_time is None:  
            event_time = div_tag.find('div', class_='event__stage')
        if event_time:  
            event_time_value = event_time.get_text() 
            # print(event_time_value)   

        flag_tag1 = div_tag.find('span',class_='event__logo--home')  
        if flag_tag1 :  
            flag1= str(flag_tag1.get('title')  )
            # print(flag1)    

        player1= div_tag.find('div',class_='event__participant--home') 
        if player1:  
            player1_value = player1.get_text() 
            # print(player1_value)  

        flag_tag2 = div_tag.find('span',class_='event__logo--away')  
        if flag_tag2 :  
            flag2= str(flag_tag2.get('title')  )
            # print(flag2) 

        player2= div_tag.find('div',class_='event__participant--away') 
        if player2:  
            player2_value = player2.get_text() 
            # print(player2_value)             

        score1= div_tag.find('div',class_='event__score--home') 
        if score1:  
            score1_value = score1.get_text() 
            # print(score1_value) 

        score2= div_tag.find('div',class_='event__score--away') 
        if score2:  
            score2_value = score2.get_text() 
            # print(score2_value) 


        row=[event_time_value,player1_value+":"+player2_value,score1_value+":"+score2_value, href_value, flag1+":"+flag2]
        data.append(row)


    # with open('first.html', 'w', encoding='utf-8') as file:  
    #     file.write(str(soup)  )
    # print('Page source saved to detail.html') 

    csv_file = 'todaysmatches.csv' 
    with open(csv_file, mode='w', newline='') as file:  
        writer = csv.writer(file)  
        for row in data:  
            writer.writerow(row)  
    print('Page source saved to response.html')  

except Exception as e:  
    print('An error occurred:', e)  

finally:  
    # Quit the WebDriver session  
    driver.quit()

if len(data)>=1:
    data.pop(0)
for player in data:
    button = tk.Button(window, text=player[0]+"     "+player[1], width=button_size[0], height=button_size[1], command=lambda p=player: on_button_click(player), justify='left', anchor='w')
    button.pack(anchor='w',padx=screen_margin, pady=screen_margin, ipadx=screen_margin, ipady=screen_margin)

window.mainloop()