#!/usr/bin/env python3

import gspread
from pathlib import Path
import plistlib

SPREADSHEET_ID = "1LfQKh3kn3gHf2IwtCKTx2tachnLfieQdqErn6tDLMsM"

if __name__ == '__main__':

    gc = gspread.oauth()
    workbook = gc.open_by_key(SPREADSHEET_ID)
    worksheet = workbook.worksheet("Devices")
    data = worksheet.get_all_records(numericise_ignore=['all'])

    manifests_path = Path.home() / "Desktop" / "manifests"

    if data:
        manifests_path.mkdir(parents=True, exist_ok=True)
        for row in data:
            pl = dict()
            pl['display_name'] = row['Name']

            if row['Asset'] != "":
                pl['asset_tag'] = row['Asset']

            if row['Included Manifests'] != "":
                pl['included_manifests'] = row['Included Manifests'].split(",")

            if row['Catalogs'] != "":
                pl['catalogs'] = row['Catalogs'].split(",")
            else:
                pl['catalogs'] = ['production']

            if row['Managed Installs'] != "":
                pl['managed_installs'] = row['Managed Installs'].split(",")
            
            if row['Optional Installs'] != "":
                pl['optional_installs'] = row['Optional Installs'].split(",")

            if row['Notes'] != "":
                pl['notes'] = row['Notes']

            manifest = manifests_path / row['Serial'] 
            print(f"Creating manifest for {row['Serial']}")
            with open(manifest, 'wb+') as f:
                pl = plistlib.dump(pl, f)
            
    else:
        print("No data loaded")