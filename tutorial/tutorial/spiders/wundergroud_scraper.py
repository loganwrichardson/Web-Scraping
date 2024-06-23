# weather_scraper/weather_scraper/spiders/weather_spider.py

import scrapy
from datetime import datetime, timedelta


class QuotesSpider(scrapy.Spider):
    name = 'wunderspider'

    def start_requests(self):
        # urls = ['https://www.wunderground.com/dashboard/pws/KNCBOONE58/table/2022-04-1/2022-04-1/daily']
        #
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

        # # Start scraping from the initial date until June 1, 2024
        start_date = datetime.strptime('2022-04-01', '%Y-%m-%d')
        end_date = datetime.strptime('2024-06-01', '%Y-%m-%d')
        current_date = start_date

        while current_date <= end_date:
            formatted_date = current_date.strftime('%Y-%m-%d')
            url = f'https://www.wunderground.com/dashboard/pws/KNCBOONE58/table/{formatted_date}/{formatted_date}/daily'
            yield scrapy.Request(url=url, callback=self.parse)
            current_date += timedelta(days=1)

    def parse(self, response):
        date = response.xpath('/html/body/app-root/app-dashboard/one-column-layout/'
                              'wu-header/sidenav/mat-sidenav-container/'
                              'mat-sidenav-content/div[2]/section/section[1]/'
                              'div[1]/div/section/div/div/div/lib-history/'
                              'div[2]/lib-history-table/div/h3/strong'
                              ).get()
        # date = date[28:41]
        yield {
            'Date': date
        }

        # Extract rows of the table
        rows = response.xpath('//table[@class="history-table desktop-table"]/tbody/tr')

        for row in rows:
            # Extract time and temperature from each row
            time = row.xpath('./td[1]/strong').get()
            temp = row.xpath('./td[2]/lib-display-unit/span/span').get()

            yield {
                'Time': time,
                'Temp': temp
            }
        next_page = response.css("").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

