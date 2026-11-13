# MatchEngine 
Welcome to the documentation for the matchengine! The Matchengine is a system designed to match cancer patients to genomically driven clinical trials using Clinical Trial Markup Language (CTML) and patient clinical and genomic data. It utilizes the the MatchminerAPI and MatchminerUI for displaying trial match information.


The matchengine can be used on local instances that provide access to private data. If you are interested in the development of new features, or in setting up a local instance of the MatchMiner system, please see the documentation, or contact [matchminer@dfci.harvard.edu](https://app.gitbook.com/@matchminer/s/matchminer)

# Documentation
[Gitbook documentation](https://matchminer.gitbook.io/matchminer/matchengine-v2/introduction)

# Requirements
* Python 3.10 or newer (CI runs 3.10–3.13)
* MongoDB 4.0 or newer (PyMongo 4.x dropped support for MongoDB 3.6); CI runs MongoDB 7.0

## Optional connection settings
In addition to the existing `SECRETS_JSON` keys, these optional keys are supported:

| Key | Default | Purpose |
|---|---|---|
| `MONGO_TLS` | `false` | Adds `tls=true` to the connection URI |
| `MONGO_RETRY_WRITES` | unset | Adds `retryWrites=<value>` to the connection URI |

For Azure Cosmos DB for MongoDB, set `MONGO_TLS` to `true` and `MONGO_RETRY_WRITES` to `false`. Usernames and passwords are URL-encoded automatically.

# Running tests
```bash
docker run -d --name matchengine-mongo -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=password mongo:7.0
docker run --rm --network host -v "$PWD/matchengine/tests/data/integration_data:/dump:ro" mongo:7.0 \
  mongorestore --uri "mongodb://root:password@localhost:27017/?authSource=admin" --db integration --gzip --dir /dump
pip install . pytest
SECRETS_JSON='{"MONGO_HOST": "localhost", "MONGO_PORT": 27017, "MONGO_USERNAME": "root", "MONGO_PASSWORD": "password", "MONGO_RO_USERNAME": "root", "MONGO_RO_PASSWORD": "password", "MONGO_DBNAME": "integration", "MONGO_AUTH_SOURCE": "admin"}' \
  python -m pytest matchengine/tests
```
