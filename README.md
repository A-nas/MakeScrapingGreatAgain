# web bot to scrape data from twitter profils.

## Steps

* clone this repo into a new project folder

```bash
$ git clone https://github.com/A-nas/MakeScrapingGreatAgain.git
$ cd MakeScrapingGreatAgain
```

* navigate to directory and run the following command :

```bash
$ scrapy crawl trumpSpider -a profileName=<profileName> -a since=<StartDate> -a until=<EndDate> -s MONGODB_COLLECTION=<CollectionName> 
```
example to collect data from Emmanuel Macron's profile

```bash
$ scrapy crawl trumpSpider -a profileName=EmmanuelMacron -a since=2009-03-01 -a until=2017-11-03 -s MONGODB_COLLECTION='EmmanuelMacron' 
```

the database name is hard-coded in setting.py file, feel free to change it
