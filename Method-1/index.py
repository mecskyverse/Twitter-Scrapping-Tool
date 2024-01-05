from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from logger import Logger
import json
from openai import OpenAI
from tweet import Tweet
from excel import Excel
from time import sleep



def main():
    log.warning("Loading configurations...")
    client = OpenAI(api_key=conf["apiKey"])
    driver = open_driver(conf["headless"], conf["userAgent"])
    driver.get("https://twitter.com/")
    set_token(driver, conf["token"])
    driver.get("https://twitter.com/")

    log.warning("Starting...")
    username = input("Enter username ")
    num = int(input("Enter the required number of tweets or -1 for all tweets: "))
    url = f'https://twitter.com/{username}/with_replies'
    data = profile_search(driver, username, num, url)
    print(data)
    print('Data Scrapping Done Offensive check.....')
    offensiveCheckData = check_offensiveness(data, client)
    print('results ',offensiveCheckData)
    
    log.warning("Saving...")
    Excel(username, offensiveCheckData, conf["output_form"])


def profile_search(
        driver: webdriver.Chrome,
        username,
        num,
        url
):
    
    driver.get(url)

    log.warning("Fetching...")
    Ad = [0]
    results = []
    while len(results) < num or num == -1:
        tweet = Tweet(driver, Ad)
        if hasattr(tweet, 'tweet_url'):
            try:
                currentUrl = tweet.get_url()
                text = tweet.get_text()
                if currentUrl.startswith(f'https://twitter.com/{username}') and text:
                    data = {
                        "URL": url,
                        "Date": tweet.get_date(),
                        "Text": tweet.get_text(),
                        "Lang": tweet.get_lang(),
                    }
                    results.append(data)

                    # Save results to a JSON file
                    json.dump(results, open("./files/temp.json", "w"))

                    # Log information
                    log.info(f"{len(results)}: {url}")

            except Exception as e:
                # Handle the exception (e.g., log or print an error message)
                print(f"Error processing tweet: {e}")
        else:
            break        
    return results

def check_offensiveness(data, client):
    for item in data:
        prompt = f"Is the following text offensive? return only true or false no extra word \"{item['Text']}\" make sure to return true or false only."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Updated to the latest model
            messages=[{"role": "system", "content": "You should return True or False"}, {"role": "user", "content": prompt}],
        )
        
        # Extracting the last message (model's response)
        is_offensive = response.choices[0].message.content.lower()
        print('offence ', is_offensive)
        item["Offensive"] = is_offensive == 'true'

        # If not explicitly true, set to false
        if not item["Offensive"]:
            item["Offensive"] = False

    return data
  


def open_driver(
        headless: bool,
        agent: str
) -> webdriver.Chrome:
    
    options = Options()

    options.add_argument('--log-level=3')
    options.add_argument('ignore-certificate-errors')

    if headless:
        options.add_argument('--headless')

    options.add_argument(f"user-agent={agent}")
    
    driver = webdriver.Chrome(options=options)

    return driver

def set_token(
        driver: webdriver.Chrome,
        token: str
) -> None:
    src = f"""
            let date = new Date();
            date.setTime(date.getTime() + (7*24*60*60*1000));
            let expires = "; expires=" + date.toUTCString();

            document.cookie = "auth_token={token}"  + expires + "; path=/";
        """
    driver.execute_script(src)

def load_conf() -> dict:
    with open("./files/conf.json", "r") as file:
        return json.loads(file.read())


if __name__  == "__main__":
    conf = load_conf()
    log = Logger()
    main()


