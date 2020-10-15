# -*- coding: utf-8 -*-
import os
from datetime import datetime

import pandas as pd
import requests

from zvt import zvt_env
from zvt.contract.api import df_to_db
from zvt.contract.recorder import Recorder
from zvt.utils.time_utils import to_time_str, TIME_FORMAT_DAY
from zvt.utils.zip_utils import unzip
from zvt_future import get_future_name
from zvt_future.domain import Future, Future1dKdata


class ExchangeFutureMetaRecorder(Recorder):
    provider = 'exchange'
    data_schema = Future

    def run(self):
        self.download_history_data()

    def download_history_data(self):
        zip_files = []
        for the_year in range(2009, datetime.today().year):
            the_zip_file = os.path.join(self.get_tmp_dir(), f'{the_year}_shfe_history_data.zip')
            zip_files.append(the_zip_file)

            if not os.path.exists(the_zip_file):
                resp = requests.get(self.get_year_k_data_url(the_year))
                if resp.headers.get('content-type') == 'application/zip':
                    with open(the_zip_file, "wb") as f:
                        f.write(resp.content)
                        f.flush()
                        self.logger.info(f'{the_zip_file} finished')

        # persist them to db
        for the_zip_file in zip_files:

            dst_dir = the_zip_file.replace('.zip', "")
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            # 文件名编码有问题
            unzip(the_zip_file, dst_dir)
            files = [os.path.join(dst_dir, f) for f in
                     os.listdir(dst_dir) if f.endswith('.xls')
                     ]

            for the_file in files:
                self.logger.info("parse {}".format(the_file))

                df = pd.read_excel(the_file, skiprows=2, skip_footer=4, index_col='合约', converters={'日期': str})
                df.index = pd.Series(df.index).fillna(method='ffill')
                df = df.loc[:,
                     ['日期', '前收盘', '前结算', '涨跌1', '涨跌2', '开盘价', '最高价', '最低价', '收盘价', '结算价', '成交量', '成交金额',
                      '持仓量']]
                df.columns = ['timestamp', 'pre_close', 'pre_settlement', 'change', 'change1', 'open', 'high',
                              'low', 'close', 'settlement', 'volume', 'turnover',
                              'interest']

                df['turnover'] = df['turnover'] * 1000

                unique_index = df.index.drop_duplicates()

                for contract_code in unique_index:
                    self.logger.info("start handling {} in {}".format(contract_code, the_file))
                    entity_id = 'future_{}_{}'.format('shfe', contract_code)

                    entity = Future.query_data(provider=self.provider, ids=[entity_id], return_type='domain')

                    # 检查是否需要保存合约meta
                    try:
                        name = get_future_name(contract_code)
                    except:
                        self.logger.warning(f'not support contract:{contract_code}')
                        continue

                    if not entity:
                        entity = Future(id=entity_id, name=name, entity_type='future',
                                        exchange='shfe', code=contract_code)

                        self.session.add(entity)
                        self.session.commit()

                    the_df = df.loc[contract_code, :].copy()

                    def generate_kdata_id(se):
                        return "{}_{}".format(se['entity_id'], to_time_str(se['timestamp'], fmt=TIME_FORMAT_DAY))

                    the_df['code'] = contract_code
                    the_df['timestamp'] = pd.to_datetime(the_df['timestamp'], format='%Y%m%d')
                    the_df['provider'] = self.provider
                    the_df['level'] = '1d'
                    the_df['name'] = name
                    the_df['entity_id'] = entity_id
                    the_df['id'] = the_df[['entity_id', 'timestamp']].apply(generate_kdata_id, axis=1)
                    the_df['change_pct'] = the_df['change'] / the_df['pre_close']
                    the_df['change_pct1'] = the_df['change1'] / the_df['pre_settlement']
                    df_to_db(df=the_df, data_schema=Future1dKdata, provider=self.provider)

    def get_tmp_dir(self):
        return zvt_env['tmp_path']

    def get_year_k_data_url(self, the_year):
        return 'http://www.shfe.com.cn/historyData/MarketData_Year_{}.zip'.format(the_year)

    def get_day_kdata_url(self, the_date):
        return 'http://www.shfe.com.cn/data/dailydata/kx/kx{}.dat'.format(the_date)

    def get_day_inventory_url(self, the_date):
        return 'http://www.shfe.com.cn/data/dailydata/kx/pm{}.dat'.format(the_date)

    def get_trading_date_url(self):
        return 'http://www.shfe.com.cn/bourseService/businessdata/calendar/20171201all.dat'


if __name__ == '__main__':
    r = ExchangeFutureMetaRecorder()
    r.run()

# the __all__ is generated
__all__ = ['ExchangeFutureMetaRecorder']
