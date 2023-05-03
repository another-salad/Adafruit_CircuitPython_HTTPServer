# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)


class Device:
    def turn_on(self):  # pylint: disable=no-self-use
        print("Turning on device.")

    def turn_off(self):  # pylint: disable=no-self-use
        print("Turning off device.")


def get_device(device_id: str) -> Device:  # pylint: disable=unused-argument
    """
    This is a **made up** function that returns a `Device` object.
    """
    return Device()


@server.route("/device/<device_id>/action/<action>")
@server.route("/device/emergency-power-off/<device_id>")
def perform_action(
    request: Request, device_id: str, action: str = "emergency_power_off"
):
    """
    Performs an "action" on a specified device.
    """

    device = get_device(device_id)

    if action in ["turn_on"]:
        device.turn_on()
    elif action in ["turn_off", "emergency_power_off"]:
        device.turn_off()
    else:
        with Response(request, content_type="text/plain") as response:
            response.send(f"Unknown action ({action})")
        return

    with Response(request, content_type="text/plain") as response:
        response.send(f"Action ({action}) performed on device with ID: {device_id}")


@server.route("/device/.../status", append_slash=True)
@server.route("/device/....", append_slash=True)
def device_status(request: Request):
    """
    Returns the status of all devices no matter what their ID is.
    Unknown commands also return the status of all devices.
    """

    with Response(request, content_type="text/plain") as response:
        response.send("Status of all devices: ...")


server.serve_forever(str(wifi.radio.ipv4_address))
