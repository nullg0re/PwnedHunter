#!/usr/bin/env python3

import re
import time
import argparse
from core.hunter import Hunter
from core.scraper import Scraper
from core.transformer import Transformer
from core.haveibeenpwned import PwnHunter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape employee names from search engine LinkedIn profiles. Convert employee names to a specified username format. Check identified email address against HaveIBeenPwned.")

    # Allow a user to scrape names or just convert an already generated list of names
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--company", type=str, help="Target company to search for LinkedIn profiles (e.g. 'Example Ltd.').")
    parser.add_argument("-D", "--domain",  type=str, help="Domain name of target company for Hunter.io email format identification and email scraping.")
    parser.add_argument("-a", "--api",     type=str, help="Hunter.io API key.")
    parser.add_argument("-d", "--depth",   type=int, help="Number of pages to search each search engine. Default: 5", default=5)
    parser.add_argument("-t", "--timeout", type=int, help="Specify request timeout. Default: 25", default=25)
    parser.add_argument("-o", "--output",  type=str, help="Directory to write username files to.")
    parser.add_argument("-f", "--format",  type=str, help="Username format if not using Hunter.IO")
    parser.add_argument("--cookie",        type=str, help="File containing Google CAPTCHA bypass cookies")
    parser.add_argument("--proxy",         type=str, help="Proxy to pass traffic through: <ip:port>")
    parser.add_argument("--lower",         action="store_true", help="Force usernames to all lower case.")
    parser.add_argument("--upper",         action="store_true", help="Force usernames to all upper case.")
    parser.add_argument("--debug",         action="store_true", help="Enable debug output.")
    args = parser.parse_args()

    start  = time.time()
    output = args.output if args.output else "./"

    if args.company:
        scraper = Scraper(args.company, cookies=args.cookie, depth=args.depth, timeout=args.timeout, proxy=args.proxy)
        scraper.loop.run_until_complete(scraper.run())
        print("\n\n[+] Names Found: %d" % len(scraper.employees))
        print("[*] Writing names to the following directory: %s" % output)
        with open("%s/names.txt" % (output), 'a') as f:
            for name in scraper.employees:
                f.write("%s\n" % name)

    # Only get format from Hunter.io if API key and domain are set
    if args.api and args.domain:
        hunter = Hunter(args.domain, api_key=args.api, timeout=args.timeout, proxy=args.proxy)
        if not args.format:
            _format = hunter.hunt_format()
            print("[*] Using Hunter.io username format")

        else:
            _format = args.format

    else:
        _format = args.format if args.format else None

    if _format:
        print("[*] Converting found names to: %s" % _format)
        transform = Transformer(args.debug)
        usernames = {f.strip(): set() for f in _format.split(',')}
        for template in usernames.keys():
            if any(t[1:-1] not in ["first","middle","last",'f','m','l'] for t in re.findall(r'\{.+?\}', template)):
                print("[!] Invalid username format: %s" % (template))
                usernames.pop(template, None) # Remove invalid template

            else:
                names = scraper.employees if args.company else open(args.file, 'r').readlines()
                if args.upper or args.lower:
                    names = [name.lower() for name in names] if args.lower else [name.upper() for name in names]

                for name in names:
                    try:
                        usernames[template].add(transform.transform(name, template, usernames[template]))
                        # Handle hyphenated last names
                        if '-' in name:
                            name = name.split()
                            nm   = ' '.join(n for n in name[:-1])
                            for ln in name[-1].split('-'):
                                _nm = "%s %s" % (nm, ln)
                                usernames[template].add(transform.transform(_nm, template, usernames[template]))

                    except IndexError as e:
                        print("[!] Name Error: %s" % name)
                        pass

        # Gather emails from Hunter.io
        # We only need to account for a single format here since we are using Hunter.io's format
        if args.api and args.domain:
            hunter.hunt_emails()
            print("[+] Hunter.io identified %d emails." % len(hunter.emails))
            for email in hunter.emails:
                usernames[_format].add(email)

    print("[+] Number of unique usernames gathered: %d" % sum(len(usernames[t]) for t in usernames.keys()))

    if _format:
        full_list = []
        if any(len(usernames[t]) > 0 for t in usernames.keys()):
            print("[*] Querying usernames against HaveIBeenPwned API [*]\r\n\r\n")
            for template in usernames.keys():
               for username in usernames[template]:
                  full_list.append(username)
        PwnHunter(full_list)

    elapsed = time.time() - start
    if args.debug: print("\n[DEBUG] %s executed in %0.4f seconds." % (__file__, elapsed))
