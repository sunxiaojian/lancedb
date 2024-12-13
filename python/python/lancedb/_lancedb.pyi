from typing import Dict, List, Optional, Tuple

import pyarrow as pa

class Connection(object):
    uri: str
    async def table_names(
        self, start_after: Optional[str], limit: Optional[int]
    ) -> list[str]: ...
    async def create_table(
        self,
        name: str,
        mode: str,
        data: pa.RecordBatchReader,
        storage_options: Optional[Dict[str, str]] = None,
        data_storage_version: Optional[str] = None,
        enable_v2_manifest_paths: Optional[bool] = None,
    ) -> Table: ...
    async def create_empty_table(
        self,
        name: str,
        mode: str,
        schema: pa.Schema,
        storage_options: Optional[Dict[str, str]] = None,
        data_storage_version: Optional[str] = None,
        enable_v2_manifest_paths: Optional[bool] = None,
    ) -> Table: ...
    async def rename_table(self, old_name: str, new_name: str) -> None: ...
    async def drop_table(self, name: str) -> None: ...

class Table:
    def name(self) -> str: ...
    def __repr__(self) -> str: ...
    async def schema(self) -> pa.Schema: ...
    async def add(self, data: pa.RecordBatchReader, mode: str) -> None: ...
    async def update(self, updates: Dict[str, str], where: Optional[str]) -> None: ...
    async def count_rows(self, filter: Optional[str]) -> int: ...
    async def create_index(self, column: str, config, replace: Optional[bool]): ...
    async def version(self) -> int: ...
    async def checkout(self, version): ...
    async def checkout_latest(self): ...
    async def restore(self): ...
    async def list_indices(self) -> List[IndexConfig]: ...
    def query(self) -> Query: ...
    def vector_search(self) -> VectorQuery: ...

class IndexConfig:
    index_type: str
    columns: List[str]

async def connect(
    uri: str,
    api_key: Optional[str],
    region: Optional[str],
    host_override: Optional[str],
    read_consistency_interval: Optional[float],
) -> Connection: ...

class RecordBatchStream:
    def schema(self) -> pa.Schema: ...
    async def next(self) -> Optional[pa.RecordBatch]: ...

class Query:
    def where(self, filter: str): ...
    def select(self, columns: Tuple[str, str]): ...
    def limit(self, limit: int): ...
    def offset(self, offset: int): ...
    def nearest_to(self, query_vec: pa.Array) -> VectorQuery: ...
    def nearest_to_text(self, query: dict) -> FTSQuery: ...
    async def execute(self, max_batch_legnth: Optional[int]) -> RecordBatchStream: ...

class FTSQuery:
    def where(self, filter: str): ...
    def select(self, columns: List[str]): ...
    def limit(self, limit: int): ...
    def offset(self, offset: int): ...
    def fast_search(self): ...
    def with_row_id(self): ...
    def postfilter(self): ...
    def nearest_to(self, query_vec: pa.Array) -> HybridQuery: ...
    async def execute(self, max_batch_length: Optional[int]) -> RecordBatchStream: ...
    async def explain_plan(self) -> str: ...

class VectorQuery:
    async def execute(self) -> RecordBatchStream: ...
    def where(self, filter: str): ...
    def select(self, columns: List[str]): ...
    def select_with_projection(self, columns: Tuple[str, str]): ...
    def limit(self, limit: int): ...
    def offset(self, offset: int): ...
    def column(self, column: str): ...
    def distance_type(self, distance_type: str): ...
    def postfilter(self): ...
    def refine_factor(self, refine_factor: int): ...
    def nprobes(self, nprobes: int): ...
    def bypass_vector_index(self): ...
    def nearest_to_text(self, query: dict) -> HybridQuery: ...

class HybridQuery:
    def where(self, filter: str): ...
    def select(self, columns: List[str]): ...
    def limit(self, limit: int): ...
    def offset(self, offset: int): ...
    def fast_search(self): ...
    def with_row_id(self): ...
    def postfilter(self): ...
    def distance_type(self, distance_type: str): ...
    def refine_factor(self, refine_factor: int): ...
    def nprobes(self, nprobes: int): ...
    def bypass_vector_index(self): ...
    def to_vector_query(self) -> VectorQuery: ...
    def to_fts_query(self) -> FTSQuery: ...
    def get_limit(self) -> int: ...
    def get_with_row_id(self) -> bool: ...

class CompactionStats:
    fragments_removed: int
    fragments_added: int
    files_removed: int
    files_added: int

class RemovalStats:
    bytes_removed: int
    old_versions_removed: int

class OptimizeStats:
    compaction: CompactionStats
    prune: RemovalStats
