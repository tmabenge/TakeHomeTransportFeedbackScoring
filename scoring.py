#!/usr/bin/python

import os
import pandas as pd
import util


class File:
    """

    :return:
    """

    def read_file_data(self, file_path, sep) -> object:
        """

        :return:
        :rtype: object
        :param sep:
        :param file_path:
        :return:
        """
        with open(file_path, 'r') as file:
            df_data = pd.read_csv(file, sep=sep, header=None, engine='python')
            return df_data

    def write_csv(self, data_frame, file_name):
        """

        :param file_name:
        :param data_frame:
        """
        data_frame.to_csv(
            file_name,
            index=None, header=None
        )

        return 'csv file added successfully..'


class SentimentScores:
    """

    :return:
    """
    File_co = None

    def __init__(self, file: File):
        self.File_co = file

    def load_files_into_memory(self,ref_data_file_name, scores_file_name, ref_data_del, scores_del) -> object:
        """
        Loads files into memory

        :rtype: object
        :return list of dataframes:
        """

        if not os.path.isfile(ref_data_file_name) \
                and not os.path.isfile(scores_file_name):
            return []

        ref_data_df = self.File_co.read_file_data(ref_data_file_name, ref_data_del)
        ref_data_df = self.clean_ref_data(ref_data_df)
        scores_df = self.File_co.read_file_data(scores_file_name, scores_del)

        return [ref_data_df, scores_df]

    def calculate_average_score(self, data_frame) -> object:
        """
        Calculates average scores for each route,
        per day of the week.

        :param data_frame:
        """
        data_frame = self.omit_entries_by_score(0, 10, 2, data_frame)

        res = data_frame \
            .groupby([1, 0]) \
            .agg({2: ['mean']}).reset_index()

        res.columns = res.columns.droplevel(-1)
        res = res.sort_values([1, 2], ascending=False)

        return res

    def omit_entries_by_score(self, min_score, max_score, col, data_frame):
        data_frame = data_frame.drop(data_frame[data_frame[col] == min_score].index)
        data_frame = data_frame.drop(data_frame[data_frame[col] == max_score].index)
        return data_frame


    def clean_ref_data(self, data_frame):
        """
        Removes additional text from route identifiers
        e.g 'METRO'
        column

        :param data_frame:
        :return:
        """
        for i in data_frame.index:
            data_frame.at[i, 0] = data_frame.at[i, 0].split()[0]
        return data_frame

    def replace_r_id_with_r_name(self, df_av_scores, df_ref_data):
        """
        Replaces route identifiers in {df_av_scores} with
        route name from {df_ref_data}

        :rtype: object
        :param df_av_scores:
        :param df_ref_data:
        :return:
        """

        for i in df_av_scores.index:
            temp_df = df_ref_data[df_ref_data[0] == df_av_scores.at[i, 1]]
            if temp_df is not None:
                df_av_scores.at[i, 1] = temp_df[1].to_string().split('  ')[2]
                df_av_scores.at[i, 0] = util.get_weekday(df_av_scores.at[i, 0])

        return df_av_scores
