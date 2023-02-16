from django import template

register = template.Library()

# Units of Measurement Conversion Filters
@register.filter(is_safe=True)
def convert_feeds(value, units):
    if units == 'IMPERIAL':
        return str(round(value / 29.574))
    else:
        return str(value)
    
@register.filter(is_safe=True)
def convert_weights(value, units):
    # kg to lbs & oz
    if units == 'IMPERIAL':
        lbs = value * 2.205
        oz = round((lbs - int(lbs)) * 16)
        round_lbs = round(lbs)
        return f'{round_lbs} lbs {oz} oz'

    else:
        return str(value)





