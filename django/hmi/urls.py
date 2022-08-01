"""hmi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os.path
from django.contrib import admin
from django.urls import include, path
import browse.views
from abcli import file
from abcli import plugins
from abcli import keywords


abcli_path_git = os.getenv("abcli_path_git")

urlpatterns = [
    path("", browse.views.view_home, name="homepage"),
    path("admin/", admin.site.urls),
    path("help", browse.views.view_help),
    path("object/<path:object_path>", browse.views.view_object),
    path("tag/<str:tag>", browse.views.view_tag),
] + [
    path(
        f"{keywords.pack(plugin)}/",
        include(f"{plugin}.urls"),
    )
    for plugin in plugins.list_of_external()
    if plugin != "browser"
    and not file.exist(
        os.path.join(
            abcli_path_git,
            plugin.replace("_", "-"),
            "no-browser",
        )
    )
]
