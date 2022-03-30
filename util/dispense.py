import csv
import os

from util.constants import BROWNIE_PROJECT as B
from util.base18 import fromBase18, toBase18

def dispenseRewards(csv_dir:str, airdrop_addr:str, from_account):
    """
    @description
      Sends tokens to addresses, as specified in CSV file. 
      Which token is specified in airdrop contract. (Not specific to OCEAN.)

    @arguments
      csv_dir -- str -- directory path for csv file
      airdrop_addr -- str -- address of airdrop contract
      from_account --
    """
    [tos, _, values_int] = csvToRewardsLists(csv_dir)
    airdrop = B.Airdrop.at(airdrop_addr)
    TOK = B.Simpletoken.at(airdrop.getToken())
    TOK.approve(airdrop, sum(values_int), {"from": from_account})
    airdrop.allocate(tos, values_int, {"from": from_account})
    
def rewardsPathToFile(path:str) -> str:
    return os.path.join(path, 'rewards.csv')

def rewardsToCsv(rewards:dict, csv_dir:str) -> str:
    """
    @description
      Given rewards dict, store as csv:

      address  value
      0x123    123.123
      0x456    456.456
      ..       ..

    @arguments
      rewards -- dict of [to_addr] : value_float (*not* base 18)
      csv_dir -- directory path for csv file
    """
    csv_file = rewardsPathToFile(csv_dir)
    assert not os.path.exists(csv_file), f"{csv_file} can't already exist"
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["address", "value"])
        for to_addr, value in rewards.items():
            writer.writerow([to_addr, value])
    print(f"Filled rewards file: {csv_file}")

def csvToRewardsLists(csv_dir):
    """
    @description
      Given rewards csv, extract it two lists

    @arguments
      csv_dir -- directory path for csv file

    @return
      tos -- list of to_addr_str
      values_float -- list of value_float (*not* base 18)
      values_int -- list of value_int (base 18, like wei)
    """
    csv_file = rewardsPathToFile(csv_dir)
    tos, values_float, values_int = [], [], []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row_i, row in enumerate(reader):
            if row_i == 0: #header
                pass
            else:
                to, value_float = row[0], float(row[1])
                value_int = toBase18(value_float)
                tos.append(to)
                values_float.append(value_float)
                values_int.append(value_int)
    return (tos, values_float, values_int)

