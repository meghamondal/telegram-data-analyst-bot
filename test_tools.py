from tools import download_file, load_dataframe, dataframe_summary

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

path = download_file(url)

print(path)

df = load_dataframe(path)

print(df.head())

print(dataframe_summary(df))