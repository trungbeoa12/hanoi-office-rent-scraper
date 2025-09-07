#!/usr/bin/env python3
"""
Real Estate Web Scraper - Main Script
Crawls real estate data from multiple Vietnamese websites
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from crawlers.nhatot_crawler import NhatotCrawler
from crawlers.muaban_crawler import MuabanCrawler
from crawlers.batdongsan_crawler import BatDongSanCrawler


def main():
    parser = argparse.ArgumentParser(description="Real Estate Web Scraper")
    parser.add_argument(
        "--website", 
        choices=["nhatot", "muaban", "batdongsan", "all"],
        default="all",
        help="Website to crawl (default: all)"
    )
    parser.add_argument(
        "--headless", 
        action="store_true",
        help="Run in headless mode"
    )
    parser.add_argument(
        "--use-profile", 
        action="store_true",
        help="Use existing Chrome profile"
    )
    
    args = parser.parse_args()
    
    crawlers = {
        "nhatot": NhatotCrawler,
        "muaban": MuabanCrawler,
        "batdongsan": BatDongSanCrawler
    }
    
    if args.website == "all":
        websites_to_crawl = list(crawlers.keys())
    else:
        websites_to_crawl = [args.website]
    
    for website in websites_to_crawl:
        print(f"\n{'='*50}")
        print(f"Starting crawler for {website.upper()}")
        print(f"{'='*50}")
        
        try:
            crawler = crawlers[website](
                headless=args.headless,
                use_profile=args.use_profile
            )
            crawler.start()
            print(f"✅ Successfully completed {website}")
            
        except KeyboardInterrupt:
            print(f"\n⚠️ Crawling interrupted by user for {website}")
            break
        except Exception as e:
            print(f"❌ Error crawling {website}: {e}")
            continue
    
    print(f"\n{'='*50}")
    print("Crawling session completed!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
