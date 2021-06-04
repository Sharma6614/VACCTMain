import pandas as pd 
import numpy as np

def CCTPull(CountyVACOVID):
    VAMC = pd.read_csv('data_folder/CleanVAMC.csv',dtype={'VISN':'int','VAMC':'str','FIPS':'str','COUNTY':'str','STATE':'str'})
    UScovid = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')

    #Formatting of NYTimes COVID-19 Data - Country Level
    UScovid[['cases','deaths']] = UScovid[['cases','deaths']].fillna(0).astype(int)
    UScovid['date'] = pd.to_datetime(UScovid['date'])
    UScovid = UScovid.rename(columns={'date':'DATE','cases':'CASES','deaths':'DEATHS'})

    USCasesToday = UScovid.loc[ UScovid.DATE == UScovid.DATE.max(),'CASES'].values[0]
    USCasesYesterday = UScovid.loc[ UScovid.DATE == UScovid.DATE.max() - pd.to_timedelta(1, unit='D'),'CASES'].values[0]
    USNewCases = USCasesToday - USCasesYesterday
    TodayDate = CountyVACOVID['DATE'][0]
    #State level Pulls
    StateDataSet = {}
    StateList = ["Ohio",
                "Indiana",
                "Michigan",
                "Illinois",
                "Wisconsin",
                "Washington",
                "Idaho",
                "Oregon",
                "Alaska",
                "Maryland",
                "Virginia",
                "District of Columbia",
                "Missouri",
                "Alabama",
                "Arizona",
                "Arkansas",
                "California",
                "Colorado",
                "Connecticut",
                "Delaware",
                "Florida",
                "Georgia",
                "Hawaii",
                "Indiana",
                "Iowa",
                "Kansas",
                "Kentucky",
                "Louisiana",
                "Maine",
                "Massachusetts",
                "Minnesota",
                "Mississippi",
                "Missouri",
                "Montana",
                "Nebraska",
                "Nevada",
                "New Hampshire"
                "New Jersey",
                "New Mexico",
                "New York",
                "North carolina",
                "North Dakota",
                "Ohio",
                "Oklahoma",
                "Oregon",
                "Pennsylvania",
                "Rhode Island",
                "South Carolina",
                "South Dakota",
                "Tennessee",
                "Texas",
                "Utah",
                "Vermont",
                "West Virginia",
                "Wyoming"]
    
    
    for state in StateList:
        StateData = CountyVACOVID[CountyVACOVID.STATE == state]
    
        Cases = StateData['CASES'].sum()
        NewCases = Cases - StateData['YESTER_CASES'].sum()
        VACases = StateData['VET_CASES'].sum()
        NewVACases = VACases - StateData['VET_YESTER'].sum()

        values = [Cases, NewCases, VACases, NewVACases]
        StateDataSet['%s' %state] = values
    

    #VISN 10 level Pulls
    VISN10List = VAMC[VAMC.VISN == 10]['FIPS']
    VISN10Data = CountyVACOVID[CountyVACOVID['FIPS'].isin(VISN10List)]

    VISN10Cases = VISN10Data['CASES'].sum()
    VISN10_VACases = VISN10Data['VET_CASES'].sum()

    #VISN 12 level Pulls
    VISN12List = VAMC[VAMC.VISN == 12]['FIPS']
    VISN12Data = CountyVACOVID[CountyVACOVID['FIPS'].isin(VISN12List)]

    VISN12Cases = VISN12Data['CASES'].sum()
    VISN12_VACases = VISN12Data['VET_CASES'].sum()

    #VISN 20 level Pulls
    VISN20List = VAMC[VAMC.VISN == 20]['FIPS']
    VISN20Data = CountyVACOVID[CountyVACOVID['FIPS'].isin(VISN20List)]

    VISN20Cases = VISN20Data['CASES'].sum()
    VISN20_VACases = VISN20Data['VET_CASES'].sum()

    #Facility level Pulls
    DataSet ={}
    VAMCList = [ "Anchorage VA Medical Center", 
    "Portland VA Medical Center",
    "North Las Vegas VA Medical Center",
    "Jonathan M. Wainwright Memorial VA Medical Center",
    "White City VA Medical Center",
    "Roseburg VA Medical Center",
    "Seattle VA Medical Center",
    "Mann-Grandstaff Department of Veterans Affairs Medical Center",
    "Boise VA Medical Center",
    "Jesse Brown Department of Veterans Affairs Medical Center",
    'William S. Middleton Memorial Veterans\' Hospital',
    'Clement J. Zablocki Veterans\' Administration Medical Center',
    "Oscar G. Johnson Department of Veterans Affairs Medical Facility",
    "Lieutenant Colonel Charles S. Kettles VA Medical Center",
    "Battle Creek VA Medical Center",
    "John D. Dingell Department of Veterans Affairs Medical Center",
    "Aleda E. Lutz Department of Veterans Affairs Medical Center", 
    "Fort Wayne VA Medical Center", 
    "Marion VA Medical Center", 
    "Richard L. Roudebush Veterans\' Administration Medical Center", 
    "Cincinnati VA Medical Center", 
    "Chillicothe VA Medical Center", 
    "Louis Stokes Cleveland Department of Veterans Affairs Medical Center", 
    "Dayton VA Medical Center", 
    "Danville VA Medical Center", 
    "Edward Hines Junior Hospital", 
    "Captain James A. Lovell Federal Health Care Center", 
    "Tomah VA Medical Center"
    ]
    
    for vamc in VAMCList:
        FacilityList = VAMC[VAMC.VAMC == vamc]['FIPS']
        FacilityData = CountyVACOVID[CountyVACOVID['FIPS'].isin(FacilityList)]
    
        ECases = FacilityData['VET_CASES'].sum()
        NewCases = ECases - FacilityData['VET_YESTER'].sum()
        TotalCases = FacilityData['CASES'].sum()
        values = [TotalCases, ECases, NewCases]
        DataSet['%s' %vamc] = values
        # print(TotalCases)

    #Hard-coding for Columbus
    COFacilityList = ['39159','39097', '39129','39049','39045','39089','39041','39117'] 
    COFacilityData = CountyVACOVID[CountyVACOVID['FIPS'].isin(COFacilityList)]

    COECases = COFacilityData['VET_CASES'].sum()
    CONewCases = COECases - COFacilityData['VET_YESTER'].sum()

    COValues = [COECases, CONewCases]
    DataSet["Columbus VA Medical Center"] = COValues


    #Establish a cyclical chart to add new rows for every date it is run
    CCTVAChart = pd.read_csv('CCTVAChart2.csv')
    CCTVAChart = CCTVAChart.set_index('index').T.rename_axis('DATE').reset_index()
    CCTVAChart_newrow = pd.DataFrame({ 'DATE': TodayDate,
                            'US Cases': USCasesToday,
                            'New US Cases': USNewCases,
                            
                            'VISN10 Cases': VISN10Cases,
                            'VISN12 Cases': VISN12Cases,
                            'VISN20 Cases': VISN20Cases,

                            'OH Cases': StateDataSet["Ohio"][0],
                            'OH NewCases' : StateDataSet["Ohio"][1],
                            'IN Cases': StateDataSet["Indiana"][0],
                            'IN NewCases' : StateDataSet["Indiana"][1],
                            'MI Cases': StateDataSet["Michigan"][0],
                            'MI NewCases' : StateDataSet["Michigan"][1],
                            
                            'IL Cases': StateDataSet["Illinois"][0],
                            'IL NewCases' : StateDataSet["Illinois"][1],
                            'WI Cases': StateDataSet["Wisconsin"][0],
                            'WI NewCases' : StateDataSet["Wisconsin"][1],
                            
                            'WA Cases': StateDataSet["Washington"][0],
                            'WA NewCases' : StateDataSet["Washington"][1],
                            'OR Cases': StateDataSet["Oregon"][0],
                            'OR NewCases' : StateDataSet["Oregon"][1],
                            'ID Cases': StateDataSet["Idaho"][0],
                            'ID NewCases' : StateDataSet["Idaho"][1],
                            'AK Cases': StateDataSet["Alaska"][0],
                            'AK NewCases': StateDataSet["Alaska"][1],

                            'MD Cases': StateDataSet["Maryland"][0],
                            'MD NewCases' : StateDataSet["Maryland"][1],
                            'VA Cases': StateDataSet["Virginia"][0],
                            'VA NewCases' : StateDataSet["Virginia"][1],
                            'DC Cases': StateDataSet["District of Columbia"][0],
                            'DC NewCases' : StateDataSet["District of Columbia"][1],
                            'MO Cases': StateDataSet["Missouri"][0],
                            'MO NewCases' : StateDataSet["Missouri"][1],
                            
                            'VISN10 VACases': VISN10_VACases,
                            'VISN12 VACases': VISN12_VACases,
                            'VISN20 VACases': VISN20_VACases,
                            
                            'OH VACases': StateDataSet["Ohio"][2],
                            'OH NewVACases' : StateDataSet["Ohio"][3],
                            'IN VACases': StateDataSet["Indiana"][2],
                            'IN NewVACases' : StateDataSet["Indiana"][3],
                            'MI VACases': StateDataSet["Michigan"][2],
                            'MI NewVACases' : StateDataSet["Michigan"][3],
                            
                            'IL VACases': StateDataSet["Illinois"][2],
                            'IL NewVACases' : StateDataSet["Illinois"][3],
                            'WI VACases': StateDataSet["Wisconsin"][2],
                            'WI NewVACases' : StateDataSet["Wisconsin"][3],
                            
                            'WA VACases': StateDataSet["Washington"][2],
                            'WA NewVACases' : StateDataSet["Washington"][3],
                            'OR VACases': StateDataSet["Oregon"][2],
                            'OR NewVACases' : StateDataSet["Oregon"][3],
                            'ID VACases': StateDataSet["Idaho"][2],
                            'ID NewVACases' : StateDataSet["Idaho"][3],
                            'AK VACases': StateDataSet["Alaska"][2],
                            'AK NewVACases': StateDataSet["Alaska"][3],

                            'MD VACases': StateDataSet["Maryland"][2],
                            'MD NewVACases' : StateDataSet["Maryland"][3],
                            'VA VACases': StateDataSet["Virginia"][2],
                            'VA NewVACases' : StateDataSet["Virginia"][3],
                            'DC VACases': StateDataSet["District of Columbia"][2],
                            'DC NewVACases' : StateDataSet["District of Columbia"][3],
                            'MO VACases': StateDataSet["Missouri"][2],
                            'MO NewVACases' : StateDataSet["Missouri"][3],
                            
                            #Anchorage (AN)
                            'AN TotalCases': DataSet["Anchorage VA Medical Center"][0],
                            'AN ECases': DataSet["Anchorage VA Medical Center"][1],
                            'AN NewECases': DataSet["Anchorage VA Medical Center"][2],
                            
                            #Portland (PO)
                            'PO TotalCases': DataSet["Portland VA Medical Center"][0],
                            'PO ECases': DataSet["Portland VA Medical Center"][1],
                            'PO NewECases': DataSet["Portland VA Medical Center"][2],
                          
                            #WCPAC (WC)
                            'WC TotalCases': DataSet["North Las Vegas VA Medical Center"][0],
                            'WC ECases': DataSet["North Las Vegas VA Medical Center"][1],
                            'WC NewECases': DataSet["North Las Vegas VA Medical Center"][2],
                      
                            #Walla Walla (WW)
                            'WW TotalCases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][0],
                            'WW ECases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][1],
                            'WW NewECases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][2],
                           
                            #White City (WH)
                            'WH TotalCases': DataSet["White City VA Medical Center"][0],
                            'WH ECases': DataSet["White City VA Medical Center"][1],
                            'WH NewECases': DataSet["White City VA Medical Center"][2],
                  
                            #Roseburg (RO)
                            'RO TotalCases': DataSet["Roseburg VA Medical Center"][0],
                            'RO ECases': DataSet["Roseburg VA Medical Center"][1],
                            'RO NewECases': DataSet["Roseburg VA Medical Center"][2],
                
                            #Puget Sound (PS)
                            'PS TotalCases': DataSet["Seattle VA Medical Center"][0],
                            'PS ECases': DataSet["Seattle VA Medical Center"][1],
                            'PS NewECases': DataSet["Seattle VA Medical Center"][2],
                
                            #Mann-Grandstaff (MG)
                            'MG TotalCases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][0],
                            'MG ECases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][1],
                            'MG NewECases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][2],
                  
                            #Boise (BO)
                            'BO TotalCases': DataSet["Boise VA Medical Center"][0],
                            'BO ECases': DataSet["Boise VA Medical Center"][1],
                            'BO NewECases': DataSet["Boise VA Medical Center"][2],
                      
                            #Jesse Brown (JE)
                            'JE TotalCases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][0],
                            'JE ECases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][1],
                            'JE NewECases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][2],
                          
                            #William S. Middleton Memorial (WM)
                            'WM TotalCases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][0],
                            'WM ECases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][1],
                            'WM NewECases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][2],
                           
                            #Clement J. Zablocki (CZ)
                            'CZ TotalCases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][0],
                            'CZ ECases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][1],
                            'CZ NewECases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][2],
                 
                            #Oscar G. Johnson (OJ)
                            'OJ TotalCases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][0],
                            'OJ ECases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][1],
                            'OJ NewECases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][2],
                
                            #Ann Arbor (AA)
                            'AA TotalCases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][0],
                            'AA ECases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][1],
                            'AA NewECases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][2],
                      
                            #Battle Creek (BC)
                            'BC TotalCases': DataSet["Battle Creek VA Medical Center"][0],
                            'BC ECases': DataSet["Battle Creek VA Medical Center"][1],
                            'BC NewECases': DataSet["Battle Creek VA Medical Center"][2],
                 
                            #Detroit (DE)
                            'DE TotalCases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][0],
                            'DE ECases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][1],
                            'DE NewECases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][2],
                            
                            #Saginaw (SA)
                            'SA TotalCases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][0], 
                            'SA ECases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][1], 
                            'SA NewECases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][2], 
                            
                            #Fort Wayne (FW)
                            'FW TotalCases' : DataSet["Fort Wayne VA Medical Center"][0], 
                            'FW ECases' : DataSet["Fort Wayne VA Medical Center"][1], 
                            'FW NewECases' : DataSet["Fort Wayne VA Medical Center"][2],

                            #Marion (MA)
                            'MA TotalCases' : DataSet["Marion VA Medical Center"][0], 
                            'MA ECases' : DataSet["Marion VA Medical Center"][1], 
                            'MA NewECases' : DataSet["Marion VA Medical Center"][2], 

                            #Indianapolis (IN)
                            'IN TotalCases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][0], 
                            'IN ECases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][1], 
                            'IN NewECases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][2],

                            #Chillicothe (CH)
                            'CH TotalCases' : DataSet["Chillicothe VA Medical Center"][0],
                            'CH ECases' : DataSet["Chillicothe VA Medical Center"][1],
                            'CH NewECases' : DataSet["Chillicothe VA Medical Center"][2],
                            
                            #Cincinnati (CN)
                            'CN TotalCases' : DataSet["Cincinnati VA Medical Center"][0],
                            'CN ECases' : DataSet["Cincinnati VA Medical Center"][1],
                            'CN NewECases' : DataSet["Cincinnati VA Medical Center"][2],

                            #Cleveland (CL)
                            'CL TotalCases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][0], 
                            'CL ECases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][1], 
                            'CL NewECases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][2],
                            
                            #Dayton (DA)
                            'DA TotalCases' : DataSet["Dayton VA Medical Center"][0],
                            'DA ECases' : DataSet["Dayton VA Medical Center"][1],
                            'DA NewECases' : DataSet["Dayton VA Medical Center"][2],
                            
                            #Danville (DN)
                            'DN TotalCases' : DataSet["Danville VA Medical Center"][0], 
                            'DN ECases' : DataSet["Danville VA Medical Center"][1], 
                            'DN NewECases' : DataSet["Danville VA Medical Center"][2], 
                            
                            #Hines (HN)
                            'HN TotalCases' : DataSet["Edward Hines Junior Hospital"][0], 
                            'HN ECases' : DataSet["Edward Hines Junior Hospital"][1], 
                            'HN NewECases' : DataSet["Edward Hines Junior Hospital"][2], 
                            
                            #North Chicago (NC)
                            'NC TotalCases' : DataSet["Captain James A. Lovell Federal Health Care Center"][0], 
                            'NC ECases' : DataSet["Captain James A. Lovell Federal Health Care Center"][1], 
                            'NC NewECases' : DataSet["Captain James A. Lovell Federal Health Care Center"][2], 
                            
                            #Tomah (TO)
                            'TO TotalCases' : DataSet["Tomah VA Medical Center"][0],
                            'TO ECases' : DataSet["Tomah VA Medical Center"][1],
                            'TO NewECases' : DataSet["Tomah VA Medical Center"][2],
                            
                            #Columbus (CO) (Hard-Coded)
                            'CO ECases' : DataSet["Columbus VA Medical Center"][0],
                            'CO NewECases' : DataSet["Columbus VA Medical Center"][1]}, index=[0])

    CCTVAChart = pd.concat([CCTVAChart_newrow, CCTVAChart]).reset_index(drop=True).drop_duplicates(subset='DATE',keep='first').round(2)
    CCTVAChart = CCTVAChart.set_index('DATE').T.reset_index()
    CCTVAChart.to_csv('CCTVAChart2.csv',index=False)