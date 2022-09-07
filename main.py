# imports
from flask import Flask, render_template
from icecream import ic
from butter_cms import ButterCMS
import logging
import env
logger = logging.getLogger(__name__)

auth_token = env.BUTTERCMS_API_TOKEN
client = ButterCMS(auth_token)

app = Flask(__name__)


def get_navigation_menu(menu_name, levels=1):
    """
    Return a navigation menu from ButterCMS. Raise 404 if the "Main menu" is not found
    """
    params = {'levels': levels}
    butter_navigation_menu = client.content_fields.get(
        [menu_name], params=params)
    navigation_menus = butter_navigation_menu.get("data", {}).get(
        menu_name, []
    )
    ic(navigation_menus)

    main_menu = [
        menu for menu in navigation_menus if menu.get("name") == "Main menu"
    ]
    portal_menu = [menu for menu in navigation_menus if menu.get(
        "name") == "Portal Nav Bar"]
    ic(portal_menu)
    if not main_menu:
        raise Exception

    return main_menu[0], portal_menu[0]


@app.route("/<slug>")
def index(slug):
    params = None
    params = {
        'preview': 1
    }
    params = {
        'page': '1',
        'page_size': '10'
    }
    butter_page = client.pages.get(
        "*", slug, params=params
    )
    # ic(butter_page)
    if 'detail' in butter_page:
        if butter_page['detail'] == "Invalid token.":
            logger.error(
                """***Your Butter token is set to an invalid value. Please verify your token is correct.***""")
    page_data = butter_page.get("data")
    ic(page_data)
    nav_menu, portal_menu = get_navigation_menu("navigation_menu", levels=4)
    roles = ['warranty', 'general']
    return render_template("index.html", title="Home", page_menu=nav_menu, roles=roles, portal_menu=portal_menu)


if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)
