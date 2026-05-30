from pathlib import Path

import pandas as pd

from src.data_loader import load_sales_data


def test_load_sales_data(tmp_path: Path):
    sample = (
        'Order_ID,Customer_Name,Age,Email,Phone,Region,Product_Category,Product_Name,Quantity,Unit_Price,Total_Price,Order_Date,Payment_Method,Status,Rating\n'
        'ORD001,Test User,30,test@example.com,9999999999,North,Books,Programming Guide,4,610,2440,2024-04-05,Credit Card,Delivered,4.5\n'
    )
    file_path = tmp_path / 'raw_sales_data-1.csv'
    file_path.write_text(sample)

    df = load_sales_data(file_path)
    assert df.shape[0] == 1
    assert df.loc[0, 'Revenue'] == 2440
    assert df.loc[0, 'Order_Date'].month == 4
    assert round(df.loc[0, 'Average_Order_Value'], 2) == 610.0


def test_load_sales_data_drops_duplicate_order_ids(tmp_path: Path):
    sample = (
        'Order_ID,Customer_Name,Age,Email,Phone,Region,Product_Category,Product_Name,Quantity,Unit_Price,Total_Price,Order_Date,Payment_Method,Status,Rating\n'
        'ORD001,First User,30,first@example.com,9999999999,North,Books,Guide,2,500,1000,2024-04-05,Credit Card,Delivered,4.0\n'
        'ORD001,Duplicate User,35,dup@example.com,9999999998,North,Books,Guide,2,500,1000,2024-04-05,Credit Card,Delivered,4.0\n'
    )
    file_path = tmp_path / 'raw_sales_data-1.csv'
    file_path.write_text(sample)

    df = load_sales_data(file_path)
    assert df.shape[0] == 1
    assert df['Order_ID'].nunique() == 1
