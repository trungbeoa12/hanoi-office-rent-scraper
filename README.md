# 🏢 Real Estate Web Scraper

A professional web scraping tool for collecting real estate data from major Vietnamese property websites. This project provides a robust, scalable solution for gathering property listings with anti-detection features and resume capability.

## 🌟 Features

- **Multi-Website Support**: Crawls data from Nhà Tốt, MuaBan.net, and BatDongSan.com.vn
- **Anti-Detection**: Advanced techniques to avoid being blocked by websites
- **Resume Capability**: Automatically resumes from the last processed page
- **Structured Data**: Extracts detailed property information in CSV format
- **Error Handling**: Robust error handling with detailed logging
- **Configurable**: Easy to configure and extend for new websites

## 🎯 Supported Websites

| Website | URL | Data Fields |
|---------|-----|-------------|
| **Nhà Tốt** | nhatot.com | Title, Details, URL |
| **MuaBan.net** | muaban.net | Title, Details, URL |
| **BatDongSan** | batdongsan.com.vn | Title, Address, Price, Area, Contact, etc. |

## 📋 Requirements

- Python 3.8+
- Chrome browser
- ChromeDriver (included)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd real-estate-scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Scraper

```bash
# Crawl all websites
python main.py

# Crawl specific website
python main.py --website nhatot

# Run in headless mode
python main.py --headless

# Use existing Chrome profile
python main.py --use-profile
```

## 📁 Project Structure

```
real-estate-scraper/
├── src/
│   ├── config.py              # Configuration settings
│   ├── crawlers/
│   │   ├── __init__.py
│   │   ├── base_crawler.py    # Base crawler class
│   │   ├── nhatot_crawler.py  # Nhà Tốt crawler
│   │   ├── muaban_crawler.py  # MuaBan.net crawler
│   │   └── batdongsan_crawler.py # BatDongSan crawler
│   └── utils/
│       ├── __init__.py
│       ├── webdriver_manager.py # WebDriver utilities
│       └── csv_manager.py       # CSV file management
├── data/                       # Input data directory
├── output/                     # Output CSV files
├── logs/                       # Log files
├── main.py                     # Main script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## ⚙️ Configuration

The scraper can be configured by modifying `src/config.py`:

- **Chrome Driver Path**: Update `CHROMEDRIVER_PATH`
- **User Agents**: Add more user agents to `USER_AGENTS` list
- **Delays**: Adjust timing settings for different websites
- **Selectors**: Update CSS/XPath selectors if websites change

## 📊 Output Data

### CSV Files

The scraper generates CSV files in the `output/` directory:

- `output_nhatot.csv` - Nhà Tốt data
- `output_muaban.csv` - MuaBan.net data  
- `output_batdongsan.csv` - BatDongSan data

### Data Fields

**Nhà Tốt & MuaBan.net:**
- Tiêu đề (Title)
- Text chi tiết (Details)
- URL

**BatDongSan.com.vn:**
- Tiêu đề (Title)
- Địa chỉ (Address)
- Mức giá (Price)
- Diện tích (Area)
- Mặt tiền (Frontage)
- Số tầng (Floors)
- Số phòng tắm, vệ sinh (Bathrooms)
- Tiện ích (Amenities)
- Mô tả (Description)
- Ngày đăng (Post Date)
- Ngày hết hạn (Expiry Date)
- Loại tin (Post Type)
- Mã tin (Post ID)
- SĐT liên hệ (Contact Phone)
- Tên liên hệ (Contact Name)
- URL

## 🔧 Advanced Usage

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --website {nhatot,muaban,batdongsan,all}
                        Website to crawl (default: all)
  --headless            Run in headless mode
  --use-profile         Use existing Chrome profile
  --help                Show help message
```

### Resume Functionality

The scraper automatically saves progress and can resume from the last processed page:

- Resume files are stored in `output/` directory
- Format: `resume_<website>.txt`
- Contains the last processed page number

### Anti-Detection Features

- **User Agent Rotation**: Randomly selects from multiple user agents
- **Random Delays**: Variable delays between requests
- **WebDriver Stealth**: Removes automation indicators
- **Scroll Simulation**: Mimics human browsing behavior

## 🛠️ Development

### Adding New Websites

1. Create a new crawler class inheriting from `BaseCrawler`
2. Implement required abstract methods
3. Add website configuration to `config.py`
4. Update the main script to include the new crawler

### Example New Crawler

```python
from .base_crawler import BaseCrawler

class NewWebsiteCrawler(BaseCrawler):
    def __init__(self, headless=False, use_profile=False):
        super().__init__("new_website", headless, use_profile)
    
    def get_item_elements(self):
        # Return list of item elements
        pass
    
    def extract_item_data(self):
        # Extract and return data dictionary
        pass
    
    def wait_for_listing_page(self):
        # Wait for listing page to reload
        pass
```

## 📝 Logging

The scraper provides detailed logging:

- Progress updates for each page
- Error messages with context
- Success confirmations for each item
- Resume status updates

## ⚠️ Important Notes

### Legal and Ethical Considerations

- **Respect robots.txt**: Check website robots.txt files
- **Rate Limiting**: Built-in delays to avoid overwhelming servers
- **Terms of Service**: Ensure compliance with website ToS
- **Data Usage**: Use scraped data responsibly and legally

### Technical Considerations

- **ChromeDriver**: Ensure ChromeDriver version matches your Chrome browser
- **Memory Usage**: Large datasets may require significant memory
- **Network**: Stable internet connection recommended
- **Storage**: Ensure sufficient disk space for output files

## 🐛 Troubleshooting

### Common Issues

**ChromeDriver Issues:**
```bash
# Update ChromeDriver
# Download from: https://chromedriver.chromium.org/
```

**Permission Errors:**
```bash
# Make main.py executable
chmod +x main.py
```

**Import Errors:**
```bash
# Ensure you're in the project directory
cd real-estate-scraper
python main.py
```

### Getting Help

1. Check the logs for error messages
2. Verify ChromeDriver compatibility
3. Ensure all dependencies are installed
4. Check network connectivity

## 📈 Performance Tips

- Use `--headless` mode for better performance
- Adjust delays in `config.py` based on your needs
- Monitor system resources during large crawls
- Consider running crawlers separately for different websites

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with website terms of service and applicable laws.

## 🔗 Links

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/)
- [Web Scraping Best Practices](https://blog.apify.com/web-scraping-best-practices/)

---

**Disclaimer**: This tool is for educational purposes only. Users are responsible for ensuring compliance with website terms of service and applicable laws.
