from util.code_hierarchy import mapping_to_description
from util.country_filters import demonym_lookup


def join_list_comma_and(listed):
    listed = list(listed)
    if len(listed) == 1:
        return listed[0]
    return '{} and {}'.format(', '.join(listed[:-1]), listed[-1])


def join_list_comma_or(listed):
    listed = list(listed)
    if len(listed) == 1:
        return listed[0]
    return '{} or {}'.format(', '.join(listed[:-1]), listed[-1])


def generate_age_description(lower_age, upper_age):
    if (lower_age is not None) and (upper_age is not None):
        return " aged " + str(lower_age) + "-" + str(upper_age)
    if lower_age is not None:
        return " aged " + str(lower_age) + " and up"
    return " aged " + str(upper_age) + " and under"


def generate_description_of_filter(comp_country, comp_code, lower_age, upper_age, text_filter, text_exclude, num_results):
    if num_results == 1:
        women = "woman"
    else:
        women = "women"
    if len(comp_country) > 0:
        desc = join_list_comma_and(demonym_lookup[c] for c in comp_country) + " " + women
    else:
        desc = women

    if lower_age is not None or upper_age is not None:
        desc += generate_age_description(lower_age, upper_age)

    mentioned = list([mapping_to_description.get(c, c) for c in comp_code])
    if len(mentioned) > 0:
        desc += " who mentioned " + join_list_comma_or(mentioned)

    if len(text_filter) > 0:
        if len(mentioned) == 0:
            desc += " who mentioned "
        else:
            desc += " and "
        desc += '"' + str(text_filter) + '"'

    if len(text_exclude) > 0:
        if len(mentioned) > 0:
            desc += ' but not "' + str(text_exclude) + '"'
        else:
            desc += ' who did not mention "' + str(text_exclude) + '"'

    if desc == women:
        desc = "all " + women
    desc = desc[0].upper() + desc[1:]

    return desc