import csv
import json
import os

from django.core.management.base import BaseCommand

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ID_CORRECTIONS = {
    "-1": "afit.edu",
    "skylinecollege.net": "skylinecollege.edu",
    "yahoo.com": "jordanlocke.edu",
}
OVERRIDES = {
    "kumc_edu": "ku_edu",
    "onid_oregonstate_edu": "oregonstate_edu",
    "bus_oregonstate_edu": "oregonstate_edu",
    "onid_edu_oregonstate_edu": "oregonstate_edu",
    "science_oregonstate_edu": "oregonstate_edu",
    "science_orst_edu": "oregonstate_edu",
    "onid_orst_edu": "oregonstate_edu",
    "orst_edu": "oregonstate_edu",
    "student_unsw_edu_au": "unsw_edu_au",
    "u_washington_edu": "washington_edu",
    "uni_sydney_edu_au": "sydney_edu_au",
    "unsw_edu_au": "unsw_edu_au",
    "uw_edu": "washington_edu",
    "zmail_unsw_edu_au": "unsw_edu_au",
    "smccd_edu": "my_smccd_edu",
}
KNOWN_CAMPUSES = {
    "buddyup_org": {
        "us_gov_id": 0,
        "name": "BuddyUp U",
        "city": "Portland",
        "state": "OR",
        "country": "US",
        "postal_code": "97207",
        "website": "buddyup.org",
        "edu_address": "buddyup_org",
        "id": "buddyup_org",
    },
    "hudson_edu": {
        "us_gov_id": 0,
        "name": "Hudson University",
        "city": "Neverneverland",
        "state": "WY",
        "country": "US",
        "postal_code": "81234",
        "website": "hudson.edu",
        "edu_address": "hudson_edu",
        "id": "hudson_edu",
    },
    "sydney_edu_au": {
        "us_gov_id": 0,
        "name": "University of Sydney",
        "city": "Sydney",
        "state": "NSW",
        "country": "AU",
        "postal_code": "2006",
        "website": "sydney.edu.au",
        "edu_address": "sydney_edu_au",
        "id": "sydney_edu_au",
    },
    "unsw_edu_au": {
        "us_gov_id": 0,
        "name": "University of New South Wales",
        "city": "Sydney",
        "state": "NSW",
        "country": "AU",
        "postal_code": "2006",
        "website": "unsw.edu.au",
        "edu_address": "unsw_edu_au",
        "id": "unsw_edu_au",
    },
    "demo_edu": {
        "us_gov_id": 0,
        "name": "Demo University",
        "city": "NYC",
        "state": "NY",
        "country": "USA",
        "postal_code": "12345",
        "website": "example.com",
        "edu_address": "demo_edu",
        "id": "demo_edu",
    },
    "example_edu": {
        "us_gov_id": 0,
        "name": "Example University",
        "city": "NYC",
        "state": "NY",
        "country": "USA",
        "postal_code": "12345",
        "website": "example.edu",
        "edu_address": "example_edu",
        "id": "example_edu",
    },
    "example_com": {
        "us_gov_id": 0,
        "name": "Example College",
        "city": "LA",
        "state": "CA",
        "country": "USA",
        "postal_code": "98765",
        "website": "example.com",
        "edu_address": "example_com",
        "id": "example_com",
    },
    "my_smccd_edu": {
        "us_gov_id": 0,
        "name": "San Mateo County Community College District",
        "city": "San Mateo",
        "state": "CA",
        "country": "USA",
        "postal_code": "94061",
        "website": "smccd.edu",
        "edu_address": "my_smccd_edu",
        "id": "my_smccd_edu",
    },
    "qa_edu": {
        "us_gov_id": 0,
        "name": "Quality University",
        "city": "Quito",
        "state": "CA",
        "country": "USA",
        "postal_code": "98765",
        "website": "qa.edu",
        "edu_address": "qa_edu",
        "id": "qa_edu",
    },
    "uhsa_edu_ag": {
        "us_gov_id": 0,
        "name": "University of Health Sciences Antigua",
        "city": "St John's",
        "state": "St John's",
        "country": "Antigua",
        "postal_code": "",
        "website": "www.uhsa.edu.ag",
        "edu_address": "uhsa_edu_ag",
        "id": "uhsa_edu_ag",
    },
    "stu_brownmackie_edu": {
        "us_gov_id": 0,
        "name": "Brown Mackie College",
        "city": "Cincinnati",
        "state": "Ohio",
        "country": "US",
        "postal_code": "45202",
        "website": "www.brownmackie.edu",
        "edu_address": "stu_brownmackie_edu",
        "id": "stu_brownmackie_edu",
    },
    "testcloud_io": {
        "us_gov_id": 0,
        "name": "Testcloud University",
        "city": "San Francisco",
        "state": "California",
        "country": "US",
        "postal_code": "94105",
        "website": "www.testcloud.io",
        "edu_address": "testcloud_io",
        "id": "testcloud_io",
    },
    "chegg_com": {
        "us_gov_id": 0,
        "name": "Chegg University",
        "city": "San Francisco",
        "state": "California",
        "country": "US",
        "postal_code": "94105",
        "website": "www.chegg.com",
        "edu_address": "chegg_com",
        "id": "chegg_com",
    },

}
DATA_OVERRIDES = {
    "columbia_edu": {
        "name": "Columbia University"
    }
}


