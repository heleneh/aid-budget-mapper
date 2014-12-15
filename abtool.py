#!/usr/bin/env python

import optparse, sys
from abmapper import projects
from abmapper.datastore import download
from abmapper import setup as absetup

def update_projects(options):
    print options
    assert options.filename
    assert options.reporting_org
    assert options.country_code
    projects.update_project(options)

def import_iati_xml(options):
    print options
    assert options.filename
    assert options.country_code
    download.parse_file(options.country_code, options.filename)

def setup(options):
    print options
    assert options.lang
    absetup.setup(options.lang)

commands = {
    "setup": (setup, "Setup"),
    "import": (import_iati_xml, "Import IATI XML file"),
    "update_projects": (update_projects, "Update projects"),
}

def main():
    p = optparse.OptionParser()

    for k, v in commands.iteritems():
        handler, help_text = v
        option_name = "--" + k.replace("_", "-")
        p.add_option(option_name, dest=k, action="store_true", default=False, help=help_text)
    
    p.add_option("--reporting-org", dest="reporting_org",
                 help="Set reporting org for projects to update")
    p.add_option("--country-code", dest="country_code",
                 help="Set country code for projects to update")
    p.add_option("--filename", dest="filename",
                 help="Set filename of data to update")
    p.add_option("--lang", dest="lang",
                 help="Set language for setup")

    options, args = p.parse_args()

    for mode, handler_ in commands.iteritems():
        handler, _ = handler_
        if getattr(options, mode, None):
            handler(options)
            return
    
    usage()

def usage():
    print "You need to specify which mode to run under"
    sys.exit(1)

if __name__ == '__main__':
    main()
