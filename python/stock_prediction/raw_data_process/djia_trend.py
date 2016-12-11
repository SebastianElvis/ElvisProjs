import csv
import datetime

class DJIATrend:
    def __init__(self, input_dir, output_dir):
        input_file = file(input_dir, 'rb')
        output_file = file(output_dir, 'w')
        self.input_csv = csv.reader(input_file)
        self.output_csv = csv.writer(output_file)


    def process_input(self):
        for line in self.input_csv:
            if self.input_csv.line_num < 2:
                self.input_csv.next()
                continue
            else:
                l = []
                l.append( datetime.datetime.strptime(line[0], '%Y-%m-%d').date() )
                l.append( 1 if line[1] <= line[4] else 0 )
                self.output_csv.writerow(l)

if __name__ == '__main__':
    d = DJIATrend('./^DJI.csv', './DJI_Trend.csv')
    d.process_input()
    d = None