#!/usr/bin/env python3
import sys
import logging
import json
import gspread
from pathlib import Path
import plistlib

if __name__ == '__main__':

    def local_path(file):
        return Path(__file__).resolve().parent / file

    # Load in config file
    config = local_path("config.json")
    try:
        with open(config) as config_file:
            settings = json.load(config_file)
    except IOError:
        logging.error("No config.json file found! Please create one!")
        sys.exit(2)

    sheets = settings['sheets']

    gc = gspread.oauth()
    workbook = gc.open_by_key(sheets['spreadsheet_id'])
    worksheet = workbook.worksheet("Devices")
    data = worksheet.get_all_records(numericise_ignore=['all'])

    manifests_path = Path.home() / "Desktop" / "manifests"

    if data:
        manifests_path.mkdir(parents=True, exist_ok=True)
        for row in data:
            pl = dict()
            pl['display_name'] = row.get('Name',"")
            pl['asset_tag'] = row.get('Asset',"")
            pl['notes'] = row.get('Notes',"")

            pl['included_manifests'] = row.get("Included Manifests","").split(",")
            pl['managed_installs'] = row.get("Managed Installs","").split(",")
            pl['optional_installs'] = row.get("Optional Installs","").split(",")

            if row['Catalogs'] != "":
                pl['catalogs'] = row['Catalogs'].split(",")
            else:
                pl['catalogs'] = ['production']

            manifest = manifests_path / row['Serial'] 
            print(f"Creating manifest for {row['Serial']}")
            with open(manifest, 'wb+') as f:
                pl = plistlib.dump(pl, f)
            
    else:
        print("No data loaded")