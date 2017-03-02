import pandas as pd

combined_dir = '../dataset/combined/'


def divide_train_test(dataset, divide_date):
    """
    Divide the whole dataset to the train/test dataset by the divide_date
    :param dataset: the DataFrame object generated from pandas.read_csv()
    :param divide_date: str indicating the date, like '2016-02-0
    :return: 2 DataFrame derived from the whole dataset
    """
    train = dataset[dataset['Date'] < divide_date]
    test = dataset[dataset['Date'] >= divide_date]
    return train, test


def derive_components_from_dataset(dataset):
    """
    Derive list of the dates/labels/documents from the dataset
    :param dataset: the DataFrame object generated from pandas.read_csv()
    :return: date_list, label_list, document_list
    """
    date_list = dataset.iloc[0:, 0]  # return pandas.core.series.Series
    label_list = dataset.iloc[0:, 1:11]
    document_list = dataset.iloc[0:, 12:]  # get the value by documents.values(a 2-dimentional array)
    return date_list, label_list, document_list

assembled_combined_csv = pd.read_csv(combined_dir + 'assembled_combined.csv', quoting=3)
train_dataset, test_dataset = divide_train_test(assembled_combined_csv, '2016-04-01')

