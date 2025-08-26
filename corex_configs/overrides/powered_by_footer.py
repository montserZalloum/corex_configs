def powered_by_footer(doc, method):
    """
    Before save hook for Website Settings.
    If the footer_powered field is blank, set it to 'Powered By Corex'.
    """
    if not doc.footer_powered:
        doc.footer_powered = "Powered By Corex"