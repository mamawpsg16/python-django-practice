from django.shortcuts import render, get_object_or_404
# from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Choice, Question
from django.urls import reverse
from django.db.models import F
from django.views import generic

# Create your views here.

# def index(request):
#     # latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template("polls/index.html")
#     # context = {
#     #     "latest_question_list": latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))

#     # SHORTCUT 
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     data = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", data)


# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
    
#     # SHORTCUT
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/details.html", {"question": question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/details.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))