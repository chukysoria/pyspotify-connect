
from flask import Flask, jsonify, request

import spotifyconnect


app = Flask('SpotifyConnect')

# #API routes
# Login routes


@app.route('/login/_zeroconf', methods=['GET', 'POST'])
def login_zeroconf():
    action = request.args.get('action') or request.form.get('action')
    if not action:
        return jsonify({
            'status': 301,
            'spotifyError': 0,
            'statusString': 'ERROR-MISSING-ACTION'})
    if action == 'getInfo' and request.method == 'GET':
        return get_info()
    elif action == 'addUser' and request.method == 'POST':
        return add_user()
    else:
        return jsonify({
            'status': 301,
            'spotifyError': 0,
            'statusString': 'ERROR-INVALID-ACTION'})


def get_info():
    zeroconf_vars = spotifyconnect._session_instance.get_zeroconf_vars()

    return jsonify({
        'status': 101,
        'spotifyError': 0,
        'activeUser': zeroconf_vars.active_user,
        'brandDisplayName': spotifyconnect._session_instance.config.brand_name,
        'accountReq': zeroconf_vars.account_req,
        'deviceID': zeroconf_vars.device_id,
        'publicKey': zeroconf_vars.public_key,
        'version': '2.0.1',
        'deviceType': zeroconf_vars.device_type,
        'modelDisplayName': spotifyconnect._session_instance.config.model_name,
        # Status codes are ERROR-OK (not actually an error),
        # ERROR-MISSING-ACTION, ERROR-INVALID-ACTION, ERROR-SPOTIFY-ERROR,
        # ERROR-INVALID-ARGUMENTS, ERROR-UNKNOWN, and ERROR_LOG_FILE
        'statusString': 'ERROR-OK',
        'remoteName': zeroconf_vars.remote_name,
    })


def add_user():
    args = request.form
    # TODO: Add parameter verification
    username = str(args.get('userName'))
    blob = str(args.get('blob'))
    clientKey = str(args.get('clientKey'))

    spotifyconnect._session_instance.connection.login(
        username, zeroconf=(blob, clientKey))

    return jsonify({
        'status': 101,
        'spotifyError': 0,
        'statusString': 'ERROR-OK'
    })
