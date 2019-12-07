import requests
import scrapy
import numpy as np
import pandas as pd
from parsel import Selector
from time import sleep

start_url = 'https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm'
thePath="/Users/ashleyfreeman/Desktop/"
company = 'fb'


base_url = start_url[:-4]
extension = start_url[-4:]

# Define the headers here
headers = {
    'Cookie': '_ga=GA1.2.1102269652.1572218003; _gat_UA-2595786-1=1; _gid=GA1.2.1777396285.1572551815; _fbp=fb.1.1572218003676.629786889; cto_bundle=HhZd819HZXMlMkJpZEslMkZsdkkxcjd0aUVvZFYlMkJpYkpWRlBUNXBCbyUyRnBBM2tYSkZkUnVIM3FOaHRHTlA0ak15ZiUyQmVScVJ0NTd5TCUyQkFCTDFPdEtaalV6S1pQcGtYdkM0NWd5SERvZXJhMThBR243QzIwckl6dktSTVhENFV0WndvT3MySVYyU0djV0NhdVVRa1JrZ2RPUjJVemolMkJUdyUzRCUzRA; AWSALB=BOX7C6KHHsezx9WkkjblSgjvw0T6cmSO6Lr6j3IvYuQd5I9nAPg6ruZh2gA46jRX+YkwuvnnZnD6bTtpxWSbesSR7vx1zfiN9umoZAxN+MmLk87/A4N1WtZ5dckN; GSESSIONID=7B93EE0CCD07782CE4224771277CC2CD; cass=1; gdId=f21a7e7f-a068-4958-a458-50f1718b7ff1; JSESSIONID_JX_APP=FD59E58F47F567B779A7D6D914C33B9F; _mibhv=anon-1572218017509-8203140083_6890; _micpn=esp:-1::1572218017509; fpvc=5; JSESSIONID=F2F5CD78220A3A7525CDADA9595BAB67; __gads=ID=a56d26af1d8ce89b:T=1572218003:RT=1572551816:S=ALNI_MaHG7Xa_PAKZH5FY-rEvE-LriF_WQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; JSESSIONID_KYWI_APP=8CCDB42B4AE533294F3D5AA85CD3B915; JSESSIONID_PR_APP=5F532FDB1DC3A34805FF37AA2433A36C; __cf_bm=ca52d9b516064a4c3ab92608a3bf9f35fd305fea-1572551813-1800-AR4ZDzF+l8fii4FHVE+27R4eMesoyA0fdcM2BDr6q12646Ak7M9n/ywdOBXdU6EzXHl4hF3o7diFLFeMbcCLx/o=; _uac=0000016e236466a9af8b3f1bffe24fe0; cto_lwid=fe86fe38-d605-4cf9-b06c-c61a98a03f5b; uc=8F0D0CFA50133D96DAB3D34ABA1B8733EF6AEA36D67601E561EC937D0C1A29B04B6F6B8C357A752F92FA952FE64B9E43F6D2C70458196A4E4E9F8AFEDD8E67CA51406F0BB532899300DB523DF52A3B012DB2031B75DF9C9DFF86C2E3DF12125084615BEEAB6A75A24C974EA336B9DB9949557DEC18385F4D1265C8238F2813907898F3DA4C205E243E6DF33B85B633B6A626B9FBB21D0DC1; __gdpopuc=1; __qca=P0-649933593-1572218003679; _gcl_au=1.1.742292409.1572218003; G_ENABLED_IDPS=google; trs=direct:direct:direct:2019-10-27+16%3A13%3A21.761:undefined:undefined',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.glassdoor.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://www.glassdoor.com/',
    'Connection': 'keep-alive',
}

