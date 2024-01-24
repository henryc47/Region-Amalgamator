import pandas as pd
import os
import math

airport_folder ='airport_csvs'
region_folder = 'region_csvs'
output_folder = 'output_folder'

def region_amalgamator(airport_filename,region_filename,output_filename):
    airport_filepath = os.path.join(airport_folder,airport_filename)
    region_filepath = os.path.join(region_folder,region_filename)
    output_filepath = os.path.join(output_folder,output_filename)
    airports_df = pd.read_csv(airport_filepath)
    airports_df = airports_df.fillna('')
    regions_df = pd.read_csv(region_filepath)
    regions_df = regions_df.fillna('')
    airport_names,airport_name_indices_dict = get_airport_unique_names(airports_df)
    airports_df["Population from Regions"] = 0.0
    airports_df["GDP from Regions"] = 0.0
    regions_df = regions_df.apply(calculate_GDP,axis=1)
    airports_df = amalgamate_regions(airports_df,regions_df,airport_name_indices_dict)
    


def amalgamate_regions(airports_df,regions_df,airport_name_indices_dict):
    num_regions = len(regions_df)
    for i in range(num_regions): #very inefficient computer timewise, but this will not be our performance bottleneck and will be easier to write and understand
        airports = regions_df.iloc[i]["Airports"]
        states = regions_df.iloc[i]["States"]
        countries = regions_df.iloc[i]["Countries"]
        fractions_raw = regions_df.iloc[i]["Fractions"]
        population = regions_df.iloc[i]["Population"]
        gdp = regions_df.iloc[i]["GDP"]
        airports = str(airports).split(',')
        states = str(states).split(',')
        countries = str(countries).split(',')
        fractions_raw = str(fractions_raw).split(',')
        fractions = [float(x) for x in fractions_raw]
        sums_to_one = math.isclose(sum(fractions),1) #we must use approximate values as we are dealing with floats
        if not sums_to_one:
            print('fractions for region ',regions_df.iloc[i]["Name"]," = ",fractions," do not sum to 1")
        num_airports = len(airports)
        if len(states)==1:
            states = states*num_airports
        if len(countries)==1:
            countries = countries*num_airports
        if len(fractions)!=num_airports:
            print("for region ",regions_df.iloc[i]["Name"]," num fractions ",fractions," not equal to num airports = ",num_airports)
            continue
        for j in range(num_airports):
            if airports[j]=='':
                continue
            unique_name = (airports[j],states[j],countries[j])

            if unique_name in airport_name_indices_dict:
                airport_index = airport_name_indices_dict[unique_name]
                fraction = fractions[j]
                population_from_fraction = population*fraction
                gdp__from_fraction = gdp*fraction
                airports_df.at[airport_index,"Population from Regions"] = airports_df.iloc[airport_index]["Population from Regions"] + population_from_fraction
                airports_df.at[airport_index,"GDP from Regions"] = airports_df.iloc[airport_index]["GDP from Regions"] + gdp__from_fraction
            else:
                print(unique_name," not found in dictionary of airports")
                print("region is ",regions_df.iloc[i]["Name"])
            
    return airports_df



def calculate_GDP(df):
    df["GDP"] = df["Population"]*df["GDP/head"]
    return df

def get_airport_unique_names(df):
    num_airports = len(df)
    unique_names = []
    airport_name_indices_dict = {}
    for i in range(num_airports):
        name : str = convert_object_to_str(df.loc[i,"Name"])
        state : str = convert_object_to_str(df.loc[i,"State"])
        country : str = convert_object_to_str(df.loc[i,"Country"])
        unique_name : tuple[str,str,str] = (name,state,country)
        unique_names.append(unique_name)
        airport_name_indices_dict[unique_name] = i

    return unique_names,airport_name_indices_dict

#convert pandas object to string
def convert_object_to_str(object) -> str:
    if pd.isnull(object):
         output : str = ""
    else:
        output : str = str(object)
    
    return output


if __name__=="__main__":
    region_amalgamator("Australia Airports.csv","Australia LGAs.csv","Australia Airports.csv")
