from django import template

register=template.Library()

@register.simple_tag
def display_rating(adventure):
    # Because just writing
    # [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0]
    # doesn't cut it don't you think ? 
    rating_steps = [ i * 0.01 for i in range(25, 525, 25)]

    # I'm sorry for that loop, 3AM
    ret = []
    alreadyChecked = 0
    checked = ""
    for step in rating_steps:
        if alreadyChecked == 0 and step >= adventure.avg_rating:
            checked = "checked='checked'"
            alreadyChecked = 1
        elif alreadyChecked == 1:
            checked = ""
            alreadyChecked == 2
                            
        ret.append(
            '<input class="star {split:4}" type="radio" name="rating-%s" '
            ' value="%s" title="%s" disabled="disabled" %s />' 
            % (adventure.id, step, adventure.avg_rating, checked)
        );
    return "\n".join(ret);
