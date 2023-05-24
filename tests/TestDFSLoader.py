import unittest
from unittest.mock import patch
from src.DFSLoader import DFSLoader


class TestDFSLoader(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada prueba
        self.prints_file = "./local/prints.json"
        self.taps_file = "./local/taps.json"
        self.pays_file = "./local/pays.csv"
        self.loader = DFSLoader(self.prints_file, self.taps_file, self.pays_file)

    # Test get_prints por cantidad de registros
    def test_get_prints(self):
        df_prints = self.loader.get_prints()
        self.assertEqual(len(df_prints), 508617)

    # Test get_prints_last_week por cantidad de registros
    def test_get_prints_last_week(self):
        df_prints = self.loader.get_prints()
        df_prints_last_week = self.loader.get_prints_last_week(df_prints)
        self.assertEqual(len(df_prints_last_week), 7)

    # Test get_taps por cantidad de registros
    def test_get_taps(self):
        df_taps = self.loader.get_taps()
        self.assertEqual(len(df_taps), 50859)

    # Test get_payss por cantidad de registros
    def test_get_pays(self):
        df_pays = self.loader.get_pays()
        self.assertEqual(len(df_pays), 756483)

    # Test get_prints por archivo no encontrado
    @patch('pandas.read_json')
    def test_get_prints_file_not_found(self, mock_read_json):
        mock_read_json.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.loader.get_prints()

    # Test get_taps por exception
    @patch('pandas.read_json')
    def test_get_taps_exception(self, mock_read_json):
        self.loader.taps_file = "FNF_taps.json"
        with self.assertRaises(Exception):
            self.loader.get_taps()

    # Test get_pays por archivo no encontrado
    @patch('pandas.read_json')
    def test_get_pays_file_not_found(self, mock_read_json):
        self.loader.pays_file = "FNF_pays.csv"
        with self.assertRaises(FileNotFoundError):
            self.loader.get_pays()

    # Test get_pays por exception
    @patch('pandas.read_json')
    def test_get_pays_exception(self, mock_read_json):
        self.loader.pays_file = "FNF_taps.json"
        with self.assertRaises(Exception):
            self.loader.get_pays()


if __name__ == '__main__':
    unittest.main()
