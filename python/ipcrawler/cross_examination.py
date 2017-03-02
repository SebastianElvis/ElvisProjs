# -*- coding: utf-8 -*-

import pymongo
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def convert_csv_to_dict(csv_file):
    ip_dict = {}
    print 'Generating ip_dict...'
    for line in csv_file.readlines():
        line = line.strip('\n')
        splitted_line = line.split(',')
        if len(splitted_line) >= 2 and splitted_line[1] == u'中国':
            single_ip_dict = dict()
            if len(splitted_line) >= 3:
                single_ip_dict['province'] = splitted_line[2]
            if len(splitted_line) >= 4:
                single_ip_dict['city'] = splitted_line[3]
            else:
                single_ip_dict['city'] = ''
            ip_dict[splitted_line[0]] = single_ip_dict
    print 'Finished!'
    return ip_dict


def cross_examine_mongodb_with_csv(ip_dict):
    start_ip_result = {}
    end_ip_result = {}
    start_ip_result['match_province'] = start_ip_result['match_city'] = end_ip_result['match_province'] = end_ip_result['match_city'] = []
    client = pymongo.MongoClient()
    col = client.get_database('ip').get_collection('yqie')
    cursor = col.find()
    for yqie_ip_record in cursor:
        # print 'Examine ip_start: ', yqie_ip_record['ip_start'], ' ip_end: ', yqie_ip_record['ip_end']
        if yqie_ip_record['ip_start'] in ip_dict.keys():
            print 'Find mutual start ip! ', yqie_ip_record['ip_start']
            single_ip_dict = ip_dict[yqie_ip_record['ip_start']]
            if yqie_ip_record['province'][0:-1] == single_ip_dict['province']:
                if yqie_ip_record['city'][0:-1] == single_ip_dict['city']:
                    print 'START IP, Province, City match!', yqie_ip_record
                    start_ip_result['match_city'].append(yqie_ip_record)
                else:
                    print 'START IP, Province match!', yqie_ip_record
                    start_ip_result['match_province'].append(yqie_ip_record)

        if yqie_ip_record['ip_end'] in ip_dict.keys():
            print 'Find mutual end ip! ', yqie_ip_record['ip_end']
            single_ip_dict = ip_dict[yqie_ip_record['ip_end']]
            if yqie_ip_record['province'][0:-1] == single_ip_dict['province']:
                if yqie_ip_record['city'][0:-1] == single_ip_dict['city']:
                    print 'END IP, Province, City match!', yqie_ip_record
                    end_ip_result['match_city'].append(yqie_ip_record)
                else:
                    print 'END IP, Province match!', yqie_ip_record
                    end_ip_result['match_province'].append(yqie_ip_record)

    return start_ip_result, end_ip_result


if __name__ == "__main__":
    ip_dict = convert_csv_to_dict(open('./ipdata/ip_location.csv', 'r'))
    start_ip_result, end_ip_result = cross_examine_mongodb_with_csv(ip_dict)
    print json.dumps(start_ip_result), "\n", json.dumps(end_ip_result)
