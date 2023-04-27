from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from csv import reader
import sys
import haversine as hs
import pandas as pd
import io
df_zip = pd.read_csv('zip_lat_long.csv')
df=df_zip.set_index('ZIP')
# settings (old version)
FILE_TO_PARSE = 'fuzzydist_TZ_419.csv'
OUTPUT = 'fuzzydistoutput_TZ_419.csv'
FIELD_OF_INTEREST = 8 # set it to 8 for district, 0 for business name
GLOBAL_FLAG = True # set to true if a global region (TZ, GL)
#########
try:
    # get the input parameters from the command line
    FILE_TO_PARSE = sys.argv[1]
    OUTPUT = sys.argv[2]
    FIELD_OF_INTEREST = int(sys.argv[3])
    GLOBAL_FLAG = bool(sys.argv[4])
except:
    print('failed to get successful parameters')
    pass

if FIELD_OF_INTEREST != 8:
    CMP_PT = 'BUSINESS/SCHOOL NAME'
else:
    CMP_PT = 'DISTRICT'
dict_tuple = {}
#print(df.head())
print('Generating Distance Matrix')
counter = 1
print(len(df.index))
potential_duplicate = []
dict_of_pk = {} #primary key with maximum tracker key! (most recent)
#print((df.loc[zipJ]['LAT'],df.loc[zipJ]['LONG']))
def fileParser():
    fileO = open(FILE_TO_PARSE,'r',encoding='utf-8')
    #text file should have name as col 1, category as col 2, pk as col 3, ZIP as col 4, event key as col 5, tk as col 6, PARTICIPANT_count as col 7, address 8/9, district 10
    text = fileO.read().split('\n')
    print(text[1:8])
    fileO.close()
    category_dict = {'faithbased':[],'schools':['district','school','union'],'healthcare':['care','healthcare','hospital','hc','Center'],'colleges':['university'],'federal':[],'state':[],'local':[],'businesses':[],'preparedness':[],'':[]}
    for h in category_dict.keys():
        #filter text file to just those in one category
        #potential_duplicate = []
        file_reader=[]
        print(h)
        for line in reader(text):
            #print(line)
            try:
                #print(line.split(',')[1].strip('\n'))
                #print('test')
                if line[1].strip('\n""')==h and (line[2] not in dict_of_pk.keys() or (line[2] in dict_of_pk.keys() and line[5] >= dict_of_pk[line[2]])):# and int(line[10]) == 1: # specifically most recent
                    dict_of_pk[line[2]] = line[5]
                    business_stripped = line[0].lower()
                    for i in category_dict[h]:
                        business_stripped = business_stripped.replace(i,'')
                    district_stripped = line[9].lower().replace('district','').replace('school','').replace('unified','') # remove commonly used words
                    for item in category_dict[h]:
                        district_stripped = district_stripped.replace(item,'') # remove commonly used words for district
                    #abbreviation =''.join([w[0] for w in line[9].lower().split()])
                    file_reader.append([business_stripped,line[2],line[3],line[4],line[5], line[6].strip('\n""'),line[7],line[8],district_stripped,len(line[9]),line[9]])
            except:
                print('fail')
                pass
        print(len(file_reader))
        parsed=[]
        counter=1
        #tuplize
        for index,val in df.iterrows():
            dict_tuple[index]=(df.loc[index]['LAT'],df.loc[index]['LNG']) # get lat long of zipcode
        #print(list(dict_tuple.values())[0:7])
        print('on the fly tuplefication done')
        fileReader(file_reader,FIELD_OF_INTEREST) 
#FileReader - given a list of businesseses, and a field to look at, return records that are closely related.
def fileReader(file_reader,field_of_interest=0): #gets records that are closely related
    parsed=[]
    counter = 1
    for i in file_reader:
        print(i[0])
        counter+=1
        counterJ = 0
        #get distances between two businesses
        try:
            zipI = int(i[2])
        except:
            zipI = 10021
        try:
            tupleI = dict_tuple[zipI]
        except:
            tupleI=(0,0)
        for j in file_reader:
            counterJ+=1
            try:
                zipJ = int(j[2])
            except:
                zipJ = 10021
            try:
                ratio=float(i[5])/float(j[5])
            except:
                ratio = 0
            if counterJ > counter:
                pass
            #print(distance_matrix[df['zip1']==zipi & df['zip1']==zipj]['DIST'][0])
            if 1 == 1:
                #tupleJ = dict_tuple[zipJ]
                try:
                    tupleJ = dict_tuple[zipJ]
                    #print(tupleJ)
                except:
                    #print('not found')
                    tupleJ = (0,0)
                #print(tupleJ)
                #print(category_dict[h])
                if i[1]!=j[1] and (field_of_interest != 0 or (ratio > .66 and ratio < 1.5)) and (field_of_interest != 8 or (i[9] != 0 and j[9] != 0)): # similar participant count and same region (before doing expensive fuzzy search)
                    #print('partial match found pre ratio')
            #print(i,j)]
                    if i[8] == j[8]:
                        continue # if districts are exactly the same, then you 
                    if ((fuzz.partial_ratio(i[field_of_interest],j[field_of_interest]) > 90 or fuzz.token_sort_ratio(i[field_of_interest],j[field_of_interest]) > 80)and i!=j):
                        #print(hs.haversine(tupleI,tupleJ))
                        distance = hs.haversine(tupleI,tupleJ)
                        if (distance < 20 or (tupleJ == (0,0) or tupleI== (0,0)) or GLOBAL_FLAG == True): # and i[-1] == j[-1]:
                            if distance == 0 and (tupleJ == (0,0) or tupleI== (0,0)):
                                distance = 'error'
                            #print('partial match found')
                            list_build = []
                            list_build.extend([str(i[range_1]) for range_1 in range(0,8)])
                            list_build.extend([str(j[range_1]) for range_1 in range(0,8)])
                            list_build.extend([i[field_of_interest],j[field_of_interest],fuzz.partial_ratio(i[field_of_interest],j[field_of_interest]),ratio,distance])
                            potential_duplicate.append(list_build)
                            #print('t')
            '''except:
                continue'''
        parsed.append(i)
    return parsed
#print(len(potential_duplicate))
fileParser()
fileOutput = io.open(OUTPUT,'w',encoding='utf8')
retStr="Data\n"
retStr+=CMP_PT+',Primary Key,Zip Code,Event Key,Tracker Key,Number of people,Address,RELATED:,'+CMP_PT+',Primary Key,Zip Code,Event Key,Tracker Key,Number of people,Address,'+CMP_PT+':,'+CMP_PT+',Related '+CMP_PT+',% Match, Ratio,Distance\n'

for i in potential_duplicate:
    #print('test')
    retStr+=','.join([str(item).replace(",","") for item in i])+'\n'
fileOutput.write(retStr)
fileOutput.close()
