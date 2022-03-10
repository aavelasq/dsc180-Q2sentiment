# The Effect of Cancel Culture on Sentiment Over Time

This project analyzes the change in public sentiment towards musicians
who were cancelled on English-speaking Twitter due to socially unacceptable behavior.
Specifically, we looked at how the 
type of issue, the background of the artist, and the strength of their
parasocial relationship with their fans affected sentiment towards them over time. 
For our analysis, we chose to focus on music artists from three different genres: 
K-Pop, Hip-Hop, and Western Pop. 
To measure sentiment, we utilized the 
[Google Perspective API](https://www.perspectiveapi.com/). 

## Running the Project
- Install dependencies using `pip install -r requirements.txt`

- To run the project using test data: run `python run.py test`

- To scrape Twitter data: run `python getTweets.py`
    - In order to run this script, must obtain valid Twitter API keys and save to a 
    file named `twitterkeys.py`
    - To change artist and timeframe of tweets, change the query attribute in the `query_params` variable
    - Saves scraped Twitter data with columns `id, text, author_id, created_at` to `data\raw`

- To run the project using real data: run `python run.py data`
    - This calls `etl.py` and retrieves data stored in `data\temp` folders. The directory where data is stored can be changed in `data-params.json`

- The different sentiment API and library scripts are found in `run.py`.
    - To run Google Perpsective API script on Twitter data: run 
    `python run.py data toxicity`
        - Before runnning, must obtain Google Developer API keys to run API script.
        - Outputs a dataframe containing toxicity, severe toxicity, insult, 
        and profanity probability scores and saves to `data\temp`
    - To run TextBlob library script on Twitter data: run 
    `python run.py data polarity`
        - Outputs a dataframe with sentiment polarity values and saves to `data\out`
    - To run Vader library script on Twitter data: run 
    `python run.py data vader`
        - Outputs a dataframe with sentiment polarity values and saves to `data\out`

- To calculate some exploratory statistics and visualizations: run
    `python run.py data eda`
    - Saves a dataframe containing the number of tweets collected per day 
    to `data\out`
    - Saves visualizations of user activity, toxicity, and polarity over time to `data\out`

- To smooth out short-term trends and compute rolling average of sentiment data:
    run `python run.py data preprocessing`
    - Saves rolling average dataframe to `data\temp`

- To generate results for first sub-question (type of issue): 
    - run `python run.py data typefOfIssue`
        - Saves dataframes to `data\temp\rq1_type`
    - run `python run.py visuals_ti`
        - Saves visualizations to `data\out\rq1_type`

- To generate results for second sub-question (background of artist): run `python run.py data background`
    - Saves dataframes to `data\temp\rq_bg2`
    - Saves visualizations to `data\out\rq_bg2`

- To generate results for third sub-question (parasocial relationships): 
    - run `python run.py data parasocial`
        - Saves dataframes to `data\temp\rq3_ps`
    - run `python run.py visuals`
        - Saves visualizations to `data\out\rq3_ps`