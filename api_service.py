from api_client import APIClient
import json
api_client = APIClient('admin', 'admin')

from enum import Enum
from typing import List, Optional

DefaultPageSize = 5

class Operators(Enum):
  LESS_THAN = 'lt',
  GREATER_THAN = 'gt',
  LESS_THAN_OR_EQUALS = 'lte',
  GREATER_THAN_OR_EQUALS = 'gte',
  EQUAL = 'eq',
  NOT_EQUAL = 'nq',
  CONTAINS = 'cn',
  NOT_CONTAINS = 'nc',
  STARTS_WITH = 'sw',
  ENDS_WITH = 'ew',
  IN = 'in',
  NOT_IN = 'ni',
    # Add other operator values here if necessary

class FilterOption:
    def __init__(self, value: str, property: str = "Id", operator: Operators = Operators.EQUAL, is_case_sensitive: bool = False):
        self.value = value
        self.property = property
        self.operator = operator
        self.isCaseSensitive = is_case_sensitive

class FilterModel:
    def __init__(self, filters: Optional[List[FilterOption]] = None, sort_field: str = "Id", page_size: int = DefaultPageSize, sort_descending: bool = False):
      self.pageNumber = 0
      self.sortField = sort_field
      self.pageSize = page_size
      self.sortDescending = sort_descending
      self.filters = filters or []
        
    def get_payload(self):
      payload = {
        "pageNumber": self.pageNumber,
        "sortField": self.sortField,
        "pageSize": self.pageSize,
        "sortDescending": self.sortDescending
        }
      if self.filters:
          payload["filters"] = [vars(filter_option) for filter_option in self.filters]
      return payload


# def get_filter(**kwargs):
  

def get_asset_detail(filter: FilterModel):
  return api_client.post_req('/Asset/GetAllForBasicDetail', data=filter.get_payload())