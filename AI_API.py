from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from AI2 import AI

PORT = 5001
HOST = '0.0.0.0'
DEVICE = 'cpu'
TEXT_GENERATION_WEBUI_URL = "http://127.0.0.1:7860"

app = Flask(__name__)


option = webdriver.ChromeOptions()
option.binary_location = "./chrome-linux64/chrome"
driver = None

textarea_xpath = '//*[@id="chat-input"]/label/textarea'
new_chat_button_id = "component-79"
parameter_tab_button_id = "parameters-button"
chat_tab_under_parameters_button_id = "component-266-button"
dropdown_xpath = '//*[@id="character-menu"]/div[2]/div[2]/div[1]/div/input' # later check if attr aria-expanded="true"
chat_tab_button_id = "chat-tab-button"

def select_character():
    driver.find_element(By.ID, parameter_tab_button_id).click()
    time.sleep(1)
    driver.find_element(By.ID, chat_tab_under_parameters_button_id).click()
    time.sleep(1)
    driver.find_element(By.XPATH, dropdown_xpath).click()
    time.sleep(1)
    driver.find_element(By.XPATH, dropdown_xpath).send_keys(Keys.CONTROL + "a")
    driver.find_element(By.XPATH, dropdown_xpath).send_keys(Keys.BACKSPACE)
    driver.find_element(By.XPATH, dropdown_xpath).send_keys("AI")
    time.sleep(1)
    driver.find_element(By.XPATH, dropdown_xpath).send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element(By.ID, chat_tab_button_id).click()
    
def select_model():
    model_tab_button_id = "model-tab-button"
    listbox_xpath = '//*[@id="component-341"]/div[2]/div/div[1]/div/input'
    model_name = 'codellama_CodeLlama-7b-Python-hf'
    load_button_id = "component-343"
    checkbox_disk_id = "component-411"
    checkbox_cpu_id = "component-399"
    
    driver.find_element(By.ID, model_tab_button_id).click()
    time.sleep(1)
    driver.find_element(By.XPATH, listbox_xpath).click()
    time.sleep(1)
    driver.find_element(By.XPATH, listbox_xpath).send_keys(Keys.CONTROL + "a")
    driver.find_element(By.XPATH, listbox_xpath).send_keys(Keys.BACKSPACE)
    driver.find_element(By.XPATH, listbox_xpath).send_keys(model_name)
    time.sleep(1)
    driver.find_element(By.XPATH, listbox_xpath).send_keys(Keys.RETURN)
    time.sleep(1)
    
    cpu_span = driver.find_element(By.XPATH, '//*[@id="component-399"]/label')
    disk_span = driver.find_element(By.XPATH, '//*[@id="component-411"]/label')
    
    cpu_span.send_keys(Keys.RETURN)
    time.sleep(1)
    disk_span.send_keys(Keys.RETURN)     
    
    time.sleep(1)
    driver.find_element(By.ID, load_button_id).click()
    
    time.sleep(3)
    
    driver.find_element(By.ID, chat_tab_button_id).click()

def select_parameter():
    listbox_xpath = '//*[@id="component-190"]/div[2]/div/div[1]/div/input'
    driver.find_element(By.ID, parameter_tab_button_id).click()
    time.sleep(1)
    driver.find_element(By.XPATH, listbox_xpath).click()
    time.sleep(1)
    driver.find_element(By.XPATH, listbox_xpath).send_keys(Keys.CONTROL + "a")
    driver.find_element(By.XPATH, listbox_xpath).send_keys(Keys.BACKSPACE)
    driver.find_element(By.XPATH, listbox_xpath).send_keys("actual")
    time.sleep(1)
    driver.find_element(By.XPATH, listbox_xpath).send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element(By.ID, chat_tab_button_id).click()
    
    
    
def get_num_class_child_elements(parent_element, child_class_name) -> int:
    num = 0
    try:
        
        num = len(parent_element.find_elements(By.CLASS_NAME, child_class_name))
    except:
        num =  -1
    return num

def get_class_child_elements(parent_element, child_class_name):
    return parent_element.find_elements(By.CLASS_NAME, child_class_name)

def start_new_chat():
    new_chat_button = driver.find_element(By.ID, new_chat_button_id)
    
    masseges_area = driver.find_element(By.CLASS_NAME, "messages")
    num_msg = get_num_class_child_elements(masseges_area, "message")
    print("num_msg: ", num_msg)
    if num_msg == -1: 
        print("Error") 
        return 'Error'
    elif num_msg == 0:
        select_character()
        return 'Selecting character'
    elif num_msg > 1:
        new_chat_button.click()
    return 'Starting a new chat!'


def send_chat(text):
    try:
        textbox = driver.find_element(By.XPATH, textarea_xpath)
    except:
        return 'Error: textbox not found'
    time.sleep(1)
    try:
        textbox.send_keys(text)
        textbox.send_keys(Keys.RETURN)
    except:
        return 'Error: sending text failed'
    
    return 'Sent message: ' + text

def recv_chat():
    
    try:
        masseges_area = driver.find_element(By.CLASS_NAME, "messages")
    except:
        return 'Error: masseges_area not found'
    try:
        num_msg = get_num_class_child_elements(masseges_area, "message")
    except:
        return 'Error: num_msg not found'
    
    if num_msg == -1: 
        return 'Error'
    elif num_msg < 2:
        return 'No message'
    try:
        return  get_class_child_elements(masseges_area, "message")[-1].text
    except:
        return 'Error: txt not found'

    
def wait_until_dots_disappear(driver):
    WebDriverWait(driver, 100).until_not(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'visible-dots')]"))
    )
    return 'Dots disappeared'

@app.route('/')
def hello():
    
    return 'Hello, World!'

@app.route('/start_new_chat')
def start_new_chat():
    return start_new_chat()

@app.route('/chat', methods=['POST'])
def chat():
    text = request.get_json().get('text', '')
    send_chat(text)
    time.sleep(1)
    try:
        wait_until_dots_disappear(driver)
    except:
        return 'try again!'
    
    return recv_chat()

if __name__ == '__main__':
    # driver = webdriver.Chrome(option)
    # option = webdriver.FirefoxOptions()
    # option.binary_location = "/home/atieh/school/p22/talk-with-text-generation-webui/geckodriver"
    driver = webdriver.Chrome(option)
    
    driver.get(TEXT_GENERATION_WEBUI_URL)
    time.sleep(5)
    select_model()
    time.sleep(1)
    select_parameter()
    time.sleep(1)
    select_character()
    app.run(port=5004, host=HOST)
    