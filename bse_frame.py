import json
from os import replace
from urllib.request import urlopen,Request
import pprint
import pandas as pd
import html
from datetime import date, datetime

def fetchdata(updstr,fromdate,todate):
    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat="+updstr+"&strPrevDate="+fromdate+"&strScrip=&strSearch=P&strToDate="+todate+"&strType=C"
    print(url)
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36\(KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    request = Request(url, headers={'User-Agent': agent})
    # store the response of URL
    response = urlopen(request)
    # from url in data
    data_json = json.loads(response.read().decode())['Table']
    #data_json = dload.json(url)
    #print(data_json)
    dataf=pd.DataFrame(data=data_json)
    return dataf
    #print(df)

def searchdata(searchstr,df):
    searched_data = df.loc[(df['NEWSSUB'].str.contains(searchstr, case=False)) | (df['HEADLINE'].str.contains(searchstr, case=False)) | (df['MORE'].str.contains(searchstr, case=False))]
    #print(searched_data)
    searched_data_df= searched_data.loc[:,['SLONGNAME','NEWSSUB','HEADLINE','ATTACHMENTNAME','DissemDT']]
    searched_data_df= searched_data_df.drop_duplicates()
    searched_data_df['LINK']='https://www.bseindia.com/xml-data/corpfiling/AttachLive/'+searched_data_df['ATTACHMENTNAME']
    del searched_data_df['ATTACHMENTNAME']
    searched_data_df.insert(0,'TYPE',searchstr)
    #print(searched_data_df)
    return searched_data_df
    #Convert to HTML
    #result = inv_meet_df.to_html()
    #Print to text file
    #text_file = open("inv_meet.html", "w")
    #text_file.write(result)
    #text_file.close()

now = datetime.now()
today_string = now.strftime("%Y%m%d")
yesterday_string=str(int(today_string)-2)


fromdate=yesterday_string
todate = today_string
comp_df=fetchdata("Company+Update",fromdate,todate)
inv_meet_df = searchdata("Investor Meet",comp_df)
print(inv_meet_df)
credit_rating_df=searchdata("Credit Rating",comp_df)
print(credit_rating_df)
presentation_df=searchdata("Presentation",comp_df)
print(presentation_df)
transcript_df=searchdata("Transcript",comp_df)
print(transcript_df)
press_rel_df=searchdata("Press Release",comp_df)
print(press_rel_df)
contract_df=searchdata("Contract",comp_df)
print(contract_df)
fda_df=searchdata("FDA",comp_df)
print(fda_df)
demerger_df=searchdata("Demerger",comp_df)
print(demerger_df)
buyback_df=searchdata("Buyback",comp_df)
print(buyback_df)
expansion_df=searchdata("Expansion",comp_df)
print(expansion_df)
capex_df=searchdata("Capex",comp_df)
print(capex_df)
capacity_df=searchdata("Capacity",comp_df)
print(capacity_df)
prefer_df=searchdata("Prefer",comp_df)
print(prefer_df)
delist_df=searchdata("Delisting",comp_df)
print(delist_df)
resignation_df=searchdata("Resignation",comp_df)
print(resignation_df)

corp_df=fetchdata("Corp.+Action",fromdate,todate)
bonus_df = searchdata("Bonus",corp_df)
print(bonus_df)
split_df = searchdata("Split",corp_df)
print(split_df)

insider_df=fetchdata("Insider+Trading+%2F+SAST",fromdate,todate)
sast_df = searchdata("SAST",insider_df)
print(sast_df)

agm_df=fetchdata("AGM%2FEGM",fromdate,todate)
egm_df = searchdata("EGM",agm_df)
print(egm_df)
ar_df = searchdata("Annual Report",agm_df)
print(ar_df)

#Append all the Dataframes to create Table
combined_data = pd.concat([inv_meet_df,credit_rating_df,presentation_df,transcript_df,press_rel_df,contract_df,fda_df,demerger_df,buyback_df,expansion_df,capex_df,capacity_df,prefer_df,delist_df,resignation_df,bonus_df,split_df,sast_df,egm_df,ar_df],axis=0,ignore_index=True)
print(combined_data)

output_name_html=today_string+"to"+yesterday_string+".html"
html_output= combined_data.to_html()
replace_beginning=html_output.replace('<td>https','<td><a href="https')
replace_end = replace_beginning.replace('.pdf','.pdf" target="_blank">Link</a>')
replace_final = replace_end.replace('.PDF','.pdf" target="_blank">Link</a>')

print('Writing HTML file ',output_name_html)
text_file = open(output_name_html, "w")
text_file.write(replace_final)
text_file.close()

#output_name_xlsx=today_string+"to"+yesterday_string+".xlsx"
#combined_data.to_excel(output_name_xlsx)

print('To date',today_string)
print('From Date',yesterday_string)