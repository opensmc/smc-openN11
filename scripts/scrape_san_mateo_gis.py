"""
So, this requires lxml, argparse, and requests. Install it from standard
via pip into a virtualenv and everything will go right. Maybe.

Usage:

python scrape_san_mateo_gis.py 003417220 --outfile out.json

It requires an APN and an --outfile, which puts things out into
a JSON file.

To use it in the case of inputing a file, and then printing out to the
screen and to the file:

python scripts/scrape_san_mateo_gis.py 003417220 --outfile out.json --input testfile.html --pretty_print

I haven't extensively tested this, so it might break on some files.

"""


import re
import json
import lxml.html
import logging
import requests
import argparse

URL = ('http://gis.co.sanmateo.ca.us/countygis/applications/'
       'gisapp_PropReviewMap.asp')
HEADER_XPATH = './/td[@class="textBlackBoldExtraSmall"]/text()'
DATA_XPATH = './/td[@class="textBlackPlainExtraSmall"]/text()'


def get_html_text(input, apn):
    """
    If we have an input file, get the data from the input file.
    If not grab it from the website via the APN.
    """
    raw_text = None
    if input is None:
        params = {'APN': apn, 'querytype': 'APNReview'}
        url = URL.format(apn)
        session = requests.Session()
        req = session.get(url, params=params)
        return req.text
    # If we have an input file, grab from it.
    with open(input, 'r') as f:
        return f.read()


def run(outfile, apn, input=None, pretty_print=False):
    """
    Grab the HTML and then run it through some
    lxml.html twisting.
    """

    raw_text = get_html_text(apn=apn, input=input)
    html = lxml.html.fromstring(raw_text)
    total_data = {}

    # First grab the results from every table.
    for table_entry in html.xpath('.//tr'):
        header_res = table_entry.xpath(HEADER_XPATH)
        data_res = table_entry.xpath(DATA_XPATH)
        if len(header_res) != 1 or len(data_res) != 1:
            # Nothing here
            continue
        if not ':' in header_res[0]:
            # Not sure what to do here
            continue
        key = header_res[0].replace(':', '').strip()
        total_data[key] = data_res[0].strip()

    total_data['links'] = []
    for link_entry in html.xpath('.//a[@target="_blank"]'):
        href = link_entry.attrib.get('href')
        total_data['links'].append(href)

    # Get the owner
    try:
        owner = raw_text.split(
            'Owner:'
        )[1].split('</TD>')[1].split('>')[1]
        total_data['Owner'] = owner
    except Exception as ex:
        logging.error('Error parsing for owner in APN {}'.format(apn))
        pass

    if outfile:
        with open(outfile, 'w') as f:
            json.dump(total_data, f)

    if pretty_print:
        # Use the magic of JSON indentation.
        print(
            json.dumps(
                total_data,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape GIS for SMC')
    parser.add_argument('apn', type=str, help='Single APN to parse')
    parser.add_argument('--outfile', type=str, help='Output JSON file')
    parser.add_argument('--input', type=str,
                        help='Optional input file holding html')
    parser.add_argument('--pretty_print', action='store_true',
                        help='Print the JSON output', default=False)
    args = parser.parse_args()
    run(outfile=args.outfile, input=args.input,
        apn=args.apn, pretty_print=args.pretty_print)
