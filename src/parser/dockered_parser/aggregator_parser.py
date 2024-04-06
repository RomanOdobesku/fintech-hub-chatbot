import parser
import distill_aggregators
import time

if __name__ == '__main__':
    while True:
        parser.parse(distill_aggregators.links, 60 * 60, 'parsed_aggregators.csv', 100)
        time.sleep(60 * 60)

