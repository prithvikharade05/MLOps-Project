import ccxt
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import DataPoint
from utils.config import settings
import logging

logger = logging.getLogger(__name__)

class BinanceCollector:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_SECRET,
            'sandbox': False,
            'enableRateLimit': True,
        })
    
    def fetch_ohlcv(self, timeframe='1h', limit=1000) -> pd.DataFrame:
        """Fetch BTC/USDT OHLCV data from Binance"""
        ohlcv = self.exchange.fetch_ohlcv('BTC/USDT', timeframe, limit=limit)
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        logger.info(f"Fetched {len(df)} candles from {df['timestamp'].min()} to {df['timestamp'].max()}")
        return df
    
    def save_to_db(self, df: pd.DataFrame, db: Session):
        """Save raw OHLCV to database (features added later)"""
        existing_timestamps = {dp.timestamp for dp in db.query(DataPoint.timestamp).all()}
        
        new_data = []
        for _, row in df.iterrows():
            ts = row['timestamp']
            if ts not in existing_timestamps:
                new_data.append(DataPoint(
                    timestamp=ts,
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume']
                ))
        
        if new_data:
            db.add_all(new_data)
            db.commit()
            logger.info(f"Saved {len(new_data)} new data points")
        else:
            logger.info("No new data to save")

collector = BinanceCollector()

