hierarchy = {
    #"Broader health, development and rights":
        #{"CLIMATE": "Environmental health and agricultural support",
         # "?": "Continuity of Care",  # not found
         #"EQUITABLE": "Equitable care (Universal Healthcare)",
         #"EVIDENCEBASED": "Evidence, research, innovation and technology",
         #"FUNDING": "Policy and political change",
         #"WOMENSEQUALITY": "Empowerment and rights (women’s leadership)"},
    "Equity, Dignity, and Respect":
        {"ATTENTIVENESS": "Timely and attentive care",  # merged with 24x7
         # "BIRTHCOMPANION": "Birth Companion Choice", # no data
         # "INFORMEDCONSENT": "Informed Consent", # no data
         #"NOABUSE": "Ethical, lawful non-abusive and secure care",
         # "NONEGLIGENCE": "No unprofessional conduct", # no data
         #"RESPECT": "Respectful and dignified care",  # ??? not sure
         "RESPECTFULCARE": "Respectful and Dignified Care"
         },
    "Facility Improvements":
        {  # "24X7": "24x7 Services, Facilities, Providers", # merged into ATTENTIVENESS
            #"BEDS": "Beds and bedding",
            #"ELECTRICITY": "Electricity",
            #  "KITCHEN": "Improved kitchens", # no data
            #"LABORATORIES": "Laboratories",
            #"MANAGEMENT": "Administration and record-keeping",
            # "MATERNALWARDS": "Maternal, women's health wards, centers, waiting rooms", # no data
            # "PRIVACY": "More space and privacy",  # ???? # no data
            "BETTERFACILITIES": "Increased, full-functioning and close health facilities",
            "TRANSPORTATION": "Transportation infrastructure",
            "WASH": "Water, sanitation and hygiene"
        },
    "Health Professionals":
        {#"DOCTORS": "Increased, competent and better supported doctors",
         "HEALTHPROFESSIONALS": "Increased, competent and better supported health providers (general)"
         #"NURSESMIDWIVES": "Increased competent and better supported midwives and nurses",
         #"FEMALEPROVIDERS": "More female health providers",
         #"MALEPROVIDERS": "Male health providers",
         #"SPECIALISTS": "Specialists (surgeons, anesthetists)",
         #"SUPPORTLINKS": "Support for traditional, mobile and community health workers"
         },
    # "Uncodable": {
    #     "UNCODABLE": "Uncodable"
    # },
    "Other":
        {#"COMMUNITY": "Community engagement and accountability",
         "NOINTERVENTION": "Reduced medicalization or do not want service",
         "FITNESS": "Fitness and recreation",
         # "QUOTE": "Good Quotes",
         "HEALTH": "Improved health, well-being, health services",
         #"IMPROVED": "Male engagement, shifts in family/partner dynamics",
         # "INNOVATION": "Innovation, R&D and Technology", # merged into EVIDENCEBASED
         #"JOBS": "Economic opportunity and financial support",
         #  "MALEENGAGEMENT": "Male Engagement", # no data
         #  "PARENTALLEAVE": "Maternity, Paternity Leave", # no data
         #"NODEMAND": "No demand, everything is OK",
         #"NOHARMFULPRACTICE": "End violence, harmful practices against women and girls",
         #"NOTRELATED": "Not related",
         #"PEACE": "Peace, no conflict",
         "RELIGION": "Religious support",
         "SCHOOLS": "Schools and educational opportunity"
         #"WANTCHILDREN": "Want children"
         },
    #"Patient-Provider Communication":
        #{"BETTERCOMMUNICATION": "Complete and understandable communication",
         #    "COMMUNICATED": "Communication understanding (e.g. language)", # no data
         #"CONFIDENTIALITY": "Confidentiality and privacy",
         #   "FRIENDLY": "Friendly, hospitable and polite", # no data
         #  "NOSTIGMA": "No Judgement or Stigma", # no data
         # "TOFEELHEARD": "To feel heard and listened to, shared trust" #  no data
         #},
    #"Rights and Affordability": {
        #"FREE": "Free and affordable services and supplies",
        #   "NOCORRUPTION": "No corruption, informal payments, appropriate payment procedures", # no data
        #   "RECEIVING": "Receiving Entitled Government Benefit, Timely Reimbursements" #  no data
    #},
    "Services, Supplies, and Information":
        {
            "ADOLESCENT": "Adolescent & Youth-Friendly Info, Services, Supplies",
            "ANTENATAL": "Antenatal and Prenatal Info, Services, Supplies",
            #   "ALTERNATIVES": "Availability of Alternative Birthing Practices", #  no data
            "CANCER": "Breast, Cervical and Other Cancers Info, Services, Supplies",
            "CHILD": "Child health Info, Services, Supplies (Vaccines)",
            "DISABILITY": "Disability Info, Services, Supplies",
            "FAMILYPLANNING": "Family Planning & Contraceptive Info, Services, Supplies",
            "FOOD": "Food and Nutrition Info, Services, Supplies",
            "HIV": "HIV, STI, Hepatitis and TB Info, Services, Supplies",
            "INFERTILITY": "Infertility Info, Services, Supplies",
            "INFORMATION": "Counseling and awareness on health & services",
            "LABOR": "Labor and delivery Info, services, supplies",
            #"LGBTQ": "LGBTQ Info, Services and Supplies",
            "MALARIA": "Malaria and Vector-borne diseases Info, Services, Supplies",
            "MENSTRUAL": "Menstrual Health Info, Services, Supplies",
            "POSTPARTUM": "Post-Partum/Mental Health Info, Services, Supplies",
            #"MISCARRIAGE": "Miscarriage Info, services, supplies",
            "NCDS": "Noncommunicable Diseases Info, Services, Supplies",
            #    "PAINMANAGEMENT": "Pain Management Info, Services, Supplies", # no data
            "POSTMENOPAUSAL": "Post-menopausal/elderly Info, Services, Supplies",
            #"REFERRAL": "Referral system",
            #"SAFEABORTION": "Abortion Info, Services, Supplies",
            "SUPPLIES": "Medicines and supplies",
            "OTHERSERVICES": "Other specific services (e.g. dentistry, eye care)"
        },
    # "To feel safe from threat, danger and discrimination when seeking health services":
    #   {
    # "NODISCRIMINATION": "No Discrimination or Denial of Services re Sex, Ethnicity, Race, Class or Migratory Status", # no data
    #  "NOARRESTFEAR": "No Fear of Deportation, Detainment or Arrest", # no data
    #   "SECURITY": "Security provisions", # no data
    #       "TOFEELSAFE": "To feel safe and free from threat and danger (general)" #  no data
    #  }

}

category_colours = {#'Broader health, development and rights': '#2ca02c',
                    'Equity, Dignity, and Respect': '#ff7f0e',
                    'Facility Improvements': '#17becf',
                    'Health Professionals': '#bcbd22',
                    'Other': 'lightslategray',
                    #'Patient-Provider Communication': '#e377c2',
                    #'Rights and Affordability': '#d62728',
                    'Services, Supplies, and Information': '#1f77b4'}

mapping_to_top_level = {}
mapping_to_description = {}
for top_level, leaves in hierarchy.items():
    for code, name in leaves.items():
        mapping_to_top_level[code] = top_level
        mapping_to_description[code] = name


def get_menu_items():
    l = []
    # l.append({"label": "all categories", "value": ""})
    for top_level, leaves in hierarchy.items():

        l.append({"label": top_level, "value": top_level})
        for code, name in leaves.items():
            l.append({"label": "— " + name, "value": code})

    return l