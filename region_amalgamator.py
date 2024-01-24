import pandas as pd
import os

airport_folder ='airport_csvs'
region_folder = 'region_csvs'
output_folder = 'output_folder'

def region_amalgamator(airport_filename,region_filename,output_filename):
    airport_filepath = os.path.join(airport_folder,airport_filename)
    region_filepath = os.path.join(region_folder,region_filename)
    output_filepath = os.path.join(output_folder,output_filename)
    airport_df = pd.read_csv(airport_filepath)
    region_df = pd.read_csv(region_filepath)


if __name__=="__main__":
    region_amalgamator("Australia Airports.csv","Australia LGAs.csv","Australia Airports.csv")
