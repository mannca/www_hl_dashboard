import pandas as pd
import pickle as pkl
from util.code_hierarchy import mapping_to_top_level
import urllib
from google.cloud import storage


def get_top_level(leaf_categories):
    cats = leaf_categories.split("/")
    top_levels = sorted(set([mapping_to_top_level.get(cat, cat) for cat in cats]))
    return "/".join(top_levels)


def get_data():
    # for when no abs paths
    
    if False:
        df_responses = pd.read_pickle("C:/Users/catie/Documents/MFM/Updated Codes Jan22/data/hl_data_final.pkl")
    else:
        #Load from GCS bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket('wra_what_women_want')
        blob = bucket.blob('data.pkl')
        mybytes = blob.download_as_bytes()
        df_responses = pkl.loads(mybytes)


    # Remove the UNCODABLE responses
    df_responses = df_responses[~df_responses["canonical_code"].isin(["UNCODABLE"])]

    df_responses["canonical_code"] = df_responses["canonical_code"].apply(lambda x: "NOTRELATED" if x == "OTHERQUESTIONABLE" else x)

    df_responses["top_level"] = df_responses.canonical_code.apply(get_top_level)
    df_responses["age_str"] = df_responses["age"].apply(lambda x: "N/A" if x == 0 else x)

    return df_responses