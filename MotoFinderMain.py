


# Motofinder: webscraper for sahibinden.com to get motorcycle listings from various cities.

import requests
from bs4 import BeautifulSoup as bs 
import math

""" First page doesn't have an offset value,
    so its index is 0 and returns empty string "".
    Starting from the 2. page, pages get an offset
    value of mulplies of 50. So the index of the 2.
    page is 1 and its offset value is 1*50.
    3. page has an offset value of 2*50
    n^th page has (n-1)*50.
    50 is the number of items presented in each page.
"""    
def PageNum(num):
    if(num == 0):
        return ""
    else:
        return "pagingOffset=" + str(50 * num) + "&" 

# request, create the soup and scrape only for the given URL.
res_file = open("result_file", "a+")

def RunScrape(URL_p1,num, URL_p2): #url and number of pages to scrape
    page_offset_num = 0
    
    #it doesn't work after scraping 20 pages
    page_limit = 20
    while page_offset_num < page_limit:
        """ print values to see that the program is alive
            and it's working as expected.
        """
        print(page_offset_num)
        print(num)
        
        #request process often caused interesting problems.
        try:
            URL = URL_p1 + PageNum(page_offset_num) + URL_p2 

            page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"})            
            page_soup = bs(page.content, "html.parser")
            search_res_item_iter = page_soup.find_all("tr", class_="searchResultsItem")
            print(URL)
        except Exception as e:
            print("request: " + str(e))
    
        for item in search_res_item_iter:
            """ it's in try/catch block because 
                some missing attribute values have caused crashes.
                I wanted the program to continue regardles of the
                missing values.
            """
            try:
                res_file.write("\n*-*-*-*-*-*-*-*-*-*\n")

                res_file.write("başlık: "+item.find("a").get("title") + "\n")

                tag_attr_iter = item.find_all("td", class_="searchResultsTagAttributeValue")
                res_file.write("marka: " + tag_attr_iter[0].text.strip() + "\n")
                res_file.write("model: " + tag_attr_iter[1].text.strip() + "\n")
 
                attr_iter = item.find_all("td", class_="searchResultsAttributeValue")
                res_file.write("km: " + attr_iter[1].text.strip()  + "\n")
                res_file.write("model yılı: " + attr_iter[0].text.strip() + "\n")

                res_file.write("fiyat: " + item.find("td", class_="searchResultsPriceValue").text.strip()  + "\n")

                detailed_url = "https://sahibinden.com" + item.find("a").get("href")  
                res_file.write("link: "+ detailed_url + "\n")
            except Exception as e:
                print("scraping: " + str(e))
    
        page_offset_num += 1
        # If required number of pages is less than the page limit, 
        # stop the loop to prevent unnecessary failed scraping attempts.
        if(page_offset_num == num):
            break

#take a number in string type and convert it to number type
def NumberMaker(str_num):
    num_list = str_num.split('.')
    
    all_listings_num=""
    i=0
    for i in range(len(num_list)):
        all_listings_num += num_list[i]
        i+=1

    all_listings_num = int(all_listings_num)

    return all_listings_num

def URLSetup():
    URL_all_p1 = "https://www.sahibinden.com/motosiklet/" + city_var + "/ikinci-el?"
    URL_all_p2 = "pagingSize=50&hasPhoto=true&a269_max=2020&sorting=price_asc&a269_min=1988"
    URL_all = URL_all_p1 + URL_all_p2

    #the request process have caused unexpected errors.
    try:
        print(URL_all)

        page = requests.get(URL_all, headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"})
        page_soup = bs(page.content, "html.parser")
        
        res_text = page_soup.find("div", class_="result-text").find_all("span")[1].text.split()

        all_listings_num = NumberMaker(res_text[0])
    except Exception as e:
        print("request all listings: " + str(e))

    while True:
       if(all_listings_num <= 1000):
            #num: number of pages to scrape, since each page has 50 listings num = (total listings)/50
            num = math.ceil(float(all_listings_num)/50)

            RunScrape(URL_all_p1, num, URL_all_p2)
            break
        else:
            min_price = NumberMaker(input("Enter min price: "))
            max_price = NumberMaker(input("Enter max price: "))
            num = input("Enter page number: ")
            print("ctrl + c for termination")

            URL_p1 ="https://www.sahibinden.com/motosiklet/" + city_var + "/ikinci-el?"

            URL_p2 = "pagingSize=50&hasPhoto=true&a269_max=2020&sorting=price_asc&a269_min=1988&price_min=" + str(min_price) + "&price_max=" + str(max_price)

            RunScrape(URL_p1, num, URL_p2)

# choose which city to scrape from
while True:
    city_var = input("Choose your city: \ntype 'i' for izmir,\n'b' for balıkesir,\n'ç' for çanakkale.\n")
    if(city_var == 'i'):
        
        city_var = "izmir"
        URLSetup()
        break
    elif(city_var == 'b'):

        city_var = "balikesir"
        URLSetup()
        break
    elif(city_var == 'ç'):

        city_var = "canakkale"
        URLSetup()
        break
    else:
        continue

res_file.close()
