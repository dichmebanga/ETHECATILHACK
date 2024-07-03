## Installation
Three dependencies are required to run this script. You can install them using the following command:
```bash
pip install -r requirements.txt
```
Additionally, you need to install ffmpeg. You can download it from [here](https://ffmpeg.org/download.html) for each OS version.
```bash
sudo apt-get install ffmpeg
```

## Usage
To implement this script in your project, you can follow a similar approach as shown below:

# For DrissionPage
```python
from DrissionPage import ChromiumPage 
from RecaptchaSolver import RecaptchaSolver

driver = ChromiumPage()
recaptchaSolver = RecaptchaSolver(driver)
driver.get("https://www.google.com/recaptcha/api2/demo")
recaptchaSolver.solveCaptcha()
```
I have created `test.py` to demonstrate the usage of this script. You can run the `test.py` file to see the script in action.

# For Selenium
Config url in SeleniumRun.py
```python
url = "https://www.google.com/recaptcha/api2/demo"

python SeleniumRun.py
```
You can run the SeleniumRun.py file directly
There will be a version in package form, in the near future.