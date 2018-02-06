# Setting up ElasticSearch

* [Official Install Guide for Elasticsearch 6.1](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)
* [Elasticsearch install guide for Ubuntu 16.04 - DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-16-04)
* [ElasticSearch with Django the easy way - freeCodeCamp](https://medium.freecodecamp.org/elasticsearch-with-django-the-easy-way-909375bc16cb)

1. Confirm Java version with `java -version`.
2. `wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -` - Download and install public signing key.
3. `sudo apt-get install apt-transport-https` - Install prerequisite.
4. `echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list` - Save the repository definition.
5. `sudo apt-get update` - Update package indexes.
6. `sudo apt-get install elasticsearch` - Install Elasticsearch.
7. `sudo systemctl enable elasticsearch.service` - Enable Elasticsearch as a service and to make it start with the server and stop with it.
8. `sudo systemctl start elasticsearch.service` - Start the Elasticsearch service for the first time.
9. `curl -XGET http://localhost:9200` - Run after a minute to let Elasticsearch start; shows JSON response of details of the server configuration to confirm it's working.
10. `sudo vim /etc/elasticsearch/elasticsearch.yml` - Edit the Elasticsearch configuration file to match these lines:
    ```
    cluster.name: ParatureSearchCluster
    node.name: ParatureSearchNode
    ```
11. `sudo systemctl restart elasticsearch.service` - Restart the Elasticsearch service.
12. `curl -XGET 'http://localhost:9200/_nodes?pretty'` - A verbose JSON listing of Elasticsearch settings.

## Bulk Indexing

[Elasticsearch docs - Tune for indexing speed](https://www.elastic.co/guide/en/elasticsearch/reference/master/tune-for-indexing-speed.html)

To start bulk indexing, first set Elasticsearch settings to be optimized for that.

In Ubuntu, disable swapfile usage with `sudo swapoff -a`.

Create an index named `customer-index` with settings configured for bulk indexing:

```
curl -XPUT 'localhost:9200/customer-index?pretty' -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "number_of_shards" : 5,
        "number_of_replicas" : 0,
        "refresh_interval": "-1"
    }
}
'
```

On an existing index, run this to temporarily change the Elasticsearch settings for bulk indexing:

```
curl -XPUT 'localhost:9200/customer-index/_settings?pretty' -H 'Content-Type: application/json' -d'
{
    "index" : {
        "refresh_interval" : "-1",
		"number_of_replicas": "0"
    }
}
'
```

After Bulk Indexing is done and Elasticsearch should get back to the job of searching, run this command to revert settings to those optimal for searching:

```
curl -XPUT 'localhost:9200/customer-index/_settings?pretty' -H 'Content-Type: application/json' -d'
{
    "index" : {
        "refresh_interval" : "1s",
		"number_of_replicas": "1"
    }
}
'
```

To delete an index:

```
curl -XDELETE 'localhost:9200/customer-index?pretty'
```
