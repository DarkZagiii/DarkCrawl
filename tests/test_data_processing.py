import unittest
from web.app import DataProcessor

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.raw_data = [
            {
                'url': 'https://example.com/laptop1',
                'title': 'Laptop 1',
                'description': 'Description of laptop 1',
                'content': 'This is a great laptop for gaming and work.',
                'images': [{'url': 'https://example.com/image1.jpg'}],
                'links': ['https://example.com/link1'],
            },
            {
                'url': 'https://example.com/laptop2',
                'title': 'Laptop 2',
                'description': 'Description of laptop 2',
                'content': 'This laptop is perfect for students and professionals.',
                'images': [{'url': 'https://example.com/image2.jpg'}],
                'links': ['https://example.com/link2'],
            },
            # Add more mock products as needed
        ]

    def test_process_raw_data(self):
        processed_data = DataProcessor.process_raw_data(self.raw_data)
        self.assertEqual(len(processed_data['products']), 2)
        self.assertIn('Elektronik', processed_data['categories'])
        self.assertGreater(processed_data['statistics']['total_images'], 0)

    def test_top_stores(self):
        # Implement logic to test for top stores based on processed data
        pass

if __name__ == '__main__':
    unittest.main()
