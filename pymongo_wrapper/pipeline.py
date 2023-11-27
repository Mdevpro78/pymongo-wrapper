"""
A pipeline builder module for MongoDB that allows users to construct a sequence of aggregation stages.

The PipelineBuilder class provides methods that correspond to the various stages in an aggregation pipeline, such as match, project, group, sort, skip, and limit. These methods can be chained together to create a custom pipeline that meets the user's specific needs.

Example usage:

builder = PipelineBuilder()

pipeline = builder.match({'status': 'active'}) \
                .group(['category', {'month': {'$month': '$timestamp'}}], total={'$sum': '$amount'}) \
                .sort([('total', -1)]) \
                .limit(10) \
                .build()

The resulting pipeline will find all records with status 'active', group them by category and month, compute the total amount for each group, sort the results in descending order by total, and return only the top 10 results.
"""

from typing import List, Dict, Any, Union, Tuple


class PipelineBuilder:
    """
    Methods:
        build(): returns the list of aggregation stages built so far.
        match(query: Dict[str, Any]) -> 'PipelineBuilder': adds a $match stage to the pipeline with the given query.
        project(fields: Dict[str, Union[int, str]]) -> 'PipelineBuilder': adds a $project stage to the pipeline with the given fields.
        group(groupby: List[Union[str, Dict[str, Any]]], **kwargs) -> 'PipelineBuilder': adds a $group stage to the pipeline with the given groupby fields and optional kwargs.
        sort(sortby: Union[List[Tuple[str, int]], Tuple[str, int]]) -> 'PipelineBuilder': adds a $sort stage to the pipeline with the given sorting criteria.
        skip(n: int) -> 'PipelineBuilder': adds a $skip stage to the pipeline that skips the first n documents.
        limit(n: int) -> 'PipelineBuilder': adds a $limit stage to the pipeline that limits the number of returned documents to n.
        unwind(field: dict) -> 'PipelineBuilder': adds a $unwind stage to the pipeline that splits an array field into separate documents.
    """
    
    def __init__(self):
        self.pipeline = []

    def build(self) -> List[Dict[str, Any]]:

        return self.pipeline

    def match(self, query: Dict[str, Any]) -> 'PipelineBuilder':
        self.pipeline.append({'$match': query})
        return self

    def project(self, fields: Dict[str, Union[int, str]]) -> 'PipelineBuilder':
        self.pipeline.append({'$project': fields})
        return self

    def group(self, groupby: List[Union[str, Dict[str, Any]]], **kwargs) -> 'PipelineBuilder':
        group_stage = {'_id': {}}
        for field in groupby:
            if isinstance(field, str):
                group_stage['_id'][field] = f'${field}'
            elif isinstance(field, dict):
                for key, value in field.items():
                    group_stage['_id'][key] = value
        group_stage.update(kwargs)
        self.pipeline.append({'$group': group_stage})
        return self

    def sort(self, sortby: Union[List[Tuple[str, int]], Tuple[str, int]]) -> 'PipelineBuilder':
        if isinstance(sortby, tuple):
            sortby = [sortby]
        sort_dict = dict(sortby)
        self.pipeline.append({'$sort': sort_dict})
        return self

    def skip(self, n: int) -> 'PipelineBuilder':
        self.pipeline.append({'$skip': n})
        return self

    def limit(self, n: int) -> 'PipelineBuilder':
        self.pipeline.append({'$limit': n})
        return self

    def unwind(self, field: dict) -> 'PipelineBuilder':
        self.pipeline.append({'$unwind': field})
        return self

