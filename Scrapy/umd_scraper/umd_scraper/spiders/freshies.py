import scrapy
import json


class FreshiesSpider(scrapy.Spider):
    name = "freshies"
    allowed_domains = ["umd.edu"]
    start_urls = ["https://admissions.umd.edu/apply/freshman-application-faqs"]

    custom_settings = {
        'DEPTH_LIMIT': 1  # Set the depth limit here
    }

    page_num = 0

    def parse(self, response):

        self.page_num += 1
        link_name = f"{self.page_num}-{response.request.url.split('/')[-1]}"
        self.log("Scraping: " + link_name)
        # Extract all text from the page
        all_text = response.xpath('//text()').getall()

        # Filter out empty lines and strip whitespace for text
        all_text = [line.strip() for line in all_text if line.strip()]
        all_text = '\n'.join(all_text)

        # Save all text to a file
        filename_text = 'scraped_data/{}.txt'.format(link_name)
        with open(filename_text, 'w', encoding='utf-8') as f:
            f.write(all_text)

        self.log(f'Saved all text to {filename_text}')


        links = []
        anchor_elements = response.xpath('//a') 
        self.log(f"RUNNING RECURSION ON FOLLOWING: {anchor_elements[50:52]}")

        
        for anchor in anchor_elements[50:52]:#FOR TESTING ONLY THE SAMPLE LINK
            # Extract link URL
            self.log(f"Checking Link: {anchor}")
            link_url = anchor.xpath('./@href').get()

            # Extract text associated with the link
            link_text = ''.join(anchor.xpath('.//text()').getall()).strip()

            # Append the link URL and associated text to the data list
            links.append({
                'url': link_url,
                'text': link_text
            })

            if response.meta['depth'] < self.settings.get('DEPTH_LIMIT'):
                yield response.follow(link_url, callback=self.parse)

        # Save data to a JSON file
        filename = 'scraped_data/{}.json'.format(link_name)
        with open(filename, 'w') as f:
            json.dump(links, f)

        f.close()

        self.log(f'Saved data to {filename}')