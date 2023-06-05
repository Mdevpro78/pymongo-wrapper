<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./logo.png" alt="Project logo"></a>
</p>

<h3 align="center">Pymongo Wrapper</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Few lines describing your project.
    <br> 
	This Python Package called PyMongo Wrapper wrapp the Pymongo python package for projects which are schemaless
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About

PyMongo Wrapper provides a simple wrapper around pymongo which is providing CRUD functionality on the MongoDB
when we don't have Schema (Schemaless)

## 🏁 Getting Started 

### Prerequisites

What things you need to install the software and how to install them.

```bash
git clone https://github.com/Mdevpro78/pymongo-wrapper.git
```

### Installing

A step by step series to install the package

```bash
cd pymongo-wrapper
```

```bash
python setup.py install
```

or just

```bash
pip install .
```

## 🎈 Usage 

### for Python Project

#### to build Db Repository

```bash
from repository import DBRepository

collection_name = 'my_collection'
database_name = 'my_database'
uri = 'mongodb://localhost:27017/'

db_repo = DBRepository(collection_name, database_name, uri)

```

#### To build Pipeline

```bash
# Instantiate the pipeline builder
builder = PipelineBuilder()

# Add a $match stage
builder.match({'name': 'John'})

# Add a $project stage
builder.project({'name': 1, 'age': 1})

# Add a $group stage
builder.group(['name'], count={'$sum': 1})

# Add a $sort stage
builder.sort([('count', -1), ('name', 1)])

# Add a $skip stage
builder.skip(10)

# Add a $limit stage
builder.limit(5)

# Add a $unwind stage
builder.unwind('$tags')

# Build the pipeline
pipeline = builder.build()

```

#### Example

```
# Example usage of query_repo()
query_repo = db_repo.query_repo()
results = query_repo.aggregate(pipeline)
for result in results:
    print(result)

```

## ⛏️ Built Using 

- [MongoDB](https://www.mongodb.com/) - MongoDB
- [Django](https://www.djangoproject.com/) - Django
- [PyMongo](https://pymongo.readthedocs.io/en/stable/index.html) - MongoDB python Driver

## ✍️ Authors 

- [@MdevPro](https://github.com/Mdevpro78/pymongo-wrapper)
