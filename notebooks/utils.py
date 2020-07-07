import numpy as np
import scipy.optimize
import pandas as pd
import json
import gzip

def fit_exp(vals, do_sigma=True):
    # takes pd.Series of values with datetime index
    # and returns dictionary with exponential fit results
    # `do_sigma` toggles on poisson errors (clipped to be at least 2.0
    # to be roughly correct for observed points of 0)

    if vals.max() < 2: return dict()

    secs = vals.index.to_numpy().astype(int)/1e9
    secs -= secs.min()
    days = secs/86400.
    cases = vals.values

    xs, ys = days, cases

    extra = dict()
    if do_sigma:
        extra["sigma"] = np.clip(vals**0.5, 2.0, None)
    try:
        def func(x,a=1.0,b=0.5,c=0.):
            return a*np.exp(b*(x-c))
        pars,cov = scipy.optimize.curve_fit(func,  xs,  ys, **extra)
    except:
        return dict()
        
    ypred = func(xs, *pars)
    # doubling time in days
    td = 1.0/(pars[1]*np.log(np.exp(1))/np.log(2))
    return dict(xs=xs, ys=ys, ypred=ypred, pars=pars, cov=cov, td=td)


def load_df_nytimes(counties=True, cases=True, cumulative=True, avg_over=1):
    """
    Return nytimes dataframe of cumulative cases/deaths (`cases`=True/False) 
    per county/state (`counties`=True/False), averaging over
    past `avg_over` days (`1` means no averaging).
    """
    fname = "../sources/nytimes/data/cases.json.gz"
    df_total = pd.read_json(fname)
    df_total["date"] = pd.to_datetime(df_total["date"])
    df_total = df_total.sort_values(["date"])

    df_total["place"] = df_total["county"].str.cat(df_total["state"], sep=", ")

    which = "cases" if cases else "deaths"

    def get(key):
        # average over last `avg_over` days (1 means instantaneous/no averaging)
        return pd.pivot_table(
            df_total.groupby(["date",key])[which].sum().reset_index(),
            values = which,
            index = "date",
            columns = key,
        ).fillna(0.).rolling(avg_over,center=False).mean()

    df = get("place" if counties else "state")

    if not cumulative:
        df = df.diff(1).dropna()

    return df

def load_df_florida():
    """
    Return florida case dataframe
    """

    df = pd.read_json("../sources/florida/data/data.json.gz")
    df = df.drop(["edvisit","county","age_group","chartdate","case","case_"],axis=1, errors="ignore")
    df = df.rename({"case1":"case"},axis=1)

    df["died"] = df["died"].map({"Yes":True,"NA":False}).fillna(False)

    df = df[df["age"] != "NA"]
    df = df[~df["age"].isna()]
    df = df[df["gender"] != "Unknown"]
    df["gender"] = df["gender"].str[0]
    # df["age"] = df["age"].astype(int)

    for k in ["case","eventdate"]:
        df[k] = pd.to_datetime(df[k].str.split(" ",1).str[0])
    #     df[k] = pd.to_datetime(df[k], unit="ms")
    df["known_status"] = (df["hospitalized"]=="YES") | (df["hospitalized"]=="NO")

    return df


def load_df_googlemobility():
    """
    Return gooble mobility dataframe
    """
    df = pd.read_csv("../sources/googlemobility/data/data.csv.gz")
    df = df.rename({
        "country_region_code":"code",
        "country_region":"country",
        "sub_region_1":"sr1",
        "sub_region_2":"sr2",
        "date":"date",
        "retail_and_recreation_percent_change_from_baseline": "retail_recreation",
        "grocery_and_pharmacy_percent_change_from_baseline": "grocery_pharmacy",
        "parks_percent_change_from_baseline": "parks",
        "transit_stations_percent_change_from_baseline": "transit_stations",
        "workplaces_percent_change_from_baseline": "workplaces",
        "residential_percent_change_from_baseline": "residential",
        },axis="columns")
    df = df.drop(["iso_3166_2_code","census_fips_code"],axis="columns")
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_df_applemobility():
    """
    Return apple mobility dataframe
    """
    fname = "../sources/applemobility/data/data.csv.gz"
    df = pd.read_csv(fname)
    df = df.drop(["alternative_name"],axis="columns")

    datecols = df.filter(regex="[0-9].*").columns
    df = (
            df.pivot_table(
                values=datecols,
                index=["geo_type","region","country","sub-region"],
                columns="transportation_type"
                )
            .stack(level=0)
            .reset_index()
            .rename({"level_4":"date"},axis="columns")
            )
    df["date"] = pd.to_datetime(df["date"])

    return df

if __name__ == "__main__":

    # print(load_df_nytimes())
    # print(load_df_florida())
    # print(load_df_googlemobility())
    print(load_df_applemobility())

