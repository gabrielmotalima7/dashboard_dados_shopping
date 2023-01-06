from datetime import datetime, date
import pandas as pd
from typing import Dict, List


def read_flow_data(path: str) -> pd.DataFrame:
    flow_data = pd.read_csv(path, index_col=0, parse_dates=[0])
    return flow_data


def read_shopping_info(path: str) -> pd.DataFrame:
    shopping_location_info = pd.read_excel(path, index_col="Nome")
    return shopping_location_info


def set_time_col(flow_data: pd.DataFrame):
    flow_data["time"] = flow_data.index
    flow_data["time"] = flow_data["time"].apply(lambda x: x.replace(day=1, month=1, year=2000))


class GlobalShoppingData:

    def __init__(self, flow_data: pd.DataFrame, shopping_info: pd.DataFrame):
        set_time_col(flow_data)
        self._flow_data = flow_data
        self._shopping_info = shopping_info[shopping_info.index.isin(flow_data.keys())]

    @property
    def flow_data(self) -> pd.DataFrame:
        return self._flow_data.copy()

    @property
    def shopping_info(self) -> pd.DataFrame:
        return self._shopping_info.copy()

    def get_shopping_names(self) -> List[str]:
        return list(self._shopping_info.index.unique())

    def get_city_names(self) -> List[str]:
        return list(self._shopping_info["Cidade"].unique())

    def get_state_names(self) -> List[str]:
        return list(self._shopping_info["Estado"].unique())

    def get_class_names(self) -> List[str]:
        return list(self._shopping_info["Classe"].unique())

    def get_shoppings_from_state(self, state_name: str) -> List[str]:
        return list(self._shopping_info[self._shopping_info["Estado"] == state_name].index)

    def get_shoppings_from_class(self, class_name: str) -> List[str]:
        shoppings_from_class = self._shopping_info[self._shopping_info["Classe"] == class_name].index
        return list(shoppings_from_class)
    
    def get_shoppings_by_city(self) -> Dict:
        city_to_shoppings = {
            city: list(self._shopping_info[self._shopping_info["Cidade"] == city].index) 
            for city in self.get_city_names()}
        return city_to_shoppings

    def get_shoppings_in_cities(self, city_names: List[str]) -> List[str]:
        shoppings_in_city = self._shopping_info[self._shopping_info["Cidade"].isin(city_names)].index
        return list(shoppings_in_city)

    def get_cities_in_state(self, state_name: str) -> List[str]:
        city_names = self._shopping_info[self._shopping_info["Estado"] == state_name]["Cidade"].unique()
        return list(city_names)

    def get_min_date(self) -> date:
        return self._flow_data.index.min()

    def get_max_date(self) -> date:
        return self._flow_data.index.max()

    def shopping_to_city(self) -> Dict:
        shopping_names = self.get_shopping_names()
        shopping_to_city = {
            shopping: self._shopping_info["Cidade"][shopping] for shopping in shopping_names
        }
        return shopping_to_city

    def city_to_state(self) -> Dict:
        city_names = self.get_city_names()
        city_to_state = {
            city: self._shopping_info[self._shopping_info["Cidade"] == city]["Estado"].values[0] for city in city_names
        }
        return city_to_state

    def get_flow_by_city(self) -> pd.DataFrame:
        flow_data = self._flow_data
        city_to_shopping = self.get_shoppings_by_city()
        flow_by_city = pd.DataFrame({
            city: flow_data[city_to_shopping[city]].sum(axis=1) for city in city_to_shopping
        }, index=flow_data.index)
        return flow_by_city

    def get_flow_by_state(self) -> pd.DataFrame:
        flow_by_city = self.get_flow_by_city()
        flow_by_state = flow_by_city.groupby(self.city_to_state(), axis=1).sum()
        return flow_by_state

    def get_flow_by_city_in_state(self, state_name: str) -> pd.DataFrame:
        flow_by_city_in_state = self.get_flow_by_city()[self.get_cities_in_state(state_name)]
        return flow_by_city_in_state

    @classmethod
    def create_data_holder_from_files(cls, flow_data_path: str, shopping_info_path: str):
        flow_data = read_flow_data(flow_data_path)
        shopping_info_path = read_shopping_info(shopping_info_path)
        return GlobalShoppingData(flow_data, shopping_info_path)


