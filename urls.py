from django.urls import path
from . import views

urlpatterns = [
    # URLs go here
    # Alert
    path(
        'alert/',
        views.AlertCollection.as_view(),
        name='alert_collection',
    ),
    # Category
    path(
        'category/',
        views.CategoryCollection.as_view(),
        name='category_collection',
    ),
    path(
        'category/<int:pk>/',
        views.CategoryResource.as_view(),
        name='category_resource',
    ),
    # Reading
    path(
        'reading/',
        views.ReadingCollection.as_view(),
        name='reading_collection',
    ),
    path(
        'reading/<int:pk>/',
        views.ReadingResource.as_view(),
        name='reading_resource',
    ),
    # Source
    path(
        'source/',
        views.SourceCollection.as_view(),
        name='source_collection',
    ),
    path(
        'source/<int:pk>/',
        views.SourceResource.as_view(),
        name='source_resource',
    ),
    # Source Group Summary
    path(
        'source_group_summary/<str:source>/',
        views.SourceGroupSummaryCollection.as_view(),
        name='source_group_summary_collection',
    ),
    # Source Share
    path(
        'source_share/',
        views.SourceShareCollection.as_view(),
        name='source_share_collection',
    ),
    path(
        'source_share/<int:pk>/',
        views.SourceShareResource.as_view(),
        name='source_share_resource',
    ),
    # Source Summary
    path(
        'source_summary/<int:source_id>/',
        views.SourceSummaryCollection.as_view(),
        name='source_summary_collection',
    ),
    # Unit
    path(
        'unit/',
        views.UnitCollection.as_view(),
        name='unit_collection',
    ),
    path(
        'unit/<int:pk>/',
        views.UnitResource.as_view(),
        name='unit_resource',
    ),
]