class Command(BaseCommand):
    help = 'Imports all schools, based on our sources.'

    def handle(self, *args, **options):

        schools = {}
        schools_js = {}
        schools_js_app = {}

        # Process list from US
        # http://ope.ed.gov/accreditation/GetDownLoadFile.aspx
        # via
        # http://bit.ly/1cxSpmm
        ed_gov_source = os.path.abspath(os.path.join(
            BASE_DIR,
            "../../../../../",
            "data/Accreditation_2015_03/Accreditation_2015_03.csv",
        ))
        schools_module = os.path.abspath(os.path.join(
            BASE_DIR,
            "..",
            "school_data.py",
        ))
        schools_service = os.path.abspath(os.path.join(
            BASE_DIR,
            "../../../../../",
            "frontends/common/js/services/schools-full.js",
        ))
        schools_app_service = os.path.abspath(os.path.join(
            BASE_DIR,
            "../../../../../",
            "frontends/common/js/services/schools.js",
        ))

        # Import US Dept of Education Spreadsheet.
        counter = 0
        with open(ed_gov_source) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[9]:
                    # TODO: handle. .edu.uk
                    edu_address = ".".join(row[9].split(".")[-2:])
                    edu_address = edu_address.replace("/", "").lower().strip()
                if edu_address in ID_CORRECTIONS:
                    row[9] = ID_CORRECTIONS[edu_address]
                    edu_address = ID_CORRECTIONS[edu_address]
                if "@" not in edu_address:
                    bu_id = edu_address.replace(".", "_")

                    if bu_id not in schools:
                        if row[9].endswith("/"):
                            row[9] = row[9][:-1]

                        data = {
                            "us_gov_id": row[0],
                            "name": row[1],
                            "city": row[3],
                            "state": row[4],
                            "country": "US",
                            "postal_code": row[5].split("-")[0].replace('"', ''),
                            "website": row[9],
                            "edu_address": edu_address,
                            "id": bu_id,
                        }

                        js_data = {
                            "id": bu_id,
                            "name": row[1],
                            "city": row[3],
                            "state": row[4],
                            "country": "US",
                            "website": row[9],
                            "edu_address": edu_address,
                        }
                        js_app_data = {
                            "name": row[1],
                        }

                        schools[bu_id] = data

                        schools_js[bu_id] = js_data
                        schools_js_app[bu_id] = js_app_data
                        counter += 1

        # Import known campuses
        for c, val in KNOWN_CAMPUSES.items():
            schools[c] = val
            schools_js[c] = val
            schools_js_app[c] = {
                "name": val["name"]
            }

        # Handle data overrides.
        for k, val in DATA_OVERRIDES.items():
            if k in schools:
                for i, v in val.items():
                    schools[k][i] = v
                    schools_js[k][i] = v

        print("%s schools imported" % counter)
        with open(schools_module, "w+") as f:
            f.write("""school_data = %s
OVERRIDES = %s""" % (
                json.dumps(schools, indent=4, sort_keys=True),
                json.dumps(OVERRIDES, indent=4, sort_keys=True),
            ))
            f.write("\n")
        print("%s written." % schools_module)

        with open(schools_service, "w+") as f:
            f.write("""
angular.module('buddyupapp.services')
.factory('schoolsListFull', function() {
  return %s""" % json.dumps(schools_js, indent=4, sort_keys=True))

            f.write(""";
});
""")
        print("%s written." % schools_service)

        with open(schools_app_service, "w+") as f:
            f.write("""
angular.module('buddyupapp.services')
.factory('schoolsList', function(fire) {
  var masterList = %s""" % json.dumps(schools_js_app, indent=4, sort_keys=True))

            f.write(""";
  var ref = new Firebase(window.firebase_endpoint);
  ref.child("overrides").child("extra_schools").once('value', function(snapshot) {
    if (snapshot.val()) {
        if (snapshot.val()) {
            var schools = snapshot.val();
            for (var k in schools) {
              masterList[k] = schools[k];
            }
        }
    }
  }, function(err){
  });

  return masterList;
});
""")
        print("%s written." % schools_app_service)
