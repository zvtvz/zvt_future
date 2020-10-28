# -*- coding: utf-8 -*-
import pandas as pd
from jqdatapy import get_all_securities

from zvt.contract.api import get_entity_exchange, get_entity_code, df_to_db
from zvt.contract.recorder import Recorder
from zvt_future.domain import Future


class JqChinaFutureRecorder(Recorder):
    data_schema = Future
    provider = 'joinquant'

    def to_zvt_entity(self, df, entity_type, category=None):
        df = df.set_index('code')
        df.index.name = 'entity_id'
        df = df.reset_index()
        # 上市日期
        df.rename(columns={'start_date': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['list_date'] = df['timestamp']
        df['end_date'] = pd.to_datetime(df['end_date'])

        df['entity_id'] = df['entity_id'].apply(lambda x: self.to_entity_id(entity_type=entity_type, jq_code=x))
        df['id'] = df['entity_id']
        df['entity_type'] = entity_type
        df['exchange'] = df['entity_id'].apply(lambda x: get_entity_exchange(x))
        df['code'] = df['entity_id'].apply(lambda x: get_entity_code(x))
        df['name'] = df['display_name']

        if category:
            df['category'] = category

        return df

    def to_entity_id(self, jq_code: str, entity_type):
        # 聚宽交易所代码
        # 交易市场	代码后缀	示例代码	证券简称
        # 上海证券交易所	.XSHG	'600519.XSHG'	贵州茅台
        # 深圳证券交易所	.XSHE	'000001.XSHE'	平安银行
        # 中金所	.CCFX	'IC9999.CCFX'	中证500主力合约
        # 大商所	.XDCE	'A9999.XDCE'	豆一主力合约
        # 上期所	.XSGE	'AU9999.XSGE'	黄金主力合约
        # 郑商所	.XZCE	'CY8888.XZCE'	棉纱期货指数
        # 上海国际能源期货交易所	.XINE	'SC9999.XINE'	原油主力合约
        code, exchange = jq_code.split('.')
        if exchange == 'XSGE':
            exchange = 'shfe'
        elif exchange == 'XZCE':
            exchange = 'czce'
        elif exchange == 'XDCE':
            exchange = 'dce'
        elif exchange == 'CCFX':
            exchange = 'cffex'

        return f'{entity_type}_{exchange}_{code}'

    def run(self):
        # 抓取股票列表
        df_stock = self.to_zvt_entity(get_all_securities(code='futures'), entity_type='future')
        df_to_db(df_stock, data_schema=self.data_schema, provider=self.provider, force_update=self.force_update)

        # self.logger.info(df_stock)
        self.logger.info("persist future list success")


if __name__ == '__main__':
    JqChinaFutureRecorder().run()
# the __all__ is generated
__all__ = ['JqChinaFutureRecorder']