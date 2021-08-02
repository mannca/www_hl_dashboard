# Hard-coded list
COUNTRIES_LIST = [('CMR', 'Cameroon', 'Cameroonian'),
                  # 'Chile',
                  # 'Honduras',
                  ('IND', 'India', 'Indian'),
                  ('KEN', 'Kenya', 'Kenyan'),
                  ('MWI', 'Malawi', 'Malawian'),
                  ('MEX', 'Mexico', 'Mexican'),
                  ('NGA', 'Nigeria', 'Nigerian'),
                  ('PAK', 'Pakistan', 'Pakistani'),
                  #  'Senegal',
                  # 'South Sudan',
                  ('TZA', 'Tanzania', 'Tanzanian'),
                  ('UGA', 'Uganda', 'Ugandan'),
                  # 'United Kingdom',
                  # 'United States'
                  ]

country_lookup = dict([(a, b) for a, b, c in COUNTRIES_LIST])
demonym_lookup = dict([(b, c) for a, b, c in COUNTRIES_LIST])


# TW: I commented out the countries with very few responses.

def get_unique_countries():
    unique_countries = []
    for alpha3code, country_name, demonym in COUNTRIES_LIST:
        unique_countries.append({"label": country_name, "value": country_name})
    return unique_countries