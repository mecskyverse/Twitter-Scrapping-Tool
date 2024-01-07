from ntscraper import Nitter
from openai import OpenAI
import csv
import os
from time import sleep


client = OpenAI(api_key="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")  #openai API key replace it with yours
def main():
    username = input("Enter username ")
    num = int(input("Enter the required number of tweets or -1 for all tweets: "))
    scaper = Nitter(log_level=1, skip_instance_check=False)
    unfilteredData = scaper.get_tweets(username, mode='user', number=num)
    filtered_data = [
            {'link': tweet['link'], 'text': tweet['text'], 'date': tweet['date']}
            for tweet in unfilteredData['tweets']
    ]


    offensive_data = check_offensiveness(filtered_data)
    make_csv(username, offensive_data)

def check_offensiveness(data):
    for item in data:
        try:
            prompt = f"Is the following text offensive? return only true or false no extra word \"{item['text']}\" make sure to return true or false only."
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You should return True or False"}, {"role": "user", "content": prompt}],
            )

            # Extracting the last message (model's response)
            is_offensive = response.choices[0].message.content.lower()
            item["Offensive"] = is_offensive == 'true'

            # If not explicitly true, set to false
            if not item["Offensive"]:
                item["Offensive"] = False
            
        except:
            sleep(0.5)
            continue
    return data

def make_csv(user, offensive_data, output_directory="csvFiles" ):
    filename = f"{user}_tweets.csv"
    try:
        os.makedirs(output_directory, exist_ok=True)  # Create directory if needed
        file_path = os.path.join(output_directory, filename)
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['link', 'text', 'date', 'Offensive']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header row
            writer.writerows(offensive_data)  # Write the tweet data
    except Exception as e:
        print(f"Error writing CSV file: {e}")  # Log any errors

    print(f"CSV file created: {filename}")

main()