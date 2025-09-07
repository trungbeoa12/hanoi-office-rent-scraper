#!/usr/bin/env python3
"""
Demo script to test the Real Estate Web Scraper
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from crawlers.nhatot_crawler import NhatotCrawler

def demo_nhatot():
    """Demo Nhà Tốt crawler with limited pages"""
    print("🏠 Demo: Nhà Tốt Crawler")
    print("=" * 50)
    
    try:
        # Create crawler instance
        crawler = NhatotCrawler(headless=True, use_profile=False)
        
        # Override the start method to limit to 1 page for demo
        original_start = crawler.start
        
        def limited_start():
            try:
                crawler.driver = crawler.driver_manager.create_driver()
                crawler.wait = crawler.driver_manager.wait
                
                print("Starting demo crawl (1 page only)...")
                
                # Crawl only page 1
                if crawler.crawl_page(1):
                    print("✅ Demo completed successfully!")
                else:
                    print("❌ No data found on page 1")
                    
            except Exception as e:
                print(f"❌ Demo error: {e}")
            finally:
                crawler.driver_manager.close()
        
        # Run limited demo
        limited_start()
        
    except Exception as e:
        print(f"❌ Failed to initialize crawler: {e}")

if __name__ == "__main__":
    print("🚀 Real Estate Web Scraper - Demo")
    print("This demo will crawl 1 page from Nhà Tốt")
    print("Press Ctrl+C to stop at any time\n")
    
    try:
        demo_nhatot()
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
    
    print("\n📊 Check the 'output/' directory for results")
    print("📖 See README.md for full usage instructions")
