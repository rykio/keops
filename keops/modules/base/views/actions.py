
import json
from django.shortcuts import render
from keops.forms.admin import ModelAdmin
#from keops.modules.form.options import ModelAdmin
#from keops.modules.admin.sites import site

def response_form(request, action):
    view_type = request.GET.get('view_type', action.view_type)
    state = request.GET.get('state', action.state or 'read')
    if action.view:
        pass
    else:
        # Auto detect ModelAdmin
        model = action.model.content_type.model_class()
        admin = getattr(model, '_admin', None)
        if not admin:
            # Auto create ModelAdmin
            admin = type("%sAdmin" % model.__name__, (ModelAdmin,), {'form': {}})()
            model.add_to_class('_admin', admin)
        return admin.view(request, view_type=view_type, action=action, state=state, **action.get_context())
        
def show_model_admin(request, admin, view_type):
    if view_type == 'list':
        return admin.list_view(request)
    
    import json
    from django import forms
    from keops.forms import extjs
    
    f = form
    
    if view_type == 'list':
        template = 'keops/base/list_form.js'
        fields = [name for name, field in form.get_form().base_fields.items() if not isinstance(field, forms.ModelMultipleChoiceField)]
        items = None
    else:
        #return form.add_view(request)
        template = 'keops/base/model_form.js'
        fields = [name for name, field in f.base_fields.items()]
        items = json.dumps(extjs.get_form_items(f))
    fields = json.dumps(fields + ['pk'])
    
    
    
    return render(request, template, {'form': f, 'model': model,
        'json': json, 'fields': fields, 'extjs': extjs, 'items': items,
        'model_name': '%s.%s' % (model._meta.app_label, model._meta.model_name),
        'form_title': model._meta.verbose_name_plural})
