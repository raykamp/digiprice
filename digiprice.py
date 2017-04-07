#!/usr/bin/env python2.7
import sys
import optparse
import json
import urllib

# Semantic Versioning: Major, Minor, Patch
VERSION = (0, 0, 1)
MAX_QUERY_ITEMS = 20

def main():
  usage = "usage: %prog [options] partNumber ..."
  versionString = "%d.%d.%d" % VERSION
  p = optparse.OptionParser(usage=usage, version="%prog "+versionString)
  p.add_option('--apikey', '-a', default="3f3a679e", help="Octopart API key")
  p.add_option('--distributor', '-d', default="Digi-Key")
  p.add_option('--strict', '-s', action="store_true", dest="strict", help="Part number must match results exactly")
  p.add_option('--verbose', '-v', action="store_true", dest="verbose")
  p.add_option('--debugging', action="store_true", dest="debugging")
  options, arguments = p.parse_args()

  if len(arguments) < 1:
    print "Enter at least one part number"
    sys.exit(0)

  # We can only process so many part numbers at a time
  partNumberBatches = list(chunks(arguments, MAX_QUERY_ITEMS))

  retultsTable = ""

  for partNumbers in partNumberBatches:
    # Build a query for the Octopart API
    if options.strict:
      querykey = "mpn"
    else:
      querykey = "q"

    queries = []
    for partNumber in partNumbers:
      queries.append({querykey: partNumber,'seller' : options.distributor })
      
    url = 'http://octopart.com/api/v3/parts/match?queries=%s' % urllib.quote(json.dumps(queries))
    url += "&apikey=%s" % options.apikey
    url += "&limit=3"
    url += "&sortby=%s" % urllib.quote('avg_price asc, score desc')

    if options.verbose:
      print "Query URL: %s" % url

    data = urllib.urlopen(url).read()
    response = json.loads(data)

    if options.debugging:
      print "Query response: %s" % json.dumps(response)

    if not 'results' in response:
      print "Query failed:"
      if 'message' in response:
        print response.message
      sys.exit(0)

    if options.verbose:
      print 'Respone time: %s ms' % response['msec']

    for idx, result in enumerate(response['results']):
      if len(result['items']) == 0:
        retultsTable += "%s \t No results found \n" % partNumbers[idx]
        continue

      quotes = [] # [[quantity, unitPrice], ...]
      for item in result['items']:
        for offer in item['offers']:
          for price in offer['prices']['USD']:
            quantity = price[0]
            price = price[1]
            quote = {'quantity': quantity ,'price': price ,'mpn': str(item['mpn'])}
            quotes.append(quote)
          break # For now, only take the first seller offer (Digi-Key). There's a bug with the API that prevents specifying the seller
      if options.debugging:
        print "Seller: %s" % item['offers'][0]['seller']['name']
      quotes.sort(key=lambda x: x['price']) # find lowest price
      if quantity >= 1000:
        retultsTable += "%s \t $%s \t @ \t %sk  \n" % (quotes[0]['mpn'], quotes[0]['price'], quotes[0]['quantity']/1000)
      else:
        retultsTable += "%s \t $%s \t @ \t %s  \n" % (quotes[0]['mpn'], quotes[0]['price'], quotes[0]['quantity'])

  print retultsTable

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
  main()