from pathlib import Path

import pandas as pd

from src.data_loader import load_sales_data


def test_load_sales_data(tmp_path: Path):
    sample = (
        'Order_ID,Date,Product_Name,Category,Region,Salesperson,Units_Sold,Unit_Price,Discount_%,Revenue,Cost,Profit,Customer_Name,Customer_Segment,Payment_Method\n'
        'ORD001,01-01-2024,Notebook,Stationery,North,Rohan Mehta,5,100,0,500,300,200,Client A,B2B,Credit Card\n'
    )
    file_path = tmp_path / 'sales_revenue_dataset.csv'
    file_path.write_text(sample)

    df = load_sales_data(file_path)
    assert df.shape[0] == 1
    assert df.loc[0, 'Revenue'] == 500
    assert round(df.loc[0, 'Profit_Margin_%'], 2) == 40.0
