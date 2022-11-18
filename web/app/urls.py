from django.urls import path

from .views import *


app_name = 'app'

urlpatterns = [

    path('home/', home, name = 'home'),

]

htmx_urlpatterns = [

    path('search-note', search_note, name='search-note'),

    path('create-notepad/', create_notepad, name = 'create-notepad'),
    path('get-notepad/<uuid:uid>/', get_notepad, name = 'get-notepad'),
    path('delete-notepad/', delete_notepad, name = 'delete-notepad'),

    path('create-note/', create_note, name = 'create-note'),
    path('get-note/<uuid:uid>/', get_note, name = 'get-note'),

    path('pin-note/', pin_note, name = 'pin-note'),
    path('move-note/<uuid:uid>/', move_note, name = 'move-note'),
    path('delete-note/', delete_note, name = 'delete-note'),

    path('upload-image/', upload_image, name = 'upload-image'),
    path('delete-image/<uuid:uid>/', delete_image, name = 'delete-image'),

]

ajax_urlpatterns = [

    path('edit-notepad/', edit_notepad, name = 'edit-notepad'),

    path('update-note/', update_note, name = 'update-note'),

]

urlpatterns += htmx_urlpatterns
urlpatterns += ajax_urlpatterns