import pandas as pd
import numpy as np

# take a random sample of 2000 rows as csv is too large 
chunksize = 100000
sampled_chunks = []
for chunk in pd.read_csv('messages-demo.csv', chunksize=chunksize, low_memory=False):
    sampled_chunk = chunk.sample(frac=0.0002, random_state=1)
    sampled_chunks.append(sampled_chunk)

messages_df = pd.concat(sampled_chunks, ignore_index=True)


# Make some cleanup (delete unnecessary columns) and processing
messages_df.drop(labels=['id', 'created_at', 'updated_at', 'category'], inplace=True, axis=1)

# Fix data types
messages_df['campaign_id'] = messages_df['campaign_id'].astype('Int64')
messages_df['client_id'] = messages_df['client_id'].astype('Int64')

def convert_to_bool(value):
    if value == 't':
        return True
    else:
        return False

messages_df['is_opened'] = messages_df['is_opened'].apply(convert_to_bool)
messages_df['is_clicked'] = messages_df['is_clicked'].apply(convert_to_bool)
messages_df['is_unsubscribed'] = messages_df['is_unsubscribed'].apply(convert_to_bool)
messages_df['is_hard_bounced'] = messages_df['is_hard_bounced'].apply(convert_to_bool)
messages_df['is_soft_bounced'] = messages_df['is_soft_bounced'].apply(convert_to_bool)
messages_df['is_complained'] = messages_df['is_complained'].apply(convert_to_bool)
messages_df['is_blocked'] = messages_df['is_blocked'].apply(convert_to_bool)
messages_df['is_purchased'] = messages_df['is_purchased'].apply(convert_to_bool)

messages_df['date'] = pd.to_datetime(messages_df['date'])
messages_df['sent_at'] = pd.to_datetime(messages_df['sent_at'])
messages_df['opened_first_time_at'] = pd.to_datetime(messages_df['opened_first_time_at'])
messages_df['opened_last_time_at'] = pd.to_datetime(messages_df['opened_last_time_at'])
messages_df['clicked_first_time_at'] = pd.to_datetime(messages_df['clicked_first_time_at'])
messages_df['clicked_last_time_at'] = pd.to_datetime(messages_df['clicked_last_time_at'])
messages_df['unsubscribed_at'] = pd.to_datetime(messages_df['unsubscribed_at'])
messages_df['hard_bounced_at'] = pd.to_datetime(messages_df['hard_bounced_at'])
messages_df['soft_bounced_at'] = pd.to_datetime(messages_df['soft_bounced_at'])
messages_df['complained_at'] = pd.to_datetime(messages_df['complained_at'])
messages_df['blocked_at'] = pd.to_datetime(messages_df['blocked_at'])
messages_df['purchased_at'] = pd.to_datetime(messages_df['purchased_at'])

# find columns with missing values
def missing_data(df):
    missing_data = df.isnull().sum()
    return(missing_data[missing_data > 0])

# calculate percentage of missing values
total_rows = len(messages_df)
missing_data = messages_df.isnull().sum()
percentage_missing = (missing_data / total_rows) * 100

# missing report
def missing_report(missing_data, percentage_missing):
    report_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing Values': missing_data.values,
        'Percentage Missing': percentage_missing.values
    }).sort_values(by='Percentage Missing', ascending=False)
    
    return report_df

missing_report = missing_report(missing_data, percentage_missing)
print(missing_report)

# drop columns with more than 50% missing values
messages_df.drop(columns=missing_report[missing_report['Percentage Missing'] > 50]['Column'], inplace=True)

# leftover columns with missing data
left_missing = messages_df.isnull().sum()
print(left_missing[left_missing > 0])

# drop columns 
messages_df.drop(columns=['email_provider', 'is_hard_bounced', 'is_soft_bounced'], inplace=True)

num_na = messages_df.isnull().sum().sum()
print("Number of missing values:", num_na)

# count the number of duplicate rows
num_duplicates = messages_df.duplicated().sum()
print("Number of duplicate rows:", num_duplicates)

messages_df.to_csv('cleaned_messages_demo.csv', index=False)