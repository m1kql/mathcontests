from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
import shutil
import numpy as np

if os.path.exists("./CMO/"):
    shutil.rmtree("./CMO/")
os.mkdir("./CMO/")

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

browser = webdriver.Chrome(executable_path="./chromedriver", options=options)

for year in range(1969, 1974):
    year_path = "./CMO/%d/" % year
    exam_path = year_path
    os.mkdir(exam_path)
    for problem in range(1, 10):
        os.mkdir(f"{exam_path}{str(problem)}/")
        url = (
            "https://artofproblemsolving.com/wiki/index.php/%d_Canadian_MO_Problems/Problem_%d"
            % (year, problem)
        )
        browser.get(url)
        try:
            div = browser.find_element_by_class_name("mw-parser-output")
            elements = (element for element in div.find_elements_by_xpath("*"))

            while next(elements).tag_name != "h2":
                pass

            ims = []
            while True:
                element = next(elements)
                if element.tag_name == "h2":
                    break
                location = element.location
                size = element.size
                png = browser.get_screenshot_as_png()
                im = Image.open(BytesIO(png))
                left = location["x"]
                top = location["y"]
                right = location["x"] + size["width"]
                bottom = location["y"] + size["height"]
                im = im.crop((left, top, right, bottom))
                ims.append(im)
            image = np.vstack([np.asarray(im) for im in ims])
            image = Image.fromarray(image)
            image.save(exam_path + f"{str(problem)}/" + "statement.png")
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print("ERROR:", str(e))
            continue


browser.close()
