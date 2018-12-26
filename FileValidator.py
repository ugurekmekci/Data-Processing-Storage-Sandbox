import pandas as pd

ExcelColumnList = {"Grup":str, "Şirket":str,"Ülke":str, "Lokasyon/Proje":str,
                   "Banka":str, "Şube":str,"Mevduat/Kredi\nFaiz Oranı":float,
                   "Vade/Kredi Baş.\nTarihi":pd._libs.tslibs.timestamps.Timestamp,
                   "Vade/Kredi Bitiş\nTarihi":pd._libs.tslibs.timestamps.Timestamp,
                   "Para Birimi":str, "Tutar":float,"İşlem Tipi":str}


#function below supposed to be returning True or False argument after its all steps completed succesfully.
def IsValid(Path):
    xl = pd.ExcelFile(Path)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        #print(len(df.index))
        for i in df.columns.values: #"i" is a column name
            for p in df[i]: #p is the data for under 'i'
                for k,v in ExcelColumnList.items():
                    if (i==k and isinstance(p,v)):
                        print(p,type(p))
                    elif i==k:
                        raise Exception('{0} {1} {2}'.format(i,'Column Only Accepts:',v))
                        exit()
        exit()

    #print (list(df.columns.values))


    return True



if __name__ == "__main__":
    print(IsValid("Banka_Mevduat_Kredi_Vade_Oranları_toros Tarım.xlsx"))
