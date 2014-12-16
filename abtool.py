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

def import_budget(options):
    print options
    assert options.filename
    assert options.country_code
    assert options.budget_type
    projects.import_budget(options)

def import_iati_xml(options):
    print options
    assert options.filename
    assert options.country_code
    download.parse_file(options.country_code, options.filename)

def setup(options):
    print options
    assert options.lang
    absetup.setup(options.lang)

def setup(options):
    absetup.setup("FR")
    download.parse_file("SN", "CA-3-SN.xml")    

commands = {
    "quicksetup": (setup, "Quick Setup with default arguments"),
    "setup": (setup, "Setup"),
    "import": (import_iati_xml, "Import IATI XML file"),
    "update-projects": (update_projects, "Update projects"),
    "import-budget": (import_budget, "Import CC-budget mapping"),
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
    p.add_option("--budget-type", dest="budget_type",
                 help="Set type of budget for importing (a, f)")

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
