import pandas as pd
import unittest
from src.do_result import do_result
import io


class TestDoResult(unittest.TestCase):
    def setUp(self):
        # Crea datos de ejemplo para las pruebas
        # prints_lw
        prints_lw_data = '''{"day":"2020-11-24","value_prop":"credits_consumer","user_id":69553}
                {"day":"2020-11-24","value_prop":"prepaid","user_id":69553}
                {"day":"2020-11-25","value_prop":"cellphone_recharge","user_id":69553}
                {"day":"2020-11-25","value_prop":"prepaid","user_id":69553}
                {"day":"2020-11-26","value_prop":"transport","user_id":69553}
                {"day":"2020-11-26","value_prop":"prepaid","user_id":69553}
                {"day":"2020-11-27","value_prop":"transport","user_id":70909}
                {"day":"2020-11-27","value_prop":"prepaid","user_id":70909}
                {"day":"2020-11-28","value_prop":"point","user_id":34758}
                {"day":"2020-11-28","value_prop":"prepaid","user_id":34758}
                {"day":"2020-11-29","value_prop":"credits_consumer","user_id":34758}
                {"day":"2020-11-29","value_prop":"prepaid","user_id":34758}
                {"day":"2020-11-30","value_prop":"link_cobro","user_id":34758}
                {"day":"2020-11-30","value_prop":"prepaid","user_id":34758}
                '''
        self.df_prints_lw = pd.read_json(io.StringIO(prints_lw_data), lines=True)
        self.df_prints_lw['day'] = pd.to_datetime(self.df_prints_lw['day'])
        self.df_prints_last_week = []
        for _, partition in self.df_prints_lw.groupby(pd.Grouper(key="day")):
            self.df_prints_last_week.append(partition)

        # prints
        prints_data = '''{"day":"2020-11-01","value_prop":"cellphone_recharge","user_id":98702}
                {"day":"2020-11-02","value_prop":"prepaid","user_id":98702}
                {"day":"2020-11-03","value_prop":"prepaid","user_id":63252}
                {"day":"2020-11-04","value_prop":"cellphone_recharge","user_id":24728}
                {"day":"2020-11-05","value_prop":"link_cobro","user_id":24728}
                {"day":"2020-11-06","value_prop":"credits_consumer","user_id":24728}
                {"day":"2020-11-07","value_prop":"point","user_id":24728}
                {"day":"2020-11-08","value_prop":"point","user_id":25517}
                {"day":"2020-11-09","value_prop":"credits_consumer","user_id":25517}
                {"day":"2020-11-10","value_prop":"transport","user_id":25517}
                {"day":"2020-11-11","value_prop":"point","user_id":57587}
                {"day":"2020-11-12","value_prop":"transport","user_id":13609}
                {"day":"2020-11-13","value_prop":"cellphone_recharge","user_id":3708}
                {"day":"2020-11-14","value_prop":"prepaid","user_id":3708}
                {"day":"2020-11-15","value_prop":"point","user_id":3708}
                {"day":"2020-11-16","value_prop":"send_money","user_id":3708}
                {"day":"2020-11-17","value_prop":"send_money","user_id":99571}
                {"day":"2020-11-18","value_prop":"point","user_id":99571}
                {"day":"2020-11-19","value_prop":"link_cobro","user_id":99571}
                {"day":"2020-11-20","value_prop":"prepaid","user_id":53823}
                {"day":"2020-11-21","value_prop":"credits_consumer","user_id":31394}
                {"day":"2020-11-22","value_prop":"prepaid","user_id":31394}
                {"day":"2020-11-23","value_prop":"point","user_id":69553}
                {"day":"2020-11-24","value_prop":"credits_consumer","user_id":69553}
                {"day":"2020-11-25","value_prop":"cellphone_recharge","user_id":69553}
                {"day":"2020-11-26","value_prop":"transport","user_id":69553}
                {"day":"2020-11-27","value_prop":"transport","user_id":70909}
                {"day":"2020-11-28","value_prop":"point","user_id":34758}
                {"day":"2020-11-29","value_prop":"credits_consumer","user_id":34758}
                {"day":"2020-11-30","value_prop":"link_cobro","user_id":34758}
                '''
        self.df_prints = pd.read_json(io.StringIO(prints_data), lines=True)
        self.df_prints['day'] = pd.to_datetime(self.df_prints['day'])

        # Taps
        taps_data = '''{"day":"2020-11-01","value_prop":"cellphone_recharge","user_id":98702}
                {"day":"2020-11-01","value_prop":"point","user_id":3708}
                {"day":"2020-11-01","value_prop":"send_money","user_id":3708}
                {"day":"2020-11-01","value_prop":"transport","user_id":93963}
                {"day":"2020-11-01","value_prop":"cellphone_recharge","user_id":93963}
                {"day":"2020-11-01","value_prop":"link_cobro","user_id":94945}
                {"day":"2020-11-01","value_prop":"cellphone_recharge","user_id":94945}
                {"day":"2020-11-01","value_prop":"prepaid","user_id":89026}
                {"day":"2020-11-01","value_prop":"link_cobro","user_id":7616}
                {"day":"2020-11-01","value_prop":"link_cobro","user_id":63471}
                '''
        self.df_taps = pd.read_json(io.StringIO(taps_data), lines=True)
        self.df_taps['day'] = pd.to_datetime(self.df_taps['day'])
        self.df_taps["clicked"] = 'Y'

        # pays
        pays_data = '''pay_date,total,user_id,value_prop
                2020-11-01,7.04,35994,link_cobro
                2020-11-01,37.36,79066,cellphone_recharge
                2020-11-01,15.84,19321,cellphone_recharge
                2020-11-01,26.26,19321,send_money
                2020-11-01,35.35,38438,send_money
                2020-11-01,20.95,85939,transport
                2020-11-01,74.48,14372,prepaid
                2020-11-01,31.52,14372,link_cobro
                2020-11-01,83.76,65274,transport
                '''
        self.df_pays = pd.read_csv(io.StringIO(pays_data), sep=",")
        self.df_pays['pay_date'] = pd.to_datetime(self.df_pays['pay_date'])

    def test_do_result(self):
        # Columnas esperadas en el resultado
        expected_columns = ['day', 'value_prop', 'user_id',  'clicked', 'print_count', 'tap_count', 'pay_count',
                            'pay_amount']
        df_result = do_result(self.df_prints_last_week, self.df_prints, self.df_taps, self.df_pays)
        print(len(df_result))
        # Espera que el resultado sea un DF
        self.assertIsInstance(df_result, pd.DataFrame)
        # Espera que el resultado tenga la lista de columnas mencionadas en expected_columns
        self.assertEqual(df_result.columns.tolist(), expected_columns)
        # Espera que el df tenga 14 registros
        self.assertEqual(len(df_result), 14)
        # Espera que el df tenga info para los 7dias
        self.assertEqual(len(df_result['day'].unique()), 7)


if __name__ == '__main__':
    unittest.main()
