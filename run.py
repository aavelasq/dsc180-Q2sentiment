import sys
import pandas as pd

sys.path.insert(0, 'src') # add src to paths

from eda import calculate_stats
from toxicity_script import toxicityFunc

def main(targets):
    # data_config = json.load(open('config/data-params.json'))

    if 'data' in targets:
        # with open('config/data-params.json') as fh:
        #     data_cfg = json.load(fh)

        # data = etl.import_data(**data_cfg)
        data = pd.read_csv(".//data/raw/JAEMIN_rawtweets.csv")

    if 'size' in targets:
        df = pd.read_csv(".//data/temp/JAEMIN_toxicVals2.csv")
        print(len(df))

    if 'eda' in targets:
        calculate_stats(data)

    if 'toxicity' in targets:
        # run on x to y tweets
        toxicityFunc(data[65000:110000], "JAEMIN")

    if 'test' in targets:
        # with open('config/data-params.json') as fh:
        #     data_cfg = json.load(fh)

        # data = etl.import_data(**data_cfg)
        data = pd.read_csv(".//data/raw/kpop_giselle/GISELLE_rawtweets.csv")

        # rq 1 function
        calculate_stats(data, test=True)

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)