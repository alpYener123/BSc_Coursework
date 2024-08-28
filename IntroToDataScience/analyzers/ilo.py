# External imports
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

# Local imports
from utils.config import config


def inflowGraph(df: pd.DataFrame):
    df = df.drop("indicator.label", axis=1)
    total_df: pd.DataFrame = df[df["sex.label"] == "Sex: Total"]

    df_sum = total_df.groupby('classif1.label')[
        'obs_value'].sum().reset_index()
    top_labels = df_sum.nlargest(6, 'obs_value')['classif1.label']
    df_top = total_df[total_df['classif1.label'].isin(top_labels)]

    fig, ax = plt.subplots(figsize=(10, 6))
    for label, group in df_top.groupby("classif1.label"):
        label = label.replace("Country of citizenship: ", "")

        # Sort the group by time values
        group = group.sort_values("time")

        ax.plot(group["time"], group["obs_value"], label=label)

    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Migration by thousands')
    ax.set_title('Migration of Working Age Citizens Over Time')

    # Add a legend
    ax.legend()

    # Save the plot as a file (e.g., PNG format)
    plt.savefig(config.GRAPH_DIR / "Inflow.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


def classif2Line(df: pd.DataFrame):

    # drop the unnecessary columns
    df = df.drop(["indicator.label", "ref_area.label", "source.label", "obs_status.label",
                 "note_classif.label", "note_indicator.label", "note_source.label"], axis=1)

    # modify the dataframe to reduce the rows of each year
    total_df: pd.DataFrame = df[df["classif2.label"]
                                != "Place of birth: Total"]
    total_df = total_df[total_df["classif2.label"]
                        != "Place of birth: Status unknown"]
    total_df = total_df[total_df["classif1.label"]
                        == "Education (Aggregate levels): Total"]
    total_df = total_df[total_df["sex.label"] == "Sex: Total"]

    # drop the columns after being used for modification
    total_df = total_df.drop(["classif1.label", "sex.label"], axis=1)

    return total_df


def outsideOfWorkGraph(df: pd.DataFrame):

    # seperate df's since the values have a great difference
    df_native: pd.DataFrame = df[df['classif2.label']
                                 == 'Place of birth: Native-born']
    df_foreign: pd.DataFrame = df[df['classif2.label']
                                  == 'Place of birth: Foreign-born']

    # FOREIGNER'S PART
    df_sorted_f = df_foreign.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_f = df_sorted_f.reset_index(drop=True)

    plt.plot(df_sorted_f['time'], df_sorted_f['obs_value'])

    # calculate the linear regression,
    # the slope will give us approximately how much increase there is
    coefficients = np.polyfit(df_sorted_f['time'], df_sorted_f['obs_value'], 1)
    slopeF = coefficients[0]
    print("\nSlope of the regression for outside-of-work-force foreigners: ", slopeF)

    plt.xlabel('Years')
    plt.ylabel('Foreigners (in thousands)')
    plt.title('Foreigners outside of labour force by years')

    # Save the plot
    plt.savefig(config.GRAPH_DIR / "OutOfWorkForceForeigners.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()

    # NATIVE'S PART
    df_sorted_n = df_native.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_n = df_sorted_n.reset_index(drop=True)

    plt.plot(df_sorted_n['time'], df_sorted_n['obs_value'])

    plt.xlabel('Years')
    plt.ylabel('Natives (in thousands)')
    plt.title('Natives outside of labour force by years')

    # Save the plot
    plt.savefig(config.GRAPH_DIR / "OutOfWorkForceNatives.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


# basically does the same as the previous function, but for a different purpose
def unemployment(df: pd.DataFrame):

    # seperate df's since the values have a great difference
    df_native: pd.DataFrame = df[df['classif2.label']
                                 == 'Place of birth: Native-born']
    df_foreign: pd.DataFrame = df[df['classif2.label']
                                  == 'Place of birth: Foreign-born']

    # FOREIGNER'S PART
    df_sorted_f = df_foreign.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_f = df_sorted_f.reset_index(drop=True)

    plt.plot(df_sorted_f['time'], df_sorted_f['obs_value'])

    # calculate the linear regression,
    # the slope will give us approximately how much increase there is
    coefficients = np.polyfit(df_sorted_f['time'], df_sorted_f['obs_value'], 1)
    slopeF = coefficients[0]
    print("Slope of the regression for unemployed foreigners: ", slopeF, "\n")

    plt.xlabel('Years')
    plt.ylabel('Foreigners (in thousands)')
    plt.title('Unemployed foreigners by years')

    # Save the plot
    plt.savefig(config.GRAPH_DIR / "UnemployedForeigners.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()

    # NATIVE'S PART
    df_sorted_n = df_native.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_n = df_sorted_n.reset_index(drop=True)

    plt.plot(df_sorted_n['time'], df_sorted_n['obs_value'])

    plt.xlabel('Years')
    plt.ylabel('Natives (in thousands)')
    plt.title('Unemployed natives by years')

    # Save the plot
    plt.savefig(config.GRAPH_DIR / "UnemployedNatives.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


def unemployment_heat_education(df: pd.DataFrame):

    # drop the unnecessary columns
    total_df: pd.DataFrame = df.drop([
        "indicator.label", "ref_area.label", "source.label", "obs_status.label",
        "note_classif.label", "note_indicator.label", "note_source.label"], axis=1)

    total_df = df[df["classif2.label"]
                  == "Place of birth: Foreign-born"]
    total_df = total_df[total_df["classif2.label"]
                        != "Place of birth: Status unknown"]

    total_df = total_df[total_df["classif1.label"]
                        != "Education (Aggregate levels): Total"]
    total_df = total_df[total_df["sex.label"] == "Sex: Total"]

    # drop the columns after being used for modification
    total_df = total_df.drop(["sex.label", "classif2.label"], axis=1)

    # modify the colummns in a more presentable way
    total_df['classif1.label'] = total_df['classif1.label'].replace(
        'Education (Aggregate levels): Advanced', 'Advanced')
    total_df['classif1.label'] = total_df['classif1.label'].replace(
        'Education (Aggregate levels): Intermediate', 'Intermediate')
    total_df['classif1.label'] = total_df['classif1.label'].replace(
        'Education (Aggregate levels): Basic', 'Basic')
    total_df['classif1.label'] = total_df['classif1.label'].replace(
        'Education (Aggregate levels): Less than basic', 'Less than basic')

    pivot_table = total_df.pivot_table(
        index='classif1.label', columns='time', values='obs_value')
    pivot_table = pivot_table.reindex(
        ["Advanced", "Intermediate", "Basic", "Less than basic"])

    # Create the heatmap using seaborn
    sns.heatmap(pivot_table, annot=True, cmap='YlGnBu')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Foreigners (thousands)')
    plt.title('Unemployment of foreigners by education')

    # Save the plot
    plt.savefig(config.GRAPH_DIR / "UnemployedForeignersHeatmap.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


def foreigner_occupation(df: pd.DataFrame):
    total_df: pd.DataFrame = df.drop([
        "indicator.label", "ref_area.label", "source.label",
        "obs_status.label", "note_classif.label", "note_indicator.label",
        "note_source.label"], axis=1)

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (Skill level): Not elsewhere classified"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (Skill level): Total"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (Skill level): Total"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (ISCO-08): Total"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (Skill level): Skill level 1 ~ low"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (Skill level): Skill levels 3 and 4 ~ high"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (Skill level): Skill level 2 ~ medium"]

    total_df = total_df[total_df["classif1.label"]
                        != "Occupation (ISCO-08): X. Not elsewhere classified"]

    occupation_data = total_df.groupby(['classif1.label', 'sex.label'])[
        'obs_value'].sum().unstack().reset_index()

    occupation_data['classif1.label'] = occupation_data['classif1.label'].replace({
        'Occupation (ISCO-08): 1. Managers': 'Managers',
        'Occupation (ISCO-08): 2. Professionals': 'Professionals',
        'Occupation (ISCO-08): 3. Technicians and associate professionals': 'Technicians',
        'Occupation (ISCO-08): 4. Clerical support workers': 'Clerical Support Workers',
        'Occupation (ISCO-08): 5. Service and sales workers': 'Service and Sales Workers',
        'Occupation (ISCO-08): 6. Skilled agricultural, forestry and fishery workers':
        'Agricultural, Forestry and Fishery',
        'Occupation (ISCO-08): 7. Craft and related trades workers':
        'Craft and Related Trades Workers',
        'Occupation (ISCO-08): 8. Plant and machine operators, and assemblers':
        'Plant and Machine Operators',
        'Occupation (ISCO-08): 9. Elementary occupations': 'Elementary Occupations',
        'Occupation (ISCO-08): 0. Armed forces occupations': 'Armed Forces'
    })

    occupation_data['Sex: Total'] = occupation_data['Sex: Female'] + \
        occupation_data['Sex: Male']
    plt.figure(figsize=(40, 30))
    bar_width = 0.25
    index = range(len(occupation_data))

    plt.bar(index, occupation_data['Sex: Female'], bar_width, label='Female')
    plt.bar([i + bar_width for i in index],
            occupation_data['Sex: Male'], bar_width, label='Male')
    plt.bar([i + 2 * bar_width for i in index],
            occupation_data['Sex: Total'], bar_width, label='Total')

    max_value = int(
        occupation_data[['Sex: Female', 'Sex: Male', 'Sex: Total']].max().max())
    step_size = max_value // 10  # Adjust the number of intervals as needed
    plt.yticks(range(0, max_value + step_size, step_size), fontsize=30)
    plt.xticks([i + bar_width for i in index],
               occupation_data['classif1.label'], fontsize=30)

    wrapped_labels = [textwrap.fill(label, 13)
                      for label in occupation_data["classif1.label"]]
    plt.gca().set_xticklabels(wrapped_labels)
    # Show the plot
    plt.xlabel('Occupation', fontsize=40)
    plt.ylabel('Number of Foreigners', fontsize=40)
    plt.title('Foreigners by Occupation and Gender', fontsize=50)
    plt.legend(fontsize=30)

    plt.savefig(config.GRAPH_DIR / "foreigner_occupation.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


def analyze():
    # Read csv
    datapath = Path(config.DATA_DIR)
    file = list(datapath.glob(config.ILO_DATA + "*"))
    df = pd.read_csv(file[0])

    label_column = 'indicator.label'

    # Get unique labels from the label column
    labels = df[label_column].unique()

    # Create separate DataFrames for each label
    sep_dfs = {
        label: df[df[label_column] == label] for label in labels}

    # Chart 1
    inflowGraph(sep_dfs[
        "Inflow of working age foreign citizens by sex and country of citizenship (thousands)"])

    # Charts 2 and 3
    outsideOfWorkGraph(classif2Line(
        sep_dfs[
            "Persons outside the labour force by sex, education and place of birth (in thousands)"
        ]))

    # Charts 4 and 5
    unemployment(classif2Line(
        sep_dfs["Unemployment by sex, education and place of birth (thousands)"]))

    # Heatmap
    unemployment_heat_education(
        sep_dfs["Unemployment by sex, education and place of birth (thousands)"])

    foreigner_occupation(
        sep_dfs["Inflow of employed foreign citizens by sex and occupation (thousands)"])
