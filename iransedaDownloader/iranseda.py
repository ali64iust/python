#not completed yet

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pyautogui
import time
import os
import requests
import codecs

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


#pip install pyautogui
#pip install selenium
#pip install requests

class IranSedaDownloader():
    IranSedaURL="http://kids.iranseda.ir/?VALID=TRUE"
    tabHandle=0

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.action = ActionChains(self.driver)


    def SaveImageAs(self,image1,FullPathToSave):
        self.action.move_to_element(image1).context_click().perform()
        pyautogui.hotkey('command', 'v')
        time.sleep(2)
        pyautogui.press('delete')
        pyautogui.write(FullPathToSave, interval=0.05)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)


        pass

    def makeDirecory(self,path1):
        isExist = os.path.exists(path1 )
        if (not isExist):
            os.mkdir(path1 )

    def GetDetailsprogramNewTab(self,url,WorkingPath):
        print("fetch: " + url)
        self.OpenNewTab(url)
        body_module = self.driver.find_element(By.CLASS_NAME, "button-list")
        doanload = body_module.find_elements(By.TAG_NAME, "a")[-1]
        downloadURL=doanload.get_attribute("href")

        content1 = self.driver.find_element(By.ID, "tags")

        fc=codecs.open(WorkingPath+"content.txt","w",encoding="utf-8")
        fc.write(content1.text)
        fc.close()


        r = requests.get(downloadURL) #, stream=True
        with open(WorkingPath+"1.mp4", 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)

        print("fetch completeg: " + url)
        self.CloseTab() #current page
        #time.sleep(1)
        #Mbox('baste shod?', 'baste shod?????', 1)

    def LoadSubBarnamehayeKodakNewTab(self,WorkingPath):
        #http://kids.iranseda.ir/planList/?VALID=TRUE&p=615  element
        self.makeDirecory(WorkingPath)
        body_module = self.driver.find_element(By.CLASS_NAME, "body-module")
        pages = body_module.find_elements(By.CLASS_NAME, "photo-responsiv")
        images =body_module.find_elements(By.TAG_NAME, "img")
        images_index=0
        pageNumber=0
        for page in pages:
            newtab = page.get_attribute("href")
            #pageNumber = newtab[newtab.find("g=") +2:]
            pageNumber=pageNumber+1
            self.makeDirecory(WorkingPath + str(pageNumber))

            image1 = images[images_index]
            self.SaveImageAs(image1, WorkingPath + str(pageNumber) + "\\" + str(pageNumber) + ".jpg")

            self.GetDetailsprogramNewTab(newtab, WorkingPath + str(pageNumber) + "\\")


            images_index=images_index+1
        pass

    def OpenNewTab(self,url):
        self.tabHandle=self.tabHandle+1
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[self.tabHandle])
        self.driver.get(url)

    def CloseTab(self):
        self.tabHandle = self.tabHandle - 1
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[self.tabHandle])


    def GetBarnamehayeKodakNewTab(self,url,WorkingPath):
        #http://kids.iranseda.ir/planList/?VALID=TRUE&p=615
        self.OpenNewTab(url)
        self.makeDirecory(WorkingPath)

        pagination=self.driver.find_element( By.CLASS_NAME,"pagination")
        pagesLinks=pagination.find_elements(By.TAG_NAME, "a")
        lastPage=pagesLinks[-2]
        lastPageURL= lastPage.get_attribute("href")
        pageCount = int(lastPageURL[lastPageURL.find("pn=") + 3:])
        basePages= lastPageURL[:lastPageURL.find("pn=") + 3]
        newPath=WorkingPath+"1\\"
        self.makeDirecory(newPath)
        self.LoadSubBarnamehayeKodakNewTab(newPath)
        for p in range(2, pageCount+1):
            print("page to load:"+basePages+str(p))
            self.driver.get(basePages+str(p)) #error???
            newPath = WorkingPath + str(p)+"\\"
            self.LoadSubBarnamehayeKodakNewTab(newPath)


        self.CloseTab() #current page


    def Get_BarnamehayeKodak(self):
        currentPath= os.getcwd()+"\\"+"BarnamehayeKodak\\"
        self.makeDirecory(currentPath)


        #main page
        self.driver.get("http://kids.iranseda.ir/homeprogram/?valid=true")

        #get pages col-plus-md-3 col-plus-6 item
        pages = self.driver.find_elements( By.CLASS_NAME,"photo-responsiv")
        #inja
        pageNumber=1
        for page in pages:
            newtab =page.get_attribute("href")
            #pageNumber = newtab[newtab.find("p=")+2:]
            self.makeDirecory(currentPath+str(pageNumber))

            image1 = page.find_element(By.TAG_NAME,"img")
            self.SaveImageAs(image1,currentPath+str(pageNumber)+"\\"+str(pageNumber)+".jpg")

            self.GetBarnamehayeKodakNewTab(newtab,currentPath+str(pageNumber)+"\\")
            pageNumber = pageNumber+1

        #http://kids.iranseda.ir/homeprogram/?valid=true

    def GetPagesLinks(self):
        self.Get_BarnamehayeKodak()

        #self.driver.close()


isd=IranSedaDownloader()
isd.GetPagesLinks()


