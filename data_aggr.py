__author__ = 'Bouhm'

#Program that uses methods from RiotAPIStats mainly for testing/debugging
from riot_API_data import RiotAPIData
import keys
import pprint

def main():
    api = RiotAPIData(keys.API_KEY)
    #pprint.pprint(api._get_BMB_items_data(1907212062))
    data = api._get_BMB_items_data(1907212062)
    pprint.pprint(api._id_to_name(data))

if __name__ == "__main__":
    main()
