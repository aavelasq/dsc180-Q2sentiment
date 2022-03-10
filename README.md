# The Effect of Cancel Culture on Sentiment Over Time

This project analyzes the change in public sentiment towards musicians,
from the genres of K-Pop, Hip-Hop, and Pop,
who were cancelled or called out on Twitter due to socially unacceptable behavior.
At this current state of the project, our code will generate visualizations that
show how sentiment changes over time for cancelled individuals 6 months before
and after getting cancelled. To measure sentiment, we utilized three APIs: 
[Google Perspective](https://www.perspectiveapi.com/), [Vader](https://github.com/cjhutto/vaderSentiment),
and [Textblob](https://textblob.readthedocs.io/en/dev/api_reference.html).



## Running the Project
- Install dependencies using `pip install -r requirements.txt`

- To run the project using test data: run `python run.py test`

- To scrape Twitter data: run `python getTweets.py`
    - To change artist and timeframe of tweets, change the query
    - In order to run this script, must obtain a valid Twitter API Key from Twitter
    parameters within the `twitter_scraper function`
    - Saves scraped twitter data to `data\raw`

- To run the project using real data: run `python run.py data`
    - This calls `etl.py` and retrivies data stored `data\temp` folders. The directory where data is stored can be changed in `data-params.json`

- The different sentiment API and library scripts are commented out in `run.py`. To run each one, uncomment each target.
    - To run Google Perpsective API on Twitter data: run 
    `python run.py data toxicity`
    - Before runnning, must obtain Google Developer API Key to run API.
    - Outputs a dataframe with toxicity, severe toxicity, insult,
    and profanity levels and saves to `data\temp`
    - To run TextBlob library on Twitter data: run 
    `python run.py data polarity`
    - Outputs a dataframe with sentiment polarity values and saves
    to `data\out`
    - To run Vader library on Twitter data: run 
    `python run.py data vader`
    - Outputs a dataframe with sentiment polarity values and saves
    to `data\out`

- To calculate some exploratory stats and visualizations: run
    `python run.py data eda`
    - Saves a dataframe of the number of tweets collected per day 
    to `data\out`
    - Saves visualizations of user activity, toxicity, and polarity over time to `data\out`

- To smooth out and compute rolling average of sentiment data:
    run `python run.py data preprocessing`
    - Saves rolling average dataframe to `data\temp`

- To generate results for first sub-question: 
    - run `python run.py data typefOfIssue`
        - Saves dataframes with type of issue data to `data\temp\rq1_type`
    - run `python run.py visuals_ti`
        - Saves type of issue visualizations to `data\out\rq1_type`

- To generate results for second sub-question: run `python run.py data background`
    - Saves background dataframes to `data\temp\rq_bg2`
    - Saves background visualizations to `data\out\rq_bg2`

- To generate results for third sub-question: 
    - run `python run.py data parasocial`
        - Saves dataframes with parasocial data to `data\temp\rq3_ps`
    - run `python run.py visuals`
        - Saves parasocial visualizations to `data\out\rq3_ps`