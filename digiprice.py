#!/usr/bin/env python
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

      priceQuotes = [] # [[quantity, unitPrice], ...]
      for item in result['items']:
        priceQuotes = priceQuotes + item['offers'][0]['prices']['USD']
      if options.debugging:
        print "Seller: %s" % item['offers'][0]['seller']['name']
      priceQuotes.sort(key=lambda x: x[1]) # find lowest price
      price = priceQuotes[0][1]
      quantity = priceQuotes[0][0]
      if quantity >= 1000:
        retultsTable += "%s \t $%s \t @ \t %sk  \n" % (partNumbers[idx], price, quantity/1000)
      else:
        retultsTable += "%s \t $%s \t @ \t %s  \n" % (partNumbers[idx], price, quantity)

  print retultsTable

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
  main()