# Twitter Scrapping Python

This guide provides instructions on setting up this project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
    - [Clone the Repository](#clone-the-repository)
3. [Project Structure](#project-structure)


## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/mecskyverse/TwitterScrap.git
cd TwitterScrap/Method-1
pip install -r requirements.txt
```
after installing dependencies of Method-1 we have to install few dependencies of Method-2 as well
```
cd TwitterScrap/Method-2
pip install -r requirements.txt
```

## Project Structure
![image](https://github.com/mecskyverse/TwitterScrap/assets/91150257/1b37016f-7f5f-4320-8635-edec1e3955ea)<br>
As you can see there are two main folders Method-1 and Method-2 I will let you know the pros and cons of both the method. In Method-1 I have used hardcoded web-scrapping through python and selenium it works good and there is no limit on how much data we want to scrape from it. It will scrape both tweets and replies of a profile and with the use of chatgpt api it will build a Excel file in folder Named Excel. 

In Method-2 we use a package named ntscraper it uses nitter to scrape the data from twitter profile. Its fast more efficient but the only drawback it has is that it is not able to fetch replies by a user it can only fetch tweets by a user. 

Both of these methods are good and I have tried to keep the code simple in Method-1 we can customize the code in Method-2 we have a good processing speed. 

In both the folders index.py is the starting point where we have to start the programme. 

## API Keyst
There is mainly openai API key and Twitter Token at one place that we need to replace in the file by which we can check the offensiveness of a tweet. 
You can find openAI API Key here: [API-Key](https://platform.openai.com/api-keys)
#### In Method-1
./files/conf.json here in the key named apikey we have to place openAI API key and a token of twitter in key named token.
#### In Method-2 
In index.py at line at you have to replace openAI api key.

