from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Todo
from .forms import TodoForm
from retackAI_sdk import retack_client


# Initialize RetackConfig and RetackClient
retack_config = retack_client.RetackConfig(api_key="t9GTPRPL-Y2G7U4PfFD5oLGq")
retack_client_instance = retack_client.RetackClient(retack_config)

def index(request):
    try:
        todo_list = Todo.objects.order_by('id')
        form = TodoForm()
        context = {'todo_list': todo_list, 'form': form}
        return render(request, 'todo/index.html', context)
    except Exception as e:
        report_error(e, "index", context)

        return redirect('error_page')  

@require_POST
def addTodo(request):
    try:
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = Todo(text=request.POST['text'])
            new_todo.save()
        return redirect('index')
    except Exception as e:
        report_error(e, "addTodo", request)
        return redirect('error_page') 

def completeTodo(request, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id)
        todo.complete = True
        todo.save()
        return redirect('completeTodowrong')
    except Exception as e:
        report_error(e, "completeTodo", request)
        return redirect('error_page') 

def deleteCompleted(request):
    try:
        Todo.objects.filter(complete__exact=True).delete()
        return redirect('index')
    except Exception as e:
        report_error(e, "deleteCompleted", request)
        return redirect('error_page') 

def deleteAll(request):
    try:
        Todo.objects.all().delete()
        return redirect('index')
    except Exception as e:
        report_error(e, "deleteAll", request)
        return redirect('error_page') 

def report_error(exception, view_name, request):
    error_report = retack_client.ErrorReportRequest(
        error=f"Error in {view_name}: {str(exception)}",
        stack_trace=exception.__traceback__,
        user_context=retack_client.UserContext(
            username="anonymous",
            extras={"view": view_name, "method": request.method}
        )
    )
    retack_client_instance.report_error(error_report)
