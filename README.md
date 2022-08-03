# PwnedHunter

Scrape employee names from search engine LinkedIn profiles.

Convert to email format with Hunter.IO.

Lookup Identified emails against HaveIBeenPwned.

## Requirements

HaveIBeenPwned API Key

Hunter.io API Key

### Usage

```
$ python3 PwnedHunter.py --help
usage: PwnedHunter.py [-h] -c COMPANY [-D DOMAIN] [-a API] [-d DEPTH] [-t TIMEOUT] [-o OUTPUT] [--cookie COOKIE] [--proxy PROXY] [--lower] [--upper] [--debug]

Scrape employee names from search engine LinkedIn profiles. Convert employee names to a specified username format. Check identified email address against HaveIBeenPwned.

options:
  -h, --help            show this help message and exit

  -c COMPANY, --company COMPANY    Target company to search for LinkedIn profiles (e.g. 'Example Ltd.').

  -D DOMAIN, --domain DOMAIN       Domain name of target company for Hunter.io email format identification and email scraping.

  -a API, --api API                Hunter.io API key.

  -d DEPTH, --depth DEPTH          Number of pages to search each search engine. Default: 5

  -t TIMEOUT, --timeout TIMEOUT    Specify request timeout. Default: 25

  -o OUTPUT, --output OUTPUT       Directory to write username files to.

  --cookie COOKIE       File containing Google CAPTCHA bypass cookies

  --proxy PROXY         Proxy to pass traffic through: <ip:port>

  --lower               Force usernames to all lower case.

  --upper               Force usernames to all upper case.

  --debug               Enable debug output.
```

### Examples

Gather employee names and email addresses from search engines and Hunter.io:<br>
`$ python3 PwnedHunter.py --company "Example Ltd." --domain example.com --api {API_KEY} --depth 10 --output example-employees/ --debug`

### Features

* Support for three major search engines: Google, Bing, and Yahoo
* Name parsing to strip LinkedIn titles, certs, prefixes, etc.
* Search engine blacklist evasion
* Proxying
* Username formatting with support for trickier username formats
  * Name trimming
    * e.g. If a username format has only the first 4 characters of the last name
  * Hyphenated last name handling
  * Duplicate username handling
    * Incrementing numbers appended to duplicate usernames
* Use Hunter.io to identify the email format for a specified domain and pull down any known emails for that domain
* Use HaveIBeenPwned API to identify previously compromised credentials

### Contributers

[0xZDH](https://github.com/0xZDH) - Literally all the logic from [BridgeKeeper](https://github.com/0xZDH/BridgeKeeper)

### Acknowledgements

**m8r0wn** - [CrossLinked](https://github.com/m8r0wn/CrossLinked)<br>
**initstring** - [linkedin2username](https://github.com/initstring/linkedin2username)
