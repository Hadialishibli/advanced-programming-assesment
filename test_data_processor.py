import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from data_processor import load_data, get_data_summary

class TestDataProcessor(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Latitude,Longitude\n51.5,-0.12\n51.51,-0.13")
    @patch("pandas.read_csv")
    def test_load_data(self, mock_read_csv, mock_file):
        mock_read_csv.return_value = pd.DataFrame({
            'Latitude': [51.5, 51.51],
            'Longitude': [-0.12, -0.13]
        })

        data = load_data("data\On_Street_Crime_In_Camden.csv")
        self.assertEqual(len(data), 2)
        self.assertIn('Latitude', data.columns)
        self.assertIn('Longitude', data.columns)

    @patch("pandas.read_csv", side_effect=Exception("File not found"))
    def test_load_data_failure(self, mock_read_csv):
        with self.assertRaises(Exception) as context:
            load_data("data\On_Street_Crime_In_Camden.csv")
        self.assertTrue("Failed to load data" in str(context.exception))

    def test_get_data_summary(self):
        data = pd.DataFrame({
            'Latitude': [51.5, 51.51],
            'Longitude': [-0.12, -0.13]
        })

        summary = get_data_summary(data)
        self.assertEqual(summary['num_entries'], 2)
        self.assertEqual(summary['lat_range'], (51.5, 51.51))
        self.assertEqual(summary['lon_range'], (-0.13, -0.12))

    def test_get_data_summary_failure(self):
        data = pd.DataFrame({
            'Latitude': ['invalid', 51.51],
            'Longitude': [-0.12, 'invalid']
        })

        with self.assertRaises(Exception) as context:
            get_data_summary(data)
        self.assertTrue("Failed to summarize data" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
