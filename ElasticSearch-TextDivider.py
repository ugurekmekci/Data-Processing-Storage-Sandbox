# -*- coding: utf-8 -*-
import json
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
from config_provider import ConfigProvider


class AddressRootFix(object):
    def __init__(self, address):
        print address
        all_config = ConfigProvider().get_config_file()
        self.elastic_ip = all_config["elasticsearch_info"]["ip"]
        self.elastic_port = all_config["elasticsearch_info"]["port"]
        self.text_divider_index = all_config["elasticsearch_fix_address_root_indices"]["text_divider"]
        self.address_root_fix_index = all_config["elasticsearch_fix_address_root_indices"]["address_root_fix"]
        self.address_name_fix_index = all_config["elasticsearch_fix_address_root_indices"]["address_name_fix"]
        self.address_full_fix_index = all_config["elasticsearch_fix_address_root_indices"]["address_full_fix"]

        self.client = self.get_elasticsearch_client()
        divided_text = self.divide_text(address)
        #print divided_text
        fixed_address_by_root = self.fix_address_root(divided_text)
        fixed_full_adress = self.fix_full_address(fixed_address_by_root)
        print fixed_address_by_root
        print fixed_full_adress

    def get_elasticsearch_client(self):
        client = Elasticsearch([{'host': self.elastic_ip, 'port': self.elastic_port}], timeout=300)
        return client

    def divide_text(self, address_text):
        body = {}
        body["text"] = address_text
        #print body["text"]
        divided_text = self.client.indices.analyze(index=self.text_divider_index, body=body)
        return divided_text

    def fix_address_root(self, divided_text):
        fixed_address_by_root = []
        for word in divided_text["tokens"]:
            root_fix_req = Search().using(self.client).index(self.address_root_fix_index).query("match", text=word["token"])
            response_root_fix = root_fix_req.execute()

            if response_root_fix.hits.total > 0:
                response_root_fix_dict = response_root_fix.to_dict()
                fixed_address_by_root.append(response_root_fix_dict["hits"]["hits"][0]["_source"]["text"])
            else:
                name_fix_req = Search().using(self.client).index(self.address_name_fix_index).query("fuzzy", text=word["token"])
                response_name_fix = name_fix_req.execute()

                if response_name_fix.hits.total > 0:
                    response_name_fix_dict = response_name_fix.to_dict()

                    fixed_address_by_root.append(response_name_fix_dict["hits"]["hits"][0]["_source"]["text"])
                else:
                    fixed_address_by_root.append(word["token"])

        fixed_address_by_root_str = " ".join(fixed_address_by_root)
        #print fixed_address_by_root_str
        return fixed_address_by_root_str

    def fix_full_address(self, fixed_address_by_root):
        full_fix_req = Search().using(self.client).index(self.address_full_fix_index).query("match", text=fixed_address_by_root)
        response_full_fix = full_fix_req.execute()

        if response_full_fix.hits.total > 0:
            print("Address found")
            fixed_adress = response_full_fix["hits"]["hits"][0]["_source"]["text"]
            print response_full_fix["hits"]["hits"]
        else:
            print("Address not found")
            fix_address_check_from_api = YandexApi().get_address(fixed_address_by_root)

            print("Checking address from api...")
            api_response_check_req = Search().using(self.client).index(self.address_full_fix_index).query("match", text=fix_address_check_from_api)
            response_api_response_check = api_response_check_req.execute()

            if response_api_response_check.hits.total > 0:
                print("Checked address found in index.")
                fixed_adress = response_api_response_check["hits"]["hits"][0]["_source"]["text"]
            else:
                print("Checked address not found in index.")
                self.client.index(index=self.address_full_fix_index, doc_type="doc_type", body=json.loads(json.dumps({"text": fix_address_check_from_api})))
                print("Address  to index. ")
                fixed_adress = fix_address_check_from_api

        return fixed_adress


    


AddressRootFix("İstanbul	,	 Ümraniye	,	Esenşehir Mahallesi	,	 Mareşal Fevzi Çakmak Caddesi	,	 1A")