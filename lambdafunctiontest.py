import unittest
from unittest.mock import MagicMock, patch
from incrementViewCount import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('incrementViewCount.boto3.resource')
    @patch('incrementViewCount.table')
    def test_lambda_handler(self, mock_table, mock_dynamodb_resource):
       
        mock_table_instance = MagicMock()
        mock_table.return_value = mock_table_instance
        mock_dynamodb_resource.return_value = MagicMock()

        mock_table_instance.get_item.return_value = {'Item': {'ID': '1', 'views': 42}}
        mock_table_instance.update_item.return_value = {'Attributes': {'views': 43}}

        result = lambda_handler({}, {})
        self.assertEqual(result, 43)

        mock_table_instance.get_item.assert_called_once_with(Key={'ID': '1'})

        mock_table_instance.update_item.assert_called_once_with(
            Key={'ID': '1'},
            UpdateExpression='SET #v = :val',
            ExpressionAttributeNames={'#v': 'views'},
            ExpressionAttributeValues={':val': 43}
        )

if __name__ == '__main__':
    unittest.main()