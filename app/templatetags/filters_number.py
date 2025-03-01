from django import template

register = template.Library()  

@register.filter
def short_number(value):
    """
    แปลงตัวเลขให้เป็น K, M เช่น:
    - 1,000 -> 1K
    - 1,000,000 -> 1M
    """
    try:
        value = int(value)
    except ValueError:
        return value  # ถ้าไม่ใช่ตัวเลข ให้คืนค่าเดิม

    if value >= 1_000_000:
        return f"{value // 1_000_000}M"
    elif value >= 1_000:
        return f"{value // 1_000}K"
    return str(value)
