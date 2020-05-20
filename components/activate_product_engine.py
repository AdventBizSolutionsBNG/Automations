import sys
import os
import json
from product.productEngine import ProductEngine
import argparse

def main():
    try:
        payload = ""
        parser = argparse.ArgumentParser()
        parser.add_argument("payload", help="please provide the payload for activation in the form of json file")
        args = parser.parse_args()
        param_1 = args.payload
        cur_path = os.path.dirname(os.path.realpath(__file__))
        payload_file = os.path.join(cur_path,param_1)
        with open(payload_file,"r") as f:
            payload = json.load(f)
            p = ProductEngine()
            p.activate_product_engine(payload)

    except Exception as e:
        print("Error occurred during activation!!!")
        print(e)

if __name__=="__main__":
    main()

# # Sample Payload
# {
# "secret_key": "18fe008f-afce-4a2d-a43e-397d1b41148a",
# "registered_to": "ABC Corporation"
# }