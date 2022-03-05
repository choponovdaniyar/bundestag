import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import json


class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers["user-agent"] = UserAgent().random
        self.users = list()
        self.links = list()



    def get_soup(self, url):
        resp = self.session.get(url)
        try:
            return BeautifulSoup(resp.text, "lxml")
        except:
            print(resp)
            return "<div>{}</div>".format(resp)



    def get_userLink(self, url):
        soup = self.get_soup(url)
        add = len(self.links)
        for x in soup.find("body").contents:
            a = x.find("a")
            if a in [None, -1]:
                continue
            print("get {}".format(a.attrs["href"]))
            self.links.append(a.attrs["href"])
        return len(self.links) - add > 0
    


    def parse_userLink(self, offset=0):
        link = "https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&offset={}".format(offset)
        if self.get_userLink(link):
            self.parse_userLink(offset + 20)
        



    def parse_user(self, link):
        soup = self.get_soup(link)
        div = soup.find("div", class_ = "bt-biografie-name")
        info = {
            "person-name": div.contents[1].text.strip().split(",")[0],
            "company_name": div.contents[3].text.strip(),
            "social_networks": dict()
        }
        networks = [ x.attrs for x in soup.find_all("a", class_ = "bt-link-extern")]
        for x in networks:
            info["social_networks"][x["title"]] = x["href"]
        self.users.append(info)



    def dict_to_json(self):
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)



    def run(self): 
        self.parse_userLink()
        pages = len(self.links)
        for x in range(pages):
            self.parse_user(self.links[x])
            print("{}/{}".format(x+1, pages))
        self.dict_to_json()

if __name__ == "__main__":
    parser = Parser()    
    parser.run()
