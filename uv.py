import requests
import pandas as pd


def csv_parse(csv, url_col):
    '''Parse url's from a csv.

    :param csv: the csv filepath
    :param url_col: the column name containing the urls

    :return urls: a list of the urls
    '''

    # parse the csv file
    df = pd.read_csv(
        csv,
        usecols=[url_col]
    )

    # convert the dataframe series to a list
    urls = df[url_col].tolist()
    
    return urls


def url_valid(url, username=None, password=None):
    '''Check if a url is valid.

    :param url: the url to check
    :param username: authentication username, if required
    :param password: authentication password, if required

    :return exists: boolean representing if the url exists or not
    :return request: the HEAD request object
    '''

    # make a head request to the url
    request = requests.head(url, auth=(username, password))

    # check for status codes which indicate a valid url
    # 1XX - informational
    # 2XX - success
    # 3XX - redirection

    status = request.status_code

    if status < 400:
        print('Exists - ' + url)
        exists = True
    else:
        print('Does not exist - ' + url)
        exists = False
    
    return exists, request


def validate(url_list, mode='all', username=None, password=None):
    '''Validate a list of urls.

    :param url_list: a list of urls to validate
    :param mode: set the return mode - all, exists, or doesnt_exist
    :param username: authentication username, if required
    :param password: authentication password, if required

    :return out_objs: a list of the resulting HEAD request objects based on the
    mode the user chooses
    '''
    
    # make lists to hold the resulting request objects
    exists_request_objs = []
    doesnt_exist_request_objs = []

    # validate the urls
    print('Validating ' + str(len(url_list)) + ' urls...')

    for url in url_list:
        result = url_valid(url, username=username, password=password)

        # add the request object to the appropriate list
        obj = result[1]

        if obj.status_code < 400:
            exists_request_objs.append(obj)
        else:
            doesnt_exist_request_objs.append(obj)
    
    print('Finished validating the urls!')
    print(str(len(exists_request_objs)) + ' urls exist.')
    print(str(len(doesnt_exist_request_objs)) + ' urls do not exist.')

    # return the request objects
    if mode == 'all':
        out_objs = exists_request_objs + doesnt_exist_request_objs
    elif mode == 'exists':
        out_objs = exists_request_objs
    elif mode == 'doesnt_exist':
        out_objs = doesnt_exist_request_objs
    
    return out_objs


if __name__ == '__main__':

    # static path
    your_file = r'c:\dir\some.csv'

    validate(
        url_list=csv_parse(your_file, 'url_column')
    )