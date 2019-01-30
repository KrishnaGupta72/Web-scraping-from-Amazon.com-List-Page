import time
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#____________________Input Section : ____________________________

tot_search = int(input("Please enter total number of search do you want to perform: "))
search_string = []
for i in range(0, tot_search):
    j = i + 1
    search_string.append(input('Please enter "%d" searching string: ' % j))

now=datetime.datetime.now()
curr_date_time=now.strftime("%Y-%m-%d %H:%M:%S")

#User defined function for extracting a portion of string from a given string.
def get_str(resp_str,frm_str,to_str):
    start_index = resp_str.find(frm_str) + len(frm_str)
    end_index = resp_str.find(to_str, start_index)
    resp_dict = resp_str[start_index:end_index]
    return resp_dict

#Loop for total number of searches
for search_str in search_string:
    #print(search_str)
    #To calculate time in capturing data
    st_time=datetime.datetime.now()
    #Path of chrome driver
    driver = webdriver.Chrome("E:/PyCharm Projects/chromedriver.exe")
    #Hitting google.com
    driver.get('http://google.com')
    time.sleep(4)
    #Fetching Input box using xpath
    search=driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')
    #Pass search string on search box.
    search.send_keys(search_str)
    time.sleep(2)
    search.send_keys(Keys.RETURN)
    time.sleep(12)
    #Capturing the website urls and stored in list "listval"
    listval = driver.find_elements_by_xpath('//div[@class="g"]//div[@class="r" and boolean(./span)]/a')
    #print(len(listval))
    site_rank_count = 0
    listpage_count = 1
    count_4_header = 0
    #Loop for capturing and storing all websites urls and other information into csv file from list.
    for item in listval:
        end_time=datetime.datetime.now()
        final_time_stamp=end_time-st_time
        count_4_header=count_4_header+1
        site_rank_count = site_rank_count + 1
        HotelName=item.get_attribute('href')
        if "www" in HotelName:
            HotelName = get_str(HotelName, 'www.', '.')
        else:# To handle condition like "https://santorinidave.com/best-hotels-london"
            HotelName = get_str(HotelName, '://', '.')

        if item == " " or item == "" or item == None or item == None or item == '' or item == ' ':
           msg = "krishna"  # Do nothing this condition solved
        else:
            #Create and open a dynamic csv file name in append mode.
            with open("google_search " + search_str + ".csv", "a", newline = '') as file:
                #Defines column names into a csv file.
                field_names = ['City', 'Website_Name', 'Url', 'Website_Rank', 'Availablity_Page_Number','Searching_Time','Date_Time']
                writer = csv.DictWriter(file, fieldnames=field_names)
                #Condition for writing header only once.
                if count_4_header==1:
                    writer.writeheader()
                #Writing all information in a row.
                writer.writerow(
                {
                    'City': search_str,
                    'Website_Name': HotelName,
                    'Url': item.get_attribute('href'),
                    'Website_Rank': str(site_rank_count),
                    'Availablity_Page_Number': str(listpage_count),
                    'Searching_Time': str(final_time_stamp),
                    'Date_Time': curr_date_time
                }
            )


    #Capturing all list pages urls from home page and store into a list "list_page_val".
    list_page_val=driver.find_elements_by_xpath('//div[@id="navcnt"]/table/tbody/tr/td/a[@class="fl"]')
    #print(list_page_val)#[0].get_attribute('href')

    #Storing all list pages urls into a new list.
    list=[]
    for i in list_page_val:
        #list_page_urls=i.get_attribute('href')
        list.append(i.get_attribute('href'))

    #Loop for hitting all list pages one by one and capturing all website urls.
    for List_page_urls in list:
        listpage_count = listpage_count + 1
        #print(List_page_urls)
        #Now Hitting next list pages upto 5 list pages
        driver.get(List_page_urls)
        #driver.implicitly_wait(10)
        time.sleep(10)
        #capturing all website urls from current list page.
        #next_page_listval = driver.find_elements_by_xpath('//div[@class="TbwUpd"]')
        next_page_listval = driver.find_elements_by_xpath('//div[@class="g"]//div[@class="r"]/a[1]')
        ##Loop for writing all websites urls and other information into csv file from list.

        for new_item in next_page_listval:
            end_time = datetime.datetime.now()
            final_time_stamp = end_time - st_time
            site_rank_count = site_rank_count + 1
            HotelName = new_item.get_attribute('href')
            if "www" in HotelName:
                HotelName = get_str(HotelName, 'www.', '.')
            else:  # to handle condition like "https://santorinidave.com/best-hotels-london"
                HotelName = get_str(HotelName, '://', '.')

            if new_item == " " or new_item == "" or new_item == None or new_item == None or new_item == '' or new_item == ' ':
                msg="krishna"#Do nothing this condition solved
            else:
                # #with open("google_search.csv", "ab", encoding="utf-8") as file:
                with open("google_search " + search_str + ".csv", "a", newline='') as file:

                    field_names = ['City', 'Website_Name', 'Url', 'Website_Rank', 'Availablity_Page_Number','Searching_Time','Date_Time']
                    writer = csv.DictWriter(file, fieldnames=field_names)

                    writer.writerow(
                        {
                            'City': search_str,
                            'Website_Name': HotelName,
                            'Url': new_item.get_attribute('href'),
                            'Website_Rank': str(site_rank_count),
                            'Availablity_Page_Number': str(listpage_count),
                            'Searching_Time': str(final_time_stamp),
                            'Date_Time': curr_date_time
                        }
                    )
        if listpage_count == 5:#(writing information upto List page=5 then exit)
            break