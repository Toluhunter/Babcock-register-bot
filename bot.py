from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
import time,getpass,socket,ssl
class bot:
    def __init__(self):
        self.api=webdriver.Chrome('/usr/bin/chromedriver')
        self.api.get('https://umis.babcock.edu.ng/babcock/')
        self.courses={}


    def __wait(self,element,text,timeout=10):
        ready=False
        obj=None
        try:
            obj=WebDriverWait(self.api,timeout).until(
                EC.presence_of_element_located((element,text))
                )
            ready=True
        except :
            pass
        finally:
            return obj,ready
    

    def refresh(self):
        print("\nThere was an issue reaching the site please check your internet connection")
        choice=input('Do you wish retry y/n: ')
        if choice=='y':
            self.api.refresh()
            return True
        self.api.quit()
        return False


    @staticmethod
    def send_text(obj,text,enter=True):
        obj.clear()
        obj.send_keys(text)
        if enter:
            obj.send_keys(Keys.RETURN)


    def login(self,matric,password):
        loading_home=True
        while loading_home:
            login,ready=self.__wait(By.LINK_TEXT,"Students")
            if ready:
                loading_login=True
                login.click()
                while loading_login:
                    user,ready_user=self.__wait(By.ID,"j_username")
                    key,ready_key=self.__wait(By.ID,"j_password")
                    if ready_key and ready_user:
                    
                        self.send_text(user,matric,False)
                        self.send_text(key,password)
                        error,ready=self.__wait(By.CLASS_NAME,"alert-danger",1)
                        if ready:
                            print(error.text)
                            matric=input("Enter your matric number: ")
                            password=input("Enter your umis password: ")
                            try_again,ready=self.__wait(By.CLASS_NAME,"px-4")
                            if ready:
                                try_again.click()
                                return self.login(matric,password)
                            
                        else:
                            return True
                            
                    if not self.refresh():
                        return False

            if not self.refresh():
                return False


    def toggle(self):
        toggler1,ready1=self.__wait(By.CLASS_NAME,"responsive-toggler")
        toggler2,ready2=self.__wait(By.CLASS_NAME,"sidebar-toggler")

        if ready1 and ready2:
            try:
                toggler1.click()
            except ElementNotInteractableException:
                toggler2.click()
            return True
        else:
            return False


    def get_details(self):
        while True:
            details,ready=self.__wait(By.TAG_NAME,"tr") 
            self.api.implicitly_wait(10)
            if ready:
                details=self.api.find_elements_by_tag_name("tr")
                name=details[4]
                name=name.find_elements_by_tag_name("td")[1]
                name=name.text
                more_details=details[41]
                more_details=more_details.find_elements_by_tag_name("a")[0]
                more_details.click()
                details=self.api.find_elements_by_tag_name("tr")
                program=details[10].find_elements_by_tag_name("td")[1]
                self.program=program.text
                print('Welcome '+name)
                print('Course: '+self.program)
                self.api.implicitly_wait(0)
                ready=self.toggle()
                self.api.implicitly_wait(10)
                if ready:
                    lists=self.api.find_elements_by_tag_name("li")
                    register_drop_down=lists[14].find_elements_by_tag_name("a")[0]
                    register_drop_down.click()
                    register=lists[15].find_elements_by_tag_name("a")[0]
                    register.click()
                    return True
            if not self.refresh:
                return False


    def register(self):
        loading_register=True
        while loading_register:
            
            ready_click=self.toggle()
            profile,ready=self.__wait(By.ID,"menu112")
            if ready and ready_click:
                
                profile.click()
                if self.get_details():
                    start_register=self.api.find_element_by_name("actionprocess")
                    semester=start_register.get_attribute('value').split('.')[1]
                    semester+="st" if semester=='1' else 'nd'
                    print(f"\nStarting registration for %s semester"%semester)
                    start_register.click()
                    time.sleep(60)
                    self.api.quit()
                    return
                    
                # toggler.click()
            
            if not self.refresh():
                print("Error registreing user")
                break
                
def main():
    try:
        test_connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        test_connection=ssl.wrap_socket(test_connection)
        test_connection.connect(("umis.babcock.edu.ng",443))
        test_connection.settimeout(5)
    except Exception:
        print("Unable to establish a connection with umis")
        return

    matric=input('Enter matric Number: ')

    password=getpass.getpass('Enter Umis password: ')
    # level=input("Enter current level e.g 100,200,300 :")"
    try:
        umis=bot()
        if  umis.login(matric,password): 
            print("\nSucessufully Logged In\n")
            umis.register()
        else:
            print("There was an issue authenticating user")
    except Exception:
        print("No internet connection")

if __name__ == '__main__':
    main()