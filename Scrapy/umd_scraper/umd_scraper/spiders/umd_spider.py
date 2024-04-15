import scrapy
import logging
from trafilatura import fetch_url, extract
from nltk.tokenize import word_tokenize
import json
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

class UmdSpiderSpider(scrapy.Spider):

    page_num = 0
    num_repeats = 0

    def __init__(self, *args, **kwargs):
        # Define the loggers you want to configure
        loggers_to_configure = ["scrapy", "trafilatura", "urllib3", "asyncio"]
        self.set_logging_level(loggers_to_configure, logging.WARNING)
        super().__init__(*args, **kwargs)

        self.visited_links = self.load_visited_links()
        self.page_num = len(self.visited_links)

    name = "umd_spider"
    allowed_domains = ["registrar.umd.edu"]
    start_urls = ["https://registrar.umd.edu/calendars/advisor-calendar"]#"https://admissions.umd.edu/apply/freshman-application-faqs"]


    custom_settings = {
        'DEPTH_LIMIT': 4,  # Set the depth limit here
        'DUPEFILTER_DEBUG': True
    }

    

    def parse(self, response):

        if response.url in self.visited_links:
            self.num_repeats += 1
            self.log(f"{self.num_repeats} - Skipping already visited link: " + response.url)
            return
        
        self.visited_links.add(response.url)
        self.save_visited_links()
        
        self.page_num += 1
        link_name = f"{self.page_num}-{response.url.split('/')[-1]}"

        json_groups = self.build_groups(response.url)

        with open(f"scraped_data/{link_name}.json", 'w') as f:
            json.dump(json_groups, f)

        links = self.link_extractor.extract_links(response)
        self.log(f"{self.page_num}@{response.meta.get('depth')} - Found {len(links)} links at {response.url}")

        for link in links:
            # Filter out links that are not relevant or are not absolute URLs
            yield response.follow(link.url, callback=self.parse, errback=self.handle_error)

    def handle_error(self, failure):
        # This method will be called if an error occurs during the request
        self.log(f"Error occurred while processing {failure.request.url}: {failure.value}", level=logging.ERROR)
        # Optionally, you can log the error to a file or handle it in another way

    def build_groups(self, url):

        # Fetch the URL content
        downloaded = fetch_url(url)

        # Extract information from the HTML
        result = extract(downloaded,output_format="txt", include_links=True, include_tables=True, favor_recall=True)


        # Assuming 'result' contains the content of your text file
        lines = result.split('\n')

        # Initialize variables for grouping
        groups = []
        current_group = []
        current_tokens = 0

        # Iterate through each line
        for line in lines:
            # Tokenize the line
            line = line.encode("ascii", "ignore").decode()

            tokens = word_tokenize(line)
            # Check if adding this line would exceed 700 tokens
            if current_tokens + len(tokens) > 700:
                # Start a new group if adding this line would exceed 700 tokens
                groups.append(current_group)
                current_group = [line]
                current_tokens = len(tokens)
            else:
                # Otherwise, add the line to the current group
                current_group.append(line)
                current_tokens += len(tokens)

        # Append the last group if it's not empty
        if current_group:
            groups.append(current_group)

        # Convert all groups into one json file
        group_arr = []
        for group in groups:
            group_arr.append(" ".join(group))

        json_file = {f"{url}": group_arr}

        
        return json_file

    def load_visited_links(self):
        visited_links_file = "visited_links.json"
        try:
            with open(visited_links_file, 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    def save_visited_links(self):
        visited_links_file = "visited_links.json"
        with open(visited_links_file, 'w') as f:
            json.dump(list(self.visited_links), f)
    
    def set_logging_level(self, logger_names, level):
        for logger_name in logger_names:
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)

    link_extractor = LxmlLinkExtractor(
        allow=(),
        deny=('^mailto:', '^tel:'),
        allow_domains=(),
        deny_domains=(),
        deny_extensions=['mp4', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'exe', '7z', '7zip', 'apk', 'bz2', 'cdr', 'dmg', 'ico', 'iso', 'tar', 'tar.gz', 'webm', 'xz'],
        restrict_xpaths=(),
        restrict_css=(),
        restrict_text=(),
        tags=('a', 'area'),
        attrs=('href',),
        canonicalize=False,
        unique=True,
        process_value=None,
        strip=True
    )