class FilteredShoppingData:

    def __init__(self, global_data: GlobalShoppingData):
        self._filtered_flow_data = global_data.flow_data
        self._max_date = global_data.get_max_date()
        self._min_date = global_data.get_min_date()
        self._global_data = global_data

    def set_interest_shoppings(self, shoppings_list: List[str]):
        self._filtered_flow_data = self._filtered_flow_data[shoppings_list + ["time"]]

    def set_date_bounds(self, min_date: datetime, max_date: datetime):
        self._min_date = min_date
        self._max_date = max_date
        self._filtered_flow_data = self._filtered_flow_data[self._filtered_flow_data.index >= min_date]
        self._filtered_flow_data = self._filtered_flow_data[self._filtered_flow_data.index <= max_date]

    def get_average_flow_by_time_interval(self, time_interval: float) -> pd.DataFrame:
        flow_by_interval = self._filtered_flow_data.groupby(pd.Grouper(key="time", freq=f"{time_interval}H")).mean(numeric_only=True)
        return flow_by_interval

    def get_flow_by_day(self):
        flow_by_month = self._filtered_flow_data.groupby(pd.Grouper(level=0, freq="D")).sum(numeric_only=True)
        return flow_by_month

    def get_average_flow_by_week_day(self) -> pd.DataFrame:
        day_of_week = pd.Series(self._filtered_flow_data.index,
                                index=self._filtered_flow_data.index).dt.dayofweek
        flow_by_week_day = self._filtered_flow_data.groupby(day_of_week).mean()
        return flow_by_week_day

    def get_flow_by_month(self):
        flow_by_month = self._filtered_flow_data.groupby(pd.Grouper(level=0, freq="BM")).sum(numeric_only=True)
        return flow_by_month

    def get_flow_by_quarter(self):
        flow_by_quarter = self._filtered_flow_data.groupby(pd.Grouper(level=0, freq="BQ")).sum(numeric_only=True)
        return flow_by_quarter

    def get_flow_series(self) -> pd.DataFrame:
        return self._filtered_flow_data.drop(columns="time", axis=1, inplace=False)

    def get_variacao_media_com_relacao_a_media(self, time_interval) -> pd.DataFrame:
        avg_flow_by_time_interval = self.get_average_flow_by_time_interval(time_interval)
        variacao = avg_flow_by_time_interval - avg_flow_by_time_interval.mean()
        return variacao

    def get_aggregate_flow(self) -> pd.DataFrame:
        flow_sum = self.get_flow_series().sum()
        return flow_sum / flow_sum.max()

    def get_flow_by_city_in_state(self, state_name: str) -> pd.DataFrame:
        flow_by_city_in_state = self._global_data.get_flow_by_city_in_state(state_name)
        flow_by_city_in_state = flow_by_city_in_state[flow_by_city_in_state.index <= self._max_date]
        flow_by_city_in_state = flow_by_city_in_state[flow_by_city_in_state.index >= self._min_date]
        return flow_by_city_in_state

    def get_flow_by_state(self) -> pd.DataFrame:
        flow_by_state = self._global_data.get_flow_by_state()
        flow_by_state = flow_by_state[flow_by_state.index <= self._max_date]
        flow_by_state = flow_by_state[flow_by_state.index >= self._min_date]
        return flow_by_state

    @classmethod
    def create_filtered_data(cls, global_data: GlobalShoppingData, shoppings: List[str], min_date: datetime, max_date: datetime):
        filtered_data = FilteredShoppingData(global_data)
        filtered_data.set_interest_shoppings(shoppings)
        filtered_data.set_date_bounds(min_date, max_date)
        return filtered_data
