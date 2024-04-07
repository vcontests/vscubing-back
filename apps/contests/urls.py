from django.urls import include, path

from .apis import (
    SolveListApi,
    SolveRetrieveApi,
    SolveCreateApi,
    SolveSubmitApi,
    SolveListBestInEveryDiscipline,
    SolveListBestOfEveryUser,
    RoundSessionWithSolvesListApi,
    # RoundSessionCurrentWithSolvesRetrieveApi,
    # RoundSessionRetrieveApi,
    ContestListApi,
    CurrentSolveApi,
    SubmittedSolvesApi,
)

solves_urlpatterns = [
    # path('', SolveListApi.as_view(), name='list'),
    path('<int:pk>/retrieve/', SolveRetrieveApi.as_view(), name='retrieve'),
    path('create/', SolveCreateApi.as_view(), name='create'),
    path('submit/<int:pk>/', SolveSubmitApi.as_view(), name='submit'),
    path('best-in-every-discipline/', SolveListBestInEveryDiscipline.as_view(), name='list-best-in-every-discipline'),
    path('best-of-every-user/', SolveListBestOfEveryUser.as_view(), name='list-best-of-every-user'),
]

ongoing_contest_urlpatterns = [
    path('submitted-solves/', SubmittedSolvesApi.as_view(), name='list-submitted'),
    path('current-solve/', CurrentSolveApi.as_view(), name='retrieve-current')
]

contests_urlpatterns = [
    path('', ContestListApi.as_view(), name='list'),
]

round_session_urlpatterns = [
    path(
        'with-solves/',
        RoundSessionWithSolvesListApi.as_view(),
        name='list-with-nested-solves'
    ),
    # path(
    #     'with-solves/<int:user_id>/retrieve/',
    #     RoundSessionRetrieveApi.as_view(),
    #     name='retrieve-with-nested-solves'
    # ),
    # path(
    #     'current/',
    #     RoundSessionCurrentWithSolvesRetrieveApi.as_view(),
    #     name='retrieve-current'
    # ),
]

urlpatterns = [
    path('solves/', include(solves_urlpatterns)),
    path('contests/', include(contests_urlpatterns)),
    path('round-sessions/', include(round_session_urlpatterns)),
    path('ongoing-contest/', include(ongoing_contest_urlpatterns)),
]
