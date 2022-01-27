from librouteros import connect
import frappe


@frappe.whitelist()
def update_customer_account(docname, disabled=True):
    connection_deets = frappe.db.get_value(
        "Customer", docname, ["default_router", "address_id_"], as_dict=1
    )
    network_router = frappe.get_doc(
        "Network Router", connection_deets.get("default_router")
    )
    payload = dict(
        host=network_router.get("host"),
        port=network_router.get("port"),
        username=network_router.get("username"),
        password=network_router.get("password"),
        address=connection_deets.get("address_id_"),
    )
    client_actions(disabled=disabled,**payload)


def client_actions(disabled=True, **connection_details):
    api = None
    if connection_details.port:
        api = connect(
            username=connection_details.username,
            password=connection_details.password,
            host=connection_details.host,
            port=connection_details.port,
            timeout=60,
        )
    else:
        api = connect(
            username=connection_details.username,
            password=connection_details.password,
            host=connection_details.host,
            timeout=60,
        )
    if not api:
        return
    ips = api.path("ip", "address")

    client_network_id = list(
        filter(lambda x: x.get("address") == connection_details.address, list(ips))
    )[0]

    params = {"disabled": disabled, ".id": client_network_id.get(".id")}

    ips.update(**params)

    return client_network_id
