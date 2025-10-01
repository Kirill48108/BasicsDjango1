from django import template

register = template.Library()

@register.filter
def add_class(field, css):
    base = field.field.widget.attrs.get("class", "")
    classes = (base + " " + css).strip()
    return field.as_widget(attrs={**field.field.widget.attrs, "class": classes})
