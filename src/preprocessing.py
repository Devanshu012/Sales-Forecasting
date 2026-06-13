import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

logger = logging.getLogger(__name__)


class FillOpenMedian(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.open_median_ = X['Open'].median()
        logger.info("[FillOpenMedian] fit — Open column median: %s", self.open_median_)
        return self

    def transform(self, X):
        X = X.copy()
        missing = int(X['Open'].isna().sum())
        if missing:
            logger.warning("[FillOpenMedian] filling %d missing Open values with median %s", missing, self.open_median_)
        else:
            logger.info("[FillOpenMedian] transform — no missing Open values found")
        X['Open'] = X['Open'].fillna(self.open_median_)
        return X


class PromoFeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        logger.info("[PromoFeatureEngineer] engineering promo features — input shape: %s", X.shape)
        X = X.copy()

        X['Promo2StartDate'] = pd.to_datetime(
            X['Promo2SinceYear'].fillna(0).astype(int).astype(str)
            + X['Promo2SinceWeek'].fillna(0).astype(int).astype(str)
            + '1',
            format='%G%V%u',
            errors='coerce'
        )

        X['Promo2SinceDays'] = (X['Date'] - X['Promo2StartDate']).dt.days
        X['Promo2SinceDays'] = X['Promo2SinceDays'].fillna(0).clip(lower=0)
        X['PromoInterval'] = X['PromoInterval'].fillna('no_promo2')

        logger.debug("[PromoFeatureEngineer] done — output shape: %s", X.shape)
        return X


class CompetitionFeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.competition_distance_mean_ = X['CompetitionDistance'].mean()
        return self

    def transform(self, X):
        logger.info("[CompetitionFeatureEngineer] engineering competition features — input shape: %s", X.shape)
        X = X.copy()

        missing = int(X['CompetitionDistance'].isna().sum())
        if missing:
            logger.warning(
                "[CompetitionFeatureEngineer] filling %d missing CompetitionDistance values with training mean", missing
            )
        X['CompetitionDistance'] = X['CompetitionDistance'].fillna(self.competition_distance_mean_)

        X['CompetitionOpenDate'] = pd.to_datetime(
            dict(
                year=X['CompetitionOpenSinceYear'],
                month=X['CompetitionOpenSinceMonth'],
                day=1
            ),
            errors='coerce'
        )
        X['CompetitionOpenSinceDays'] = (X['Date'] - X['CompetitionOpenDate']).dt.days
        X['CompetitionOpenSinceDays'] = X['CompetitionOpenSinceDays'].fillna(0).clip(lower=0)

        logger.debug("[CompetitionFeatureEngineer] done — output shape: %s", X.shape)
        return X


class DateFeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        logger.info("[DateFeatureEngineer] extracting Year and Month from Date — input shape: %s", X.shape)
        X = X.copy()
        X['Year'] = X['Date'].dt.year
        X['Month'] = X['Date'].dt.month
        logger.debug("[DateFeatureEngineer] done — output shape: %s", X.shape)
        return X


class DropColumnsTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        cols_to_drop = [
            'CompetitionOpenSinceYear',
            'CompetitionOpenSinceMonth',
            'CompetitionOpenDate',
            'Promo2SinceYear',
            'Promo2SinceWeek',
            'Promo2StartDate',
            'Date'
        ]
        existing_cols = [c for c in cols_to_drop if c in X.columns]
        logger.info("[DropColumnsTransformer] dropping %d columns: %s", len(existing_cols), existing_cols)
        return X.drop(columns=existing_cols)
