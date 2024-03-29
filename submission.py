def submission(np_preds, submission_dir, file_name):
    np_preds[np_preds == 0] += 1
    submission_df = pd.read_csv(submission_dir)
    submission_df.iloc[:, 1:] = np_preds
    submission_df.to_csv(file_name, index=False)
