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
        NewECases = ECases - FacilityData['VET_YESTER'].sum()
        TotalSumCases = FacilityData['CASES'].sum()
        NewSumCases = TotalSumCases - FacilityData['YESTER_CASES'].sum()
        values = [TotalSumCases,NewSumCases, ECases, NewECases]
        DataSet['%s' %vamc] = values
        # print(TotalSumCases)

    #Hard-coding for Columbus
    COFacilityList = ['39159','39097', '39129','39049','39045','39089','39041','39117'] 
    COFacilityData = CountyVACOVID[CountyVACOVID['FIPS'].isin(COFacilityList)]

    COTotalSumCases = FacilityData['CASES'].sum()
    CONewSumCases = COTotalSumCases - FacilityData['YESTER_CASES'].sum()
    COECases = COFacilityData['VET_CASES'].sum()
    CONewCases = COECases - COFacilityData['VET_YESTER'].sum()

    COValues = [COTotalSumCases,CONewSumCases,COECases, CONewCases]
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
                            'Anchorage VAMC TotalSumCases': DataSet["Anchorage VA Medical Center"][0],
                            'Anchorage VAMC NewSumCases': DataSet["Anchorage VA Medical Center"][1],
                            'Anchorage VAMC ECases': DataSet["Anchorage VA Medical Center"][2],
                            'Anchorage VAMC NewECases': DataSet["Anchorage VA Medical Center"][3],
                            
                            #Portland (PO)
                            'Portland VAMC TotalSumCases': DataSet["Portland VA Medical Center"][0],
                            'Portland VAMC NewSumCases': DataSet["Portland VA Medical Center"][1],
                            'Portland VAMC ECases': DataSet["Portland VA Medical Center"][2],
                            'Portland VAMC NewECases': DataSet["Portland VA Medical Center"][3],
                          
                            #WCPAC (WC)
                            'Las Vegas VAMC TotalSumCases': DataSet["North Las Vegas VA Medical Center"][0],
                            'Las Vegas VAMC NewSumCases': DataSet["North Las Vegas VA Medical Center"][1],
                            'Las Vegas VAMC ECases': DataSet["North Las Vegas VA Medical Center"][2],
                            'Las Vegas VAMC NewECases': DataSet["North Las Vegas VA Medical Center"][3],
                      
                            #Walla Walla (WW)
                            'Jonathan M. VAMC TotalSumCases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][0],
                            'Jonathan M. VAMC NewSumCases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][1],
                            'Jonathan M. VAMC ECases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][2],
                            'Jonathan M. VAMC NewECases': DataSet["Jonathan M. Wainwright Memorial VA Medical Center"][3],


                            #White City
                            'White City VAMC TotalSumCases': DataSet["White City VA Medical Center"][0],
                            'White City VAMC NewSumCases': DataSet["White City VA Medical Center"][1],
                            'White City VAMC ECases': DataSet["White City VA Medical Center"][2],
                            'White City VAMC NewECases': DataSet["White City VA Medical Center"][3],
                  
                            #Roseburg (RO)
                            'Roseburg  VAMC TotalSumCases': DataSet["Roseburg VA Medical Center"][0],
                            'Roseburg VAMC NewSumCases': DataSet["Roseburg VA Medical Center"][1],
                            'Roseburg VAMC ECases': DataSet["Roseburg VA Medical Center"][2],
                            'Roseburg VAMC NewECases': DataSet["Roseburg VA Medical Center"][3],
                
                            #Puget Sound (PS)
                            'Seattle VAMC TotalSumCases': DataSet["Seattle VA Medical Center"][0],
                            'Seattle VAMC NewSumCases': DataSet["Seattle VA Medical Center"][1],
                            'Seattle VAMC ECases': DataSet["Seattle VA Medical Center"][2],
                            'Seattle VAMC NewECases': DataSet["Seattle VA Medical Center"][3],
                
                            #Mann-Grandstaff (MG)
                            'Mann-Grandstaff VAMC TotalSumCases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][0],
                            'Mann-Grandstaff VAMC NewSumCases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][1],
                            'Mann-Grandstaff VAMC ECases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][2],
                            'Mann-Grandstaff VAMC NewECases': DataSet["Mann-Grandstaff Department of Veterans Affairs Medical Center"][3],
                  
                            #Boise (BO)
                            'Boise VAMC TotalSumCases': DataSet["Boise VA Medical Center"][0],
                            'Boise VAMC NewSumCases': DataSet["Boise VA Medical Center"][1],
                            'Boise VAMC ECases': DataSet["Boise VA Medical Center"][2],
                            'Boise VAMC NewECases': DataSet["Boise VA Medical Center"][3],
                      
                            #Jesse Brown (JE)
                            'Jesse Brown VAMC TotalSumCases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][0],
                            'Jesse Brown VAMC NewSumCases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][1],
                            'Jesse Brown VAMC ECases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][2],
                            'Jesse Brown VAMC NewECases': DataSet["Jesse Brown Department of Veterans Affairs Medical Center"][3],
                          
                            #William S. Middleton Memorial (WM)
                            'William S. VAMC TotalSumCases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][0],
                            'William S. VAMC NewSumCases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][1],
                            'William S. VAMC ECases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][2],
                            'William S. VAMC NewECases': DataSet['William S. Middleton Memorial Veterans\' Hospital'][3],
                           
                            #Clement J. Zablocki (CZ)
                            'Clement J. VAMC TotalSumCases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][0],
                            'Clement J. VAMC NewSumCases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][1],
                            'Clement J. VAMC ECases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][2],
                            'Clement J. VAMC NewECases': DataSet['Clement J. Zablocki Veterans\' Administration Medical Center'][3],
                 
                            #Oscar G. Johnson (OJ)
                            'Oscar G. VAMC TotalSumCases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][0],
                            'Oscar G. VAMC NewSumCases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][1],
                            'Oscar G. VAMC ECases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][2],
                            'Oscar G. VAMC NewECases': DataSet["Oscar G. Johnson Department of Veterans Affairs Medical Facility"][3],
                
                            #Ann Arbor (AA)
                            'Lieutenant Colonel Charles S. VAMC TotalSumCases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][0],
                            'Lieutenant Colonel Charles S. VAMC NewSumCases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][1],
                            'Lieutenant Colonel Charles S. VAMC ECases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][2],
                            'Lieutenant Colonel Charles S. VAMC NewECases': DataSet["Lieutenant Colonel Charles S. Kettles VA Medical Center"][3],
                      
                            #Battle Creek (BC)
                            'Battle Creek VAMC TotalSumCases': DataSet["Battle Creek VA Medical Center"][0],
                            'Battle Creek VAMC NewSumCases': DataSet["Battle Creek VA Medical Center"][1],
                            'Battle Creek VAMC ECases': DataSet["Battle Creek VA Medical Center"][2],
                            'Battle Creek VAMC NewECases': DataSet["Battle Creek VA Medical Center"][3],
                 
                            #Detroit (DE)
                            'John D. Dingell VAMC TotalSumCases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][0],
                            'John D. Dingell VAMC NewSumCases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][1],
                            'John D. Dingell VAMC ECases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][2],
                            'John D. Dingell VAMC NewECases': DataSet["John D. Dingell Department of Veterans Affairs Medical Center"][3],
                            
                            #Saginaw (SA)
                            'Aleda E. VAMC TotalSumCases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][0], 
                            'Aleda E. VAMC NewSumCases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][1], 
                            'Aleda E. VAMC ECases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][2], 
                            'Aleda E. VAMC NewECases' : DataSet["Aleda E. Lutz Department of Veterans Affairs Medical Center"][3], 
                            
                            #Fort Wayne (FW)
                            'Fort Wayne VAMC TotalSumCases' : DataSet["Fort Wayne VA Medical Center"][0], 
                            'Fort Wayne VAMC NewSumCases' : DataSet["Fort Wayne VA Medical Center"][1], 
                            'Fort Wayne VAMC ECases' : DataSet["Fort Wayne VA Medical Center"][2], 
                            'Fort Wayne VAMC NewECases' : DataSet["Fort Wayne VA Medical Center"][3],

                            #Marion (MA)
                            'Marion VAMC TotalSumCases' : DataSet["Marion VA Medical Center"][0], 
                            'Marion VAMC NewSumCases' : DataSet["Marion VA Medical Center"][1], 
                            'Marion VAMC ECases' : DataSet["Marion VA Medical Center"][2], 
                            'Marion VAMC NewECases' : DataSet["Marion VA Medical Center"][3], 

                            #Indianapolis (IN)
                            'Richard L. VAMC TotalSumCases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][0], 
                            'Richard L. VAMC NewSumCases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][1], 
                            'Richard L. VAMC ECases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][2], 
                            'Richard L. VAMC NewECases' : DataSet["Richard L. Roudebush Veterans\' Administration Medical Center"][3],

                            #Chillicothe (CH)
                            'Chillicothe VAMC TotalSumCases' : DataSet["Chillicothe VA Medical Center"][0],
                            'Chillicothe VAMC NewSumCases' : DataSet["Chillicothe VA Medical Center"][1],
                            'Chillicothe VAMC ECases' : DataSet["Chillicothe VA Medical Center"][2],
                            'Chillicothe VAMC NewECases' : DataSet["Chillicothe VA Medical Center"][3],
                            
                            #Cincinnati (CN)
                            'Cincinnati VAMC TotalSumCases' : DataSet["Cincinnati VA Medical Center"][0],
                            'Cincinnati VAMC NewSumCases' : DataSet["Cincinnati VA Medical Center"][1],
                            'Cincinnati VAMC ECases' : DataSet["Cincinnati VA Medical Center"][2],
                            'Cincinnati VAMC NewECases' : DataSet["Cincinnati VA Medical Center"][3],

                            #Cleveland (CL)
                            'Louis Stokes VAMC TotalSumCases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][0], 
                            'Louis Stokes VAMC NewSumCases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][1], 
                            'Louis Stokes VAMC ECases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][2], 
                            'Louis Stokes VAMC NewECases' : DataSet["Louis Stokes Cleveland Department of Veterans Affairs Medical Center"][3],
                            
                            #Dayton (DA)
                            'Dayton VAMC TotalSumCases' : DataSet["Dayton VA Medical Center"][0],
                            'Dayton VAMC NewSumCases' : DataSet["Dayton VA Medical Center"][1],
                            'Dayton VAMC ECases' : DataSet["Dayton VA Medical Center"][2],
                            'Dayton VAMC NewECases' : DataSet["Dayton VA Medical Center"][3],
                            
                            #Danville (DN)
                            'Danville VAMC TotalSumCases' : DataSet["Danville VA Medical Center"][0], 
                            'Danville VAMC NewSumCases' : DataSet["Danville VA Medical Center"][1], 
                            'Danville VAMC ECases' : DataSet["Danville VA Medical Center"][2], 
                            'Danville VAMC NewECases' : DataSet["Danville VA Medical Center"][3], 
                            
                            #Hines (HN)
                            'Edward Hines VAMC TotalSumCases' : DataSet["Edward Hines Junior Hospital"][0], 
                            'Edward Hines VAMC NewSumCases' : DataSet["Edward Hines Junior Hospital"][1], 
                            'Edward Hines VAMC ECases' : DataSet["Edward Hines Junior Hospital"][2], 
                            'Edward Hines VAMC NewECases' : DataSet["Edward Hines Junior Hospital"][3], 
                            
                            #North Chicago (NC)
                            'Captain James A. VAMC TotalSumCases' : DataSet["Captain James A. Lovell Federal Health Care Center"][0], 
                            'Captain James A. VAMC NewSumCases' : DataSet["Captain James A. Lovell Federal Health Care Center"][1], 
                            'Captain James A. VAMC ECases' : DataSet["Captain James A. Lovell Federal Health Care Center"][2], 
                            'Captain James A. VAMC NewECases' : DataSet["Captain James A. Lovell Federal Health Care Center"][3], 
                            
                            #Tomah (TO)
                            'Tomah VAMC TotalSumCases' : DataSet["Tomah VA Medical Center"][0],
                            'Tomah VAMC NewSumCases' : DataSet["Tomah VA Medical Center"][1],
                            'Tomah VAMC ECases' : DataSet["Tomah VA Medical Center"][2],
                            'Tomah VAMC NewECases' : DataSet["Tomah VA Medical Center"][3],
                            
                            #Columbus (CO) (Hard-Coded)

                            'Columbus VAMC TotalSumCases' : DataSet["Columbus VA Medical Center"][0],
                            'Columbus VAMC NewSumCases' : DataSet["Columbus VA Medical Center"][1],
                            'Columbus VAMC ECases' : DataSet["Columbus VA Medical Center"][2],
                            'Columbus VAMC NewECases' : DataSet["Columbus VA Medical Center"][3]}, index=[0])

    CCTVAChart = pd.concat([CCTVAChart_newrow, CCTVAChart]).reset_index(drop=True).drop_duplicates(subset='DATE',keep='first').round(2)
    CCTVAChart = CCTVAChart.set_index('DATE').T.reset_index()
    CCTVAChart.to_csv('CCTVAChart2.csv',index=False)
