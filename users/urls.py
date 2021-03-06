from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.user,
        name='user'),
    path(
        'order_history/<order_number>',
        views.order_history,
        name='order_history'),
    path(
        'feedback/',
        views.FeedbackView.as_view(),
        name='feedback'),
    path(
        'add_feedback/',
        views.SubmitFeedback.as_view(),
        name='add_feedback'),
]
