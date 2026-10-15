import pandas as pd





def getDataFromCsv(fileName):
    
    df=pd.read_csv(fileName,on_bad_lines='skip')
    # listOfDicts = df.to_dict(orient='records')
    # print(listOfDicts)
    # return listOfDicts
    return df




