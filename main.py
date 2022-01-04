import scoring
import util

if __name__ == '__main__':
    file = scoring.File()
    sentiment_scores = scoring.SentimentScores(file)

    df_files = sentiment_scores.load_files_into_memory()
    df_avg_scores = sentiment_scores.calculate_average_score(df_files[1])

    df_final_avg_scores_with_r_name_day = \
        sentiment_scores.replace_r_id_with_r_name(df_avg_scores, df_files[0])

    file.write_csv(
        df_final_avg_scores_with_r_name_day,
        'processed/' + str(util.gm_time()) + '_' + 'result.txt'
    )
