from mcfields.base.forms import EmailForm


def emailform(request):
    return {'EMAILFORM': EmailForm()}
