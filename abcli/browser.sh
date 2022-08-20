#! /usr/bin/env bash

export abcli_path_static="$abcli_path_git/browser/django/static"

function abcli_browser() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_help_line "abcli browser [object_1]" \
            "open [object_1] in browser."
        abcli_help_line "abcli browser host [install]" \
            "[install and] host browser."
        return
    fi

    local port=8000

    if [ "$task" == "host" ] ; then
        rm -rf $abcli_path_static
        mkdir -p $abcli_path_static
        cp -v $abcli_path_git/browser/abcli/assets/*.png $abcli_path_static

        local options=$2
        local install=$(abcli_option_int "$options" "install" 0)

        if [ "$install" == "1" ] ; then
            python3 -m pip install Django

            pushd $abcli_path_git/browser > /dev/null
            pip3 install -e .
            popd > /dev/null
        fi

        pushd $abcli_path_git/browser/django > /dev/null
        python3 manage.py runserver ${port} &
        popd > /dev/null

        abcli_browse_url "http://127.0.0.1:$port/"

        return
    fi

    local object=$(abcli_clarify_object "$1" $abcli_object)
    local url=http://127.0.0.1:$port/object/$object
    abcli_browse_url $url
}