def process_response(response):
    selector = Selector(response)
    review_lis = selector.css('li.empReview')

    processed_reviews = []

    for review_li in review_lis:
        processed_review = {
            'date': '-',
            'summary': '',
            'job_title': '',
            'location': '',
            'overall_rating': 0,
            'work_life_balance_rating': 0,
            'culture_values_rating': 0,
            'career_opportunities_rating': 0,
            'comp_benefits_rating': 0,
            'senior_management_rating': 0,
            'main_text': '',
            'pros': '',
            'cons': '',
            'advice_management': '',
        }

        try:
            processed_review['date'] = review_li.css('.date')[0].xpath('./text()').get()
        except IndexError:
            pass

        processed_review['summary'] = review_li.css('.summary')[0].xpath('./a/span/text()').get()

        processed_review['job_title'] = review_li.css('.authorJobTitle')[0].xpath('./text()').get()

        try:
            processed_review['location'] = review_li.css('.authorLocation')[0].xpath('./text()').get()
        except IndexError:
            pass

        # Get overall rating
        processed_review['overall_rating'] = float(review_li.css('.gdStars').xpath('./span/span[@class="value-title"]/@title').get())

        # Get subratings
        subratings_div = review_li.css('.subRatings')

        for sub_rating in subratings_div.xpath('./ul/li'):
            sub_rating_type = sub_rating.xpath('./div[@class="minor"]/text()').get()

            if sub_rating_type == "Work/Life Balance":
                processed_review['work_life_balance_rating'] = float(sub_rating.xpath('./span/@title').get())
                pass
            elif sub_rating_type == "Culture & Values":
                processed_review['culture_values_rating'] = float(sub_rating.xpath('./span/@title').get())
                pass
            elif sub_rating_type == "Career Opportunities":
                processed_review['career_opportunities_rating'] = float(sub_rating.xpath('./span/@title').get())
                pass
            elif sub_rating_type == "Compensation and Benefits":
                processed_review['comp_benefits_rating'] = float(sub_rating.xpath('./span/@title').get())
                pass
            elif sub_rating_type == "Senior Management":
                processed_review['senior_management_rating'] = float(sub_rating.xpath('./span/@title').get())
                pass

        processed_review['main_text'] = review_li.css('.mainText')[0].xpath('./text()').get()

        for procon in review_li.css('.common__EiReviewTextStyles__allowLineBreaks'):
            info_type = procon.xpath('./p[@class="strong"]/text()').get()
            if(info_type == "Pros"):
                processed_review['pros'] = procon.xpath('./p[2]/text()').get()

                # If there is a "Show More" button append the rest of the comment
                if len(procon.xpath('./p[2]/span[@class="d-none"]')) > 0:
                    processed_review['pros'] = processed_review['pros'][:-3] + procon.xpath('./p[2]/span[@class="d-none"]/text()').get()

            elif(info_type == "Cons"):
                processed_review['cons'] = procon.xpath('./p[2]/text()').get()

                # If there is a "Show More" button append the rest of the comment
                if len(procon.xpath('./p[2]/span[@class="d-none"]')) > 0:
                    processed_review['cons'] = processed_review['cons'][:-3] + procon.xpath('./p[2]/span[@class="d-none"]/text()').get()
            elif(info_type == "Advice to Management"):
                processed_review['advice_management'] = procon.xpath('./p[2]/text()').get()

                # If there is a "Show More" button append the rest of the comment
                if len(procon.xpath('./p[2]/span[@class="d-none"]')) > 0:
                    processed_review['advice_management'] = processed_review['advice_management'][:-3] + procon.xpath('./p[2]/span[@class="d-none"]/text()').get()
            else:
                print("UNK")


        processed_reviews.append(processed_review)

    return processed_reviews

page_num = 1
processed_reviews = []

while len(processed_reviews)<=5000:
    # Construct the page url
    url = base_url+extension
    if page_num != 1:
        url = "{}_P{}{}".format(base_url, page_num, extension)

    print("Processing url {}...".format(url))

    # Get the first page
    response = requests.get(url, headers=headers).text

    new_processed_reviews = process_response(response)

    processed_reviews += new_processed_reviews

    print("Got {} new reviews. Total: {} reviews".format(len(new_processed_reviews), len(processed_reviews)))

    page_num += 1
    # Break if there are no new reviews
    if len(new_processed_reviews) == 0:
        break

    sleep(1)

    columns = ['date','summary', 'job_title','location','overall_rating','work_life_balance_rating','culture_values_rating',
                  'career_opportunities_rating','comp_benefits_rating','senior_management_rating','main_text','pros','cons','advice_management']


df = pd.DataFrame(processed_reviews,columns = columns)
filename = company + '.csv'
path = thePath + filename
df.to_csv(path)
