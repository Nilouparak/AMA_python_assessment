
import numpy as np
import pandas as pd
import datetime
from dateutil.rrule import rrule, MONTHLY
import pdb

#Assignment 1

def clean_number(text):
    """
    Assignment 1 - Question 1
    """
    assert isinstance(text,str), "Input must be string"
    text = text.strip()
    try:
        if '.' in text:
            if '.0' in text:
                return int(float(text))
            else:
                return float(text)
        else:
            return int(text)
    except:
        return np.nan


def find_min_of_diff(df, col1, col2, col_metric, diff_column_name, diff_column_unit):
    """
    Assignment 1 - Question 4
    :param df: dataset
    :param col1: First column in column difference calculation
    :param col2: Second column in column difference calculation
    :param col_metric: We calculate the difference of col2 and col2 values based on this parameter
    :param diff_column_name: Name of the difference column
    :param diff_column_unit: Unit measure for difference column
    :return: NA - function adds the column to df and prints the results
    """
    for col in [col1, col2]:
        df[col] = df[col].apply(clean_number)
    df[diff_column_name] = df[col1] - df[col2]
    min_diff = min(df[diff_column_name])
    print(f'Minimum {diff_column_name} is {min_diff} {diff_column_unit}s.')
    metric_with_min_diff = df[col_metric].loc[df[diff_column_name] == min_diff].values[0]
    print(f'{col_metric} {metric_with_min_diff} has minimum {diff_column_name} of {min_diff} {diff_column_unit}s.')
    return


def answer_question_2():
    """
    Assignment 1 - Question 2

    """

    def read_clean_weather_data(url):
        w = pd.read_csv(url, header=None)
        w.columns = ["000"]
        # w["000"]=w["000"].str.replace(" ","#")
        w["000"] = w["000"].astype(str).str.replace("              ", " None None ").\
                                        str.replace("          5.3", " None None ").\
                                        str.replace("          "," None ").\
                                        str.replace("         "," None ").\
                                        str.replace("       0.00"," None 0.00")

        w["000"] = w["000"].str.replace("    "," ").str.replace("   "," ").str.replace("  "," ")
        assert "  " not in w["000"], "Table not ready: white spaces not properly eliminated."
        new_columns = w.iloc[0].str.split()[0]
        w[new_columns] = w["000"].str.split(expand=True)
        w = w.reset_index(drop=True).drop("000",axis=1)
        assert all(w.columns == list(w.iloc[0])), "Column names do not match the data frame."
        w = w.iloc[1: , :]
        w = w.rename(columns={'Dy': 'Day'})
        return w
    w_df = read_clean_weather_data('https://github.com/AMADataLabs/Python-Assessment/blob/main/Assignment%201/weather.csv?raw=True')
    find_min_of_diff(w_df, 'MxT', 'MnT', 'Day', 'temp_spread', 'degree')
    return


def answer_question_3():
    """
       Assignment 1 - Question 3

    """
    url = "https://github.com/AMADataLabs/Python-Assessment/blob/main/Assignment%201/football.csv?raw=true"
    f_df = pd.read_csv(url)
    find_min_of_diff(f_df, 'F', 'A', 'Team', 'for_against_difference', 'goal')
    return


#Assignment 2

def months_interval(start_date,end_date):
    """
    Assignment 2

    :param start_date: First date
    :param end_date: Second date
    :return: months names in between first and second date (inclusive)

    """

    assert isinstance(start_date, str), "Start date must be a string."
    assert isinstance(end_date, str), "End date must be a string."
    st_year, sd_month, sd_day = start_date.split(",")
    ed_year, ed_month, ed_day = end_date.split(",")
    strt_dt = datetime.date(int(st_year), int(sd_month), int(sd_day))
    end_dt = datetime.date(int(ed_year), int(ed_month), int(ed_day))
    month_names_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                        6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
                        12: 'December'}
    month_numbers = [dt.month for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
    month_names = [value for key, value in month_names_dict.items() if key in month_numbers]
    print(month_names)
    return month_names


if __name__ == "__main__":
    clean_number(' 30.0  ')
    answer_question_2()
    answer_question_3()
    months_interval('2017, 1, 1', '2017, 3, 1')
