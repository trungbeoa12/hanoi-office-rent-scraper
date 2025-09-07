# 📊 Output Data Samples

This directory contains sample output data from the real estate web scraper.

## 📁 Files

### Demo Files (Small samples for demonstration)
- `demo_nhatot.csv` - Sample data from Nhà Tốt (5 rows)
- `demo_muaban.csv` - Sample data from MuaBan.net (5 rows)  
- `demo_batdongsan.csv` - Sample data from BatDongSan.com.vn (5 rows)

### Full Output Files (Complete datasets)
- `output_nhatot.com.csv` - Complete Nhà Tốt dataset
- `output_muaban.net.csv` - Complete MuaBan.net dataset
- `output_batdongsan.com.csv` - Complete BatDongSan dataset

## 📋 Data Structure

### Nhà Tốt & MuaBan.net
| Field | Description |
|-------|-------------|
| Tiêu đề | Property title |
| Text chi tiết | Detailed description |
| URL | Property listing URL |

### BatDongSan.com.vn
| Field | Description |
|-------|-------------|
| Tiêu đề | Property title |
| Địa chỉ | Property address |
| Mức giá | Price range |
| Diện tích | Area in square meters |
| Mặt tiền | Frontage width |
| Số tầng | Number of floors |
| Số phòng tắm, vệ sinh | Number of bathrooms |
| Tiện ích | Amenities |
| Mô tả | Property description |
| Ngày đăng | Posting date |
| Ngày hết hạn | Expiry date |
| Loại tin | Post type |
| Mã tin | Post ID |
| SĐT liên hệ | Contact phone |
| Tên liên hệ | Contact name |
| URL | Property listing URL |

## 🚀 Usage

These files are generated when you run the scraper:

```bash
# Generate new data
python main.py --website nhatot
python main.py --website muaban  
python main.py --website batdongsan

# Or run all websites
python main.py
```

## 📈 Statistics

- **Nhà Tốt**: ~2.8MB of data
- **MuaBan.net**: ~559KB of data  
- **BatDongSan**: ~1.8MB of data

*Note: File sizes may vary based on the amount of data scraped.*
