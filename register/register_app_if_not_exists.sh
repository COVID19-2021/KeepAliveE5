#!/usr/bin/env bash

APP_NAME='E5_ALIVE'
REPLY_URI='http://localhost:53682/'
PERMISSIONS_FILE='./required-resource-accesses.json'
CONFIG_PATH='../config'

[ -d "$CONFIG_PATH" ] || mkdir -p "$CONFIG_PATH"

jq() {
    echo "$1" |
        python3 -c "import sys, json; print(json.load(sys.stdin)$2)"
}

get_app_id() {
    ret=$(az ad app list --display-name "$APP_NAME")
    [ "$ret" != "[]" ] && {
        az ad app delete --id "$(jq "$ret" "[0]['appId']")"
    }

    # --identifier-uris api://e5.app \
    ret="$(az ad app create \
        --display-name "$APP_NAME" \
        --reply-urls "$REPLY_URI" \
        --available-to-other-tenants true \
        --required-resource-accesses "@$PERMISSIONS_FILE")"

    app_id="$(jq "$ret" "['appId']")"

    # set owner
    az ad app owner add \
        --id "$app_id" \
        --owner-object-id "$user_id"

    # grant admin consent
    az ad app permission admin-consent --id "$app_id"
}

register_app() {
    # install cli
    [ "$(command -v az)" ] || apt install -y azure-cli
    # curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

    az account clear
    # login
    ret="$(az login \
        --allow-no-subscriptions \
        -u "$USER" \
        -p "$PASSWD" 2>/dev/null)"

    tenant_id="$(jq "$ret" "[0]['tenantId']")"
    user_id="$(jq "$(az ad user list)" "[0]['objectId']")"
    get_app_id

    # generate client secret
    ret="$(az ad app credential reset \
        --id "$app_id" \
        --years 100)"
    client_secret="$(jq "$ret" "['password']")"
}

[ "$USER" ] && [ "$PASSWD" ] && {
    register_app
    # waiting for azure system to refresh
    sleep 60

    cat >"$CONFIG_PATH/app.json" <<EOF
{
    "username": "$USER",
    "password": "$PASSWD",
    "client_id": "$app_id",
    "client_secret": "$client_secret",
    "redirect_uri": "$REPLY_URI"
}
EOF

    node server.js &
    sleep 2
    node client.js
    sleep 2
}
