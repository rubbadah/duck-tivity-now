def rgb(r, g, b, a=255):
    """255基準のRGB値を0-1の値に変換

    Args:
        r (int): red.
        g (int): green.
        b (int): blue.
        a (int, optional): alpha. Defaults to 255.

    Returns:
        tuple: (r / 255.0, g / 255.0, b / 255.0, a / 255.0)
    """

    # rgb(166, 215, 232)
    # rgb(113, 193, 209)
    # rgb(59, 143, 176)
    # rgb(91, 97, 128)
    # rgb(61, 64, 77)
    return (r / 255.0, g / 255.0, b / 255.0, a / 255.0)
