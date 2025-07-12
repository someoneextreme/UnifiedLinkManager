# UnifiedLinkManager
UnifiedLinkManager streamlines link management by scraping, parsing, and removing duplicate URLs, then categorizing them efficiently.
Designed for educational and research use, it provides a structured, easy-to-use system to collect, clean, and organize links, ensuring a reliable and well-maintained repository.
# Browser_Scraper
Brave Browser Path:
The script explicitly sets the path to the Brave browser executable. You need to ensure this path matches where Brave is installed on your system.
Automatic ChromeDriver Management:
It uses a tool to automatically download and manage the compatible ChromeDriver for your Brave browser version, eliminating the need for manual driver setup.
How It Works:
Configures Selenium to launch Brave with options to prevent automation detection.
Navigates to Bing and performs a search based on user input.
Scrapes search result titles and URLs from multiple pages until the requested number of results is collected.
Handles cookie consent popups automatically.
Saves results in a text file on the desktop.
