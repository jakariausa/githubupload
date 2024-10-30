from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .forms import ExpenseForm
from .mixins import SearchExpenseMixin
from .models import Expense


class ExpenseListView(SearchExpenseMixin, ListView):
    model = Expense
    paginate_by = 10


def expense_detail():
    system_prompt = """
    You are an AI assistant that retrieves specific information for ETL connectors. Your task is to extract data based on the given parameters and return only the allowed value that closely matches the requested field or multiple fields.
    """
    
    user_prompt = '''{
        "Connector": "SalesforceUpdated",
        "field": "supported and development environments for my application Updated",
        "description": "the available environments a user can interact with the connector in. If N/A then save PROD",
        "data_type": "JSON String array"
    }'''

    return get_chat_response(system_prompt, user_prompt, new_function_code)
def expense_create(request):
    template_name = 'expense/expense_form.html'
    form = ExpenseForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            expense = form.save()
            template_name = 'expense/expense_result.html'
            context = {'object': expense}
            return render(request, template_name, context)

    context = {'form': form}
    return render(request, template_name, context)


def expense_update(request, pk):
    template_name = 'expense/expense_update_form.html'
    instance = Expense.objects.get(pk=pk)
    form = ExpenseForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            expense = form.save()
            template_name = 'expense/expense_result.html'
            context = {'object': expense}
            return render(request, template_name, context)

    context = {'form': form, 'object': instance}
    return render(request, template_name, context)


@require_http_methods(['DELETE'])
def expense_delete(request, pk):
    template_name = 'expense/expense_table.html'
    obj = Expense.objects.get(pk=pk)
    obj.delete()
    return render(request, template_name)
