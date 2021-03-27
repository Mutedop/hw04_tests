# ServerRunTests: 

# ```
# ----------------------- Проверка flake8 пройдена -----------------------

# Creating test database for alias 'default'...
# ../app/posts/views.py:11: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'posts.models.Post'> QuerySet.
#   paginator = Paginator(latest, 10)
# ........../app/posts/views.py:24: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'posts.models.Post'> QuerySet.
#   paginator = Paginator(posts, 10)
# /app/posts/views.py:78: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'posts.models.Post'> QuerySet.
#   paginator = Paginator(posts, 10)
# ..........
# ----------------------------------------------------------------------
# Ran 22 tests in 0.582s

# OK
# Destroying test database for alias 'default'...
# System check identified no issues (0 silenced).
# -------------------- Проверка ваших тестов пройдена --------------------

# ============================= test session starts ==============================
# platform linux -- Python 3.7.4, pytest-5.3.5, py-1.8.1, pluggy-0.13.1 -- /usr/local/bin/python
# django: settings: yatube.settings (from env)
# rootdir: /app, inifile: pytest.ini
# plugins: Faker-6.6.3, django-3.8.0
# collecting ... collected 19 items

# tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_view_get PASSED [  5%]
# tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_not_in_context_view FAILED [ 10%]
# tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_not_in_view_context FAILED [ 15%]
# tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_view PASSED [ 21%]
# tests/test_paginator.py::TestGroupPaginatorView::test_profile_paginator_view FAILED [ 26%]
# tests/test_about.py::TestTemplateView::test_about_author_tech PASSED     [ 31%]
# tests/test_homework.py::TestPost::test_post_create PASSED                [ 36%]
# tests/test_homework.py::TestGroup::test_group_create PASSED              [ 42%]
# tests/test_homework.py::TestGroupView::test_group_view PASSED            [ 47%]
# tests/test_new.py::TestNewView::test_new_view_get PASSED                 [ 52%]
# tests/test_new.py::TestNewView::test_new_view_post PASSED                [ 57%]
# tests/test_post.py::TestPostView::test_post_view_get PASSED              [ 63%]
# tests/test_post.py::TestPostEditView::test_post_edit_view_get PASSED     [ 68%]
# tests/test_post.py::TestPostEditView::test_post_edit_view_author_get PASSED [ 73%]
# tests/test_post.py::TestPostEditView::test_post_edit_view_author_post PASSED [ 78%]
# tests/test_profile.py::TestProfileView::test_profile_view_get PASSED     [ 84%]
# tests/test_homework.py::TestPost::test_post_model PASSED                 [ 89%]
# tests/test_homework.py::TestPost::test_post_admin PASSED                 [ 94%]
# tests/test_homework.py::TestGroup::test_group_model PASSED               [100%]

# =================================== FAILURES ===================================
# /app/tests/test_paginator.py:26: AssertionError: Проверьте, что переменной `paginator` нет в контексте страницы `/group/<slug>/`
# /app/tests/test_paginator.py:35: AssertionError: Проверьте, что объект `page` страницы `/` не содержит `paginator` в контексте
# /app/tests/test_paginator.py:54: AssertionError: Проверьте, что объект `page` страницы `/` не содержит `paginator` в контексте
# =============================== warnings summary ===============================
# tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_view_get
# tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_not_in_context_view
# tests/test_homework.py::TestGroupView::test_group_view
#   /app/posts/views.py:24: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'posts.models.Post'> QuerySet.
#     paginator = Paginator(posts, 10)

# tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_not_in_view_context
# tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_view
#   /app/posts/views.py:11: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'posts.models.Post'> QuerySet.
#     paginator = Paginator(latest, 10)

# tests/test_paginator.py::TestGroupPaginatorView::test_profile_paginator_view
# tests/test_profile.py::TestProfileView::test_profile_view_get
#   /app/posts/views.py:78: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'posts.models.Post'> QuerySet.
#     paginator = Paginator(posts, 10)

# -- Docs: https://docs.pytest.org/en/latest/warnings.html
# =================== 3 failed, 16 passed, 7 warnings in 3.31s ===================
# ```
