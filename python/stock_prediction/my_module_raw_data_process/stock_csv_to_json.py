import json, os

stockdata_dir = '../dataset/stockdata/'


def read_stock_csv(filename):
    lines = open(stockdata_dir + filename + '.csv', 'r').readlines()
    result_list = []
    del lines[0]
    lines.reverse()
    for line in lines:
        cells = line.split(',')
        result = []
        result.append(cells[0])  # date 0
        result.append(float(cells[1]))  # open 1
        result.append(float(cells[4]))  # close 2
        result.append(float(cells[3]))  # lowest 3
        result.append(float(cells[2]))  # highest 4
        result.append(float(cells[5]))  # volume 5
        result_list.append(result)
    return result_list


def store_result_list_in_json(filename, result_list):
    json_filename = filename + '.json'
    print 'Create file %s' % json_filename
    json_file = open(stockdata_dir + json_filename, 'w+')
    print 'Start writing file...'
    json_file.write(json.dumps(result_list))
    print 'finish!'
    json_file.close()
    print "File closed\n----------------------------------------"

if __name__ == '__main__':
    filename_list = os.listdir(stockdata_dir)
    print filename_list
    for filename in filename_list:
        print 'Processing the file %s' % filename
        splitted_filename = filename.split('.')
        if splitted_filename[-1] != 'csv':
            print "Not this file\n----------------------------------------"
            continue
        else:
            result_list = read_stock_csv(splitted_filename[0])
            store_result_list_in_json(splitted_filename[0], result_list)

