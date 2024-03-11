from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from subway_kl.handlers import SubwayOutletHandler
from subway_kl.models import SubwayContext, SubwayOutlet
from subway_kl.typings import OutletData

from .scraping import scrape_subway_kl_data


def index(request):
    data = {"key1": "value1", "key2": "value2"}

    # Render the template with the provided data
    return render(request, "index.html", context=data)


def question_handler(request):
    from .question_answer_ml import handle_query

    question = request.GET.get("question", None)

    # Validation
    if question is None or question == "":
        return JsonResponse({"answer": "No question"})
    if len(question) < 10:
        return JsonResponse({"answer": "Do type full question so AI can understand."})

    datas = SubwayContext.objects.first().context.split(".")
    datas.extend([obj.to_context() for obj in SubwayOutlet.objects.all()])

    # Process question
    score, answer = handle_query(question, datas)

    if score < 0.7:
        return JsonResponse({"answer": "I cannot understand the question."})

    return JsonResponse({"answer": answer})


def scrape_and_update_subway_kl_data(request):
    subway_kl_data: list[OutletData] = scrape_subway_kl_data()

    SubwayOutletHandler.bulk_update_or_create(subway_kl_data)

    return HttpResponse("Update complete")


def retrieve_subway_kl_geo_coord(request):
    SubwayOutletHandler.retrieve_geographical_data()

    return HttpResponse("Update complete")